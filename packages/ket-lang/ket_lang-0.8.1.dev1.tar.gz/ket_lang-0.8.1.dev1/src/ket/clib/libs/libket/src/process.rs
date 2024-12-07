// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};

use crate::{
    circuit::Circuit,
    decompose::{AuxMode, Registry, Schema, State},
    error::{KetError, Result},
    execution::{Configuration, FeatureStatus, QuantumExecution, Qubit},
    ir::{
        gate::QuantumGate,
        hamiltonian::Hamiltonian,
        instructions::Instruction,
        qubit::{LogicalQubit, PhysicalQubit},
    },
    mapping,
    prelude::QPU,
};

type QubitList = Vec<LogicalQubit>;
type CtrlStack = Vec<QubitList>;

#[derive(Debug)]
enum GateInstruction {
    Gate {
        gate: QuantumGate,
        target: LogicalQubit,
        control: Vec<LogicalQubit>,
    },
    AuxRegistry(std::rc::Rc<std::cell::RefCell<Registry>>),
}

type GateList = Vec<GateInstruction>;
pub type Sample = (Vec<u64>, Vec<u64>);

#[derive(Debug, Clone, Default, Deserialize, Serialize)]
pub struct DumpData {
    pub basis_states: Vec<Vec<u64>>,
    pub amplitudes_real: Vec<f64>,
    pub amplitudes_imag: Vec<f64>,
}

#[derive(Debug, Serialize)]
pub struct Metadata {
    pub logical_gate_count: HashMap<usize, usize>,
    pub logical_circuit_depth: usize,
    pub physical_gate_count: Option<HashMap<usize, usize>>,
    pub physical_circuit_depth: Option<usize>,
    pub allocated_qubits: usize,
    pub terminated: bool,
    pub decomposition: HashMap<String, usize>,
}

#[derive(Debug, Default)]
pub struct Process {
    ctrl_stack: Vec<CtrlStack>,
    ctrl_list: QubitList,
    ctrl_list_is_valid: bool,

    logical_circuit: Circuit<LogicalQubit>,

    physical_circuit: Option<Circuit<PhysicalQubit>>,

    adj_stack: Vec<GateList>,

    measurements: Vec<Option<u64>>,

    samples: Vec<Option<Sample>>,

    exp_values: Vec<Option<f64>>,

    dumps: Vec<Option<DumpData>>,

    configuration: Configuration,

    allocated_qubits: usize,
    qubit_count: usize,

    aux_count: usize,

    pub(crate) qubit_valid: HashMap<LogicalQubit, bool>,
    pub(crate) qubit_measured: HashMap<LogicalQubit, bool>,

    alloc_stack: Vec<LogicalQubit>,
    clean_qubits: HashSet<LogicalQubit>,

    terminated: bool,

    decomposition_stats: HashMap<String, usize>,
}

impl Process {
    pub fn new(configuration: Configuration) -> Self {
        Self {
            ctrl_stack: vec![Vec::new()],
            configuration,
            ..Default::default()
        }
    }

    fn flatten_control_qubits(&mut self) {
        if !self.ctrl_list_is_valid {
            self.ctrl_list = self
                .ctrl_stack
                .last()
                .unwrap()
                .clone()
                .into_iter()
                .flatten()
                .collect();
            self.ctrl_list_is_valid = true;
        }
    }

    fn non_gate_checks(
        &mut self,
        qubits: Option<&[LogicalQubit]>,
        feature: Option<FeatureStatus>,
    ) -> Result<()> {
        if self.terminated {
            Err(KetError::TerminatedProcess)
        } else if matches!(feature, Some(FeatureStatus::Disable)) {
            Err(KetError::MeasurementDisabled)
        } else if !(self.ctrl_stack.len() == 1 && self.ctrl_stack[0].is_empty()) {
            Err(KetError::ControlledScope)
        } else if !self.adj_stack.is_empty() {
            Err(KetError::InverseScope)
        } else if qubits.map_or(false, |qubits| {
            qubits
                .iter()
                .any(|qubit| !*self.qubit_valid.entry(*qubit).or_insert(true))
        }) {
            Err(KetError::QubitUnavailable)
        } else {
            Ok(())
        }
    }

    fn gate_checks(&mut self, target: LogicalQubit) -> Result<()> {
        if !*self.qubit_valid.entry(target).or_insert(true) {
            Err(KetError::QubitUnavailable)
        } else if self.ctrl_list.contains(&target) {
            Err(KetError::ControlTargetOverlap)
        } else if self.terminated {
            Err(KetError::TerminatedProcess)
        } else {
            Ok(())
        }
    }

    fn adj_ctrl_checks(&mut self, qubits: Option<&[LogicalQubit]>) -> Result<()> {
        if qubits.map_or(false, |qubits| {
            qubits
                .iter()
                .any(|qubit| !*self.qubit_valid.entry(*qubit).or_insert(true))
        }) {
            Err(KetError::QubitUnavailable)
        } else if qubits.map_or(false, |qubits| {
            qubits.iter().any(|qubit| self.ctrl_list.contains(qubit))
        }) {
            Err(KetError::ControlTwice)
        } else if self.terminated {
            Err(KetError::TerminatedProcess)
        } else {
            Ok(())
        }
    }

    pub fn alloc(&mut self) -> Result<LogicalQubit> {
        self.non_gate_checks(None, None)?;

        self.reserve_qubits(1)?;
        self.allocated_qubits += 1;

        Ok(self.alloc_stack.pop().unwrap())
    }

    fn reserve_qubits(&mut self, num_qubits: usize) -> Result<()> {
        while self.alloc_stack.len() < num_qubits {
            if self.allocated_qubits > self.configuration.num_qubits {
                return Err(KetError::MaxQubitsReached);
            }

            let qubit = LogicalQubit::main(self.qubit_count);

            self.qubit_count += 1;

            self.alloc_stack.push(qubit);
            assert!(self.clean_qubits.insert(qubit));
        }

        Ok(())
    }

    fn try_alloc_aux(
        &mut self,
        num_qubits: usize,
        interacting_qubits: Option<&[LogicalQubit]>,
    ) -> Option<Vec<LogicalQubit>> {
        if (interacting_qubits.is_none()
            && (num_qubits + self.allocated_qubits) > self.configuration.num_qubits)
            || (interacting_qubits.is_some()
                && (num_qubits + interacting_qubits.unwrap().len()) > self.configuration.num_qubits)
        {
            return None;
        }

        let result: Vec<_> = (0..num_qubits)
            .map(|index| LogicalQubit::aux(index + self.aux_count))
            .collect();

        self.aux_count += num_qubits;

        let reserver_qubits = if let Some(interacting_qubits) = interacting_qubits {
            let dirty_available = self.allocated_qubits - interacting_qubits.len();
            if dirty_available >= num_qubits {
                0
            } else {
                num_qubits - dirty_available
            }
        } else {
            num_qubits
        };

        self.reserve_qubits(reserver_qubits).unwrap(); // this should not fail if the first check is correct

        Some(result)
    }

    fn free_aux(&mut self, registry: &Registry) {
        if let Some(aux_qubits) = &registry.aux_qubits {
            let mut allocated = HashSet::new();
            for aux_qubit in aux_qubits {
                let mut main_qubit = None;
                for interacting_qubit in self.logical_circuit.interacting_qubits(*aux_qubit) {
                    for candidate_qubit in self
                        .logical_circuit
                        .interacting_qubits_rev(*interacting_qubit)
                    {
                        if candidate_qubit.is_aux() {
                            continue;
                        }
                        let use_this = match &registry.interacting_qubits {
                            Some(interacting_qubits) => {
                                !interacting_qubits.contains(candidate_qubit)
                                    && !allocated.contains(candidate_qubit)
                            }
                            None => {
                                self.clean_qubits.contains(candidate_qubit)
                                    && !allocated.contains(candidate_qubit)
                            }
                        };

                        if use_this {
                            main_qubit = Some(*candidate_qubit);
                            break;
                        }
                    }
                }
                let main_qubit = if let Some(main_qubit) = main_qubit {
                    main_qubit
                } else {
                    let mut main_qubit = None;
                    for candidate_qubit in &self.clean_qubits {
                        if !allocated.contains(candidate_qubit) {
                            main_qubit = Some(*candidate_qubit);
                            break;
                        }
                    }

                    if main_qubit.is_none() {
                        for candidate_qubit in 0..self.allocated_qubits {
                            let candidate_qubit = LogicalQubit::main(candidate_qubit);
                            if !allocated.contains(&candidate_qubit)
                                && !registry
                                    .interacting_qubits
                                    .as_ref()
                                    .unwrap()
                                    .contains(&candidate_qubit)
                            {
                                main_qubit = Some(candidate_qubit);
                                break;
                            }
                        }
                    }

                    main_qubit.unwrap()
                };
                allocated.insert(main_qubit);
                self.logical_circuit.alloc_aux_qubit(*aux_qubit, main_qubit);
            }
        }
    }

    pub fn gate(&mut self, gate: QuantumGate, target: LogicalQubit) -> Result<()> {
        if gate.is_identity() {
            return Ok(());
        }

        self.flatten_control_qubits();
        self.gate_checks(target)?;

        for qubit in self.ctrl_list.iter().chain([&target]) {
            self.clean_qubits.remove(qubit);
        }

        if !self.ctrl_list.is_empty() && self.configuration.qpu.is_some() {
            let mut schema = Schema::default();
            let interacting_qubits: Vec<_> =
                self.ctrl_list.iter().cloned().chain([target]).collect();

            for algorithm in gate.decomposition_list(self.ctrl_list.len()) {
                if !algorithm.need_aux() {
                    schema = Schema {
                        algorithm,
                        aux_qubits: None,
                    };
                    break;
                }

                if let Some(qubits) = self.try_alloc_aux(
                    algorithm.aux_needed(self.ctrl_list.len()),
                    if matches!(algorithm.aux_mode(), AuxMode::Dirty) {
                        Some(&interacting_qubits)
                    } else {
                        None
                    },
                ) {
                    schema = Schema {
                        algorithm,
                        aux_qubits: Some(qubits),
                    };
                    break;
                }
            }

            let registry: std::rc::Rc<std::cell::RefCell<Registry>> =
                std::rc::Rc::new(std::cell::RefCell::new(Registry {
                    algorithm: schema.algorithm,
                    aux_qubits: schema.aux_qubits.clone(),
                    interacting_qubits: if schema.algorithm.aux_mode() == AuxMode::Dirty {
                        Some(interacting_qubits)
                    } else {
                        None
                    },
                    ..Default::default()
                }));

            self.push_gate(GateInstruction::AuxRegistry(registry.clone()));

            for (gate, target, control) in gate.decompose(
                target,
                &self.ctrl_list,
                schema,
                self.configuration.qpu.as_ref().unwrap().u4_gate,
            ) {
                let control = control.map_or(vec![], |control| vec![control]);
                self.push_gate(GateInstruction::Gate {
                    gate,
                    target,
                    control,
                });
            }

            self.push_gate(GateInstruction::AuxRegistry(registry));
        } else {
            self.push_gate(GateInstruction::Gate {
                gate,
                target,
                control: self.ctrl_list.to_owned(),
            });
        }

        Ok(())
    }

    fn push_gate(&mut self, gate: GateInstruction) {
        if let Some(ajd_stack) = self.adj_stack.last_mut() {
            ajd_stack.push(gate);
        } else {
            match gate {
                GateInstruction::Gate {
                    gate,
                    target,
                    control,
                } => {
                    self.logical_circuit.gate(gate, target, &control);
                    if let Some(QuantumExecution::Live(execution)) =
                        self.configuration.execution.as_mut()
                    {
                        execution.gate(gate, target, &control);
                    }
                }
                GateInstruction::AuxRegistry(registry) => {
                    let mut registry = registry.borrow_mut();
                    match registry.state {
                        State::Begin => {
                            registry.num_u4 =
                                *self.logical_circuit.gate_count.entry(2).or_default();
                            registry.state = State::End;
                        }
                        State::End => {
                            *self
                                .decomposition_stats
                                .entry(registry.algorithm.to_string())
                                .or_default() +=
                                *self.logical_circuit.gate_count.entry(2).or_default()
                                    - registry.num_u4;
                            self.free_aux(&registry);
                        }
                    }
                }
            }
        }
    }

    pub fn global_phase(&mut self, angle: f64) -> Result<()> {
        self.adj_ctrl_checks(None)?;
        self.flatten_control_qubits();

        if self.ctrl_list.is_empty() {
            return Ok(());
        }

        let qubits = self.ctrl_list.clone();

        self.ctrl_begin()?;
        self.ctrl_push(&qubits[1..])?;
        self.gate(QuantumGate::Phase(angle), qubits[0])?;
        self.ctrl_pop()?;
        self.ctrl_end()?;
        Ok(())
    }

    pub fn measure(&mut self, qubits: &[LogicalQubit]) -> Result<usize> {
        self.non_gate_checks(Some(qubits), Some(self.configuration.measure))?;

        let index = self.measurements.len();

        self.logical_circuit.measure(qubits, index);

        self.measurements.push(
            if let Some(QuantumExecution::Live(execution)) = self.configuration.execution.as_mut() {
                Some(execution.measure(qubits))
            } else {
                None
            },
        );

        for qubit in qubits {
            self.qubit_measured.insert(*qubit, true);
        }

        if !matches!(self.configuration.measure, FeatureStatus::ValidAfter) {
            for qubit in qubits {
                self.qubit_valid.insert(*qubit, false);
            }
        }
        Ok(index)
    }

    pub fn sample(&mut self, qubits: &[LogicalQubit], shots: usize) -> Result<usize> {
        self.non_gate_checks(Some(qubits), Some(self.configuration.sample))?;

        let index = self.samples.len();

        self.logical_circuit.sample(qubits, shots, index);

        self.samples.push(
            if let Some(QuantumExecution::Live(execution)) = self.configuration.execution.as_mut() {
                Some(execution.sample(qubits, shots))
            } else {
                None
            },
        );

        if !matches!(self.configuration.sample, FeatureStatus::ValidAfter) {
            self.terminated = true;
            self.transpile();
        }

        Ok(index)
    }

    pub fn exp_value(&mut self, hamiltonian: Hamiltonian<LogicalQubit>) -> Result<usize> {
        let qubits = hamiltonian.qubits().cloned().collect::<Vec<_>>();
        self.non_gate_checks(Some(&qubits), Some(self.configuration.exp_value))?;

        let index = self.exp_values.len();

        self.exp_values.push(
            if let Some(QuantumExecution::Live(execution)) = self.configuration.execution.as_mut() {
                Some(execution.exp_value(&hamiltonian))
            } else {
                None
            },
        );

        self.logical_circuit.exp_value(hamiltonian, index);

        if !matches!(self.configuration.exp_value, FeatureStatus::ValidAfter) {
            self.terminated = true;
            self.transpile();
        }

        Ok(index)
    }

    pub fn dump(&mut self, qubits: &[LogicalQubit]) -> Result<usize> {
        self.non_gate_checks(Some(qubits), Some(self.configuration.dump))?;

        let index = self.dumps.len();

        self.logical_circuit.dump(qubits, index);

        self.dumps.push(
            if let Some(QuantumExecution::Live(execution)) = self.configuration.execution.as_mut() {
                Some(execution.dump(qubits))
            } else {
                None
            },
        );

        if !matches!(self.configuration.dump, FeatureStatus::ValidAfter) {
            self.terminated = true;
            self.transpile();
        }

        Ok(index)
    }

    pub fn transpile(&mut self) {
        self.terminated = true;

        if let (
            Some(QPU {
                coupling_graph: Some(coupling_graph),
                ..
            }),
            None,
        ) = (
            self.configuration.qpu.as_mut(),
            self.physical_circuit.as_ref(),
        ) {
            coupling_graph.calculate_distance();
        }

        if let (
            Some(QPU {
                coupling_graph: Some(coupling_graph),
                u4_gate,
                u2_gates,
            }),
            None,
        ) = (
            self.configuration.qpu.as_ref(),
            self.physical_circuit.as_ref(),
        ) {
            let mapping = mapping::allocation::initial(
                &self.logical_circuit.interaction_graph(),
                coupling_graph,
            );
            let mut physical_circuit =
                mapping::map::map_circuit(mapping, coupling_graph, &self.logical_circuit, *u4_gate);
            physical_circuit.gate_map(*u2_gates);
            self.physical_circuit = Some(physical_circuit);
        }
    }

    pub fn execute(&mut self) -> Result<()> {
        self.transpile();

        let mut results = None;

        if let Some(QuantumExecution::Batch(execution)) = self.configuration.execution.as_mut() {
            execution.submit_execution(
                &self.logical_circuit.instructions,
                self.physical_circuit
                    .as_ref()
                    .map(|circuit| circuit.instructions.as_ref()),
            );
            results = Some(execution.get_results());
        }

        if let Some(mut results) = results {
            if self.measurements.len() != results.measurements.len()
                || self.exp_values.len() != results.exp_values.len()
                || self.samples.len() != results.samples.len()
                || self.dumps.len() != results.dumps.len()
            {
                return Err(KetError::ResultDataMismatch);
            }

            results
                .measurements
                .drain(..)
                .zip(self.measurements.iter_mut())
                .for_each(|(result, measurement)| {
                    *measurement = Some(result);
                });

            results
                .exp_values
                .drain(..)
                .zip(self.exp_values.iter_mut())
                .for_each(|(result, exp_value)| {
                    *exp_value = Some(result);
                });

            results
                .samples
                .drain(..)
                .zip(self.samples.iter_mut())
                .for_each(|(result, sample)| {
                    assert_eq!(result.0.len(), result.1.len());
                    *sample = Some(result);
                });

            results
                .dumps
                .drain(..)
                .zip(self.dumps.iter_mut())
                .for_each(|(result, dump)| {
                    *dump = Some(result);
                });
        }
        Ok(())
    }

    pub fn get_measure(&self, index: usize) -> Option<u64> {
        self.measurements.get(index).copied().flatten()
    }

    pub fn get_sample(&self, index: usize) -> Option<&Sample> {
        self.samples.get(index).and_then(|s| s.as_ref())
    }

    pub fn get_exp_value(&self, index: usize) -> Option<f64> {
        self.exp_values.get(index).copied().flatten()
    }

    pub fn get_dump(&self, index: usize) -> Option<&DumpData> {
        self.dumps.get(index).and_then(|d| d.as_ref())
    }

    pub fn ctrl_push(&mut self, qubits: &[LogicalQubit]) -> Result<()> {
        self.flatten_control_qubits();
        self.adj_ctrl_checks(Some(qubits))?;
        self.ctrl_stack.last_mut().unwrap().push(qubits.to_owned());
        self.ctrl_list_is_valid = false;
        Ok(())
    }

    pub fn ctrl_pop(&mut self) -> Result<()> {
        self.ctrl_list_is_valid = false;

        if self.ctrl_stack.last_mut().unwrap().pop().is_none() {
            Err(KetError::ControlStackEmpty)
        } else {
            Ok(())
        }
    }

    pub fn adj_begin(&mut self) -> Result<()> {
        self.adj_ctrl_checks(None)?;
        self.adj_stack.push(vec![]);
        Ok(())
    }

    pub fn adj_end(&mut self) -> Result<()> {
        if let Some(mut gates) = self.adj_stack.pop() {
            while let Some(gate) = gates.pop() {
                self.push_gate(gate);
            }
            Ok(())
        } else {
            Err(KetError::InverseScopeEmpty)
        }
    }

    pub fn ctrl_begin(&mut self) -> Result<()> {
        self.adj_ctrl_checks(None)?;
        self.ctrl_stack.push(vec![]);
        self.ctrl_list_is_valid = false;
        Ok(())
    }

    pub fn ctrl_end(&mut self) -> Result<()> {
        self.adj_ctrl_checks(None)?;
        match self.ctrl_stack.pop() {
            Some(stack) => {
                if !stack.is_empty() {
                    Err(KetError::ControlStackNotEmpty)
                } else {
                    self.ctrl_list_is_valid = false;
                    if self.ctrl_stack.is_empty() {
                        Err(KetError::ControlStackRemovePrimary)
                    } else {
                        Ok(())
                    }
                }
            }
            None => Err(KetError::ControlStackRemovePrimary),
        }
    }

    pub fn instructions(&self) -> &[Instruction<LogicalQubit>] {
        &self.logical_circuit.instructions
    }

    pub fn instructions_json(&self) -> String {
        serde_json::to_string(&self.instructions()).unwrap()
    }

    pub fn isa_instructions(&self) -> Option<&[Instruction<PhysicalQubit>]> {
        self.physical_circuit
            .as_ref()
            .map(|c| c.instructions.as_ref())
    }

    pub fn isa_instructions_json(&self) -> String {
        serde_json::to_string(&self.isa_instructions()).unwrap()
    }

    pub fn metadata(&self) -> Metadata {
        Metadata {
            logical_gate_count: self.logical_circuit.gate_count.clone(),
            logical_circuit_depth: self.logical_circuit.depth(),
            physical_gate_count: self
                .physical_circuit
                .as_ref()
                .map(|circuit| circuit.gate_count.clone()),
            physical_circuit_depth: self
                .physical_circuit
                .as_ref()
                .map(|circuit| circuit.depth()),
            allocated_qubits: self.allocated_qubits,
            terminated: self.terminated,
            decomposition: self.decomposition_stats.clone(),
        }
    }
}
