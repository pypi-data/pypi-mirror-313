// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use std::f64::consts::FRAC_PI_2;

use serde::{Deserialize, Serialize};

use std::fmt::Debug;

use crate::{
    decompose,
    graph::GraphMatrix,
    ir::{
        gate::{Matrix, QuantumGate},
        hamiltonian::Hamiltonian,
    },
};

pub use crate::{
    ir::{
        instructions::Instruction,
        qubit::{LogicalQubit, PhysicalQubit, Qubit},
    },
    process::{DumpData, Sample},
};

#[derive(Debug, Default)]
pub struct Configuration {
    pub measure: FeatureStatus,
    pub sample: FeatureStatus,
    pub exp_value: FeatureStatus,
    pub dump: FeatureStatus,
    pub execution: Option<QuantumExecution>,
    pub num_qubits: usize,
    pub qpu: Option<QPU>,
}

#[derive(Debug)]
pub enum QuantumExecution {
    Live(Box<dyn LiveExecution>),
    Batch(Box<dyn BatchExecution>),
}

pub trait LiveExecution {
    fn gate(&mut self, gate: QuantumGate, target: LogicalQubit, control: &[LogicalQubit]);
    fn measure(&mut self, qubits: &[LogicalQubit]) -> u64;
    fn exp_value(&mut self, hamiltonian: &Hamiltonian<LogicalQubit>) -> f64;
    fn sample(&mut self, qubits: &[LogicalQubit], shots: usize) -> Sample;
    fn dump(&mut self, qubits: &[LogicalQubit]) -> DumpData;
    fn free_aux(&mut self, aux_group: usize, num_qubits: usize);
}

pub trait BatchExecution {
    fn submit_execution(
        &mut self,
        logical_circuit: &[Instruction<LogicalQubit>],
        physical_circuit: Option<&[Instruction<PhysicalQubit>]>,
    );
    fn get_results(&mut self) -> ResultData;
}

#[derive(Default, Debug, Clone, Copy)]
pub enum FeatureStatus {
    Disable,
    #[default]
    Allowed,
    ValidAfter,
}

#[derive(Debug, Clone, Default, Deserialize, Serialize)]
pub struct ResultData {
    pub measurements: Vec<u64>,
    pub exp_values: Vec<f64>,
    pub samples: Vec<Sample>,
    pub dumps: Vec<DumpData>,
}

#[derive(Debug, Default)]
pub struct QPU {
    pub(crate) coupling_graph: Option<GraphMatrix<PhysicalQubit>>,
    pub u2_gates: U2Gates,
    pub u4_gate: U4Gate,
}

#[derive(Debug, Default, Clone, Copy)]
pub enum U2Gates {
    #[default]
    All,
    ZYZ,
    RzSx,
}

impl U2Gates {
    pub fn decompose(&self, matrix: &Matrix) -> Vec<QuantumGate> {
        match self {
            Self::ZYZ => Self::decompose_zyz(matrix),
            Self::RzSx => Self::decompose_rzsx(matrix),
            Self::All => panic!("decomposition not required"),
        }
    }

    fn decompose_zyz(matrix: &Matrix) -> Vec<QuantumGate> {
        let (_, theta_0, theta_1, theta_2) = decompose::util::zyz(*matrix);
        if theta_1.abs() <= 1e-14 {
            vec![QuantumGate::RotationZ(theta_2 + theta_0)]
        } else {
            vec![
                QuantumGate::RotationZ(theta_2),
                QuantumGate::RotationY(theta_1),
                QuantumGate::RotationZ(theta_0),
            ]
        }
    }

    fn decompose_rzsx(matrix: &Matrix) -> Vec<QuantumGate> {
        let (_, theta_0, theta_1, theta_2) = decompose::util::zyz(*matrix);
        if theta_1.abs() <= 1e-14 {
            vec![QuantumGate::RotationZ(theta_2 + theta_0)]
        } else {
            vec![
                QuantumGate::RotationZ(theta_2),
                QuantumGate::RotationX(FRAC_PI_2),
                QuantumGate::RotationZ(theta_1),
                QuantumGate::RotationX(-FRAC_PI_2),
                QuantumGate::RotationZ(theta_0),
            ]
        }
    }
}

#[derive(Debug, Default, Clone, Copy)]
pub enum U4Gate {
    #[default]
    CX,
    CZ,
}

impl std::fmt::Debug for dyn LiveExecution {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("LiveExecution")
    }
}

impl std::fmt::Debug for dyn BatchExecution {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("BatchExecution")
    }
}

impl QPU {
    pub fn new(
        coupling_graph: Option<Vec<(usize, usize)>>,
        num_qubits: usize,
        u2_gates: U2Gates,
        u4_gate: U4Gate,
    ) -> Self {
        let coupling_graph = coupling_graph.map(|edges| {
            let mut coupling_graph: GraphMatrix<PhysicalQubit> = GraphMatrix::new(num_qubits);
            for (i, j) in edges {
                coupling_graph.set_edge(i.into(), j.into(), 1);
            }
            coupling_graph
        });

        Self {
            coupling_graph,
            u2_gates,
            u4_gate,
        }
    }
}

impl U4Gate {
    pub(crate) fn cnot<Q: Copy>(&self, control: Q, target: Q) -> Vec<(QuantumGate, Q, Option<Q>)> {
        match self {
            Self::CX => vec![(QuantumGate::PauliX, target, Some(control))],
            Self::CZ => vec![
                (QuantumGate::Hadamard, target, None),
                (QuantumGate::PauliZ, target, Some(control)),
                (QuantumGate::Hadamard, target, None),
            ],
        }
    }

    pub(crate) fn swap<Q: Copy>(&self, qubit_a: Q, qubit_b: Q) -> Vec<(QuantumGate, Q, Option<Q>)> {
        self.cnot(qubit_a, qubit_b)
            .into_iter()
            .chain(self.cnot(qubit_b, qubit_a))
            .chain(self.cnot(qubit_a, qubit_b))
            .collect()
    }
}

impl FeatureStatus {
    pub fn from(value: i32) -> Self {
        match value {
            0 => Self::Disable,
            1 => Self::Allowed,
            2 => Self::ValidAfter,
            _ => panic!("Invalid value for FeatureStatus"),
        }
    }
}
