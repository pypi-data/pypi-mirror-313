// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use super::qubit::LogicalQubit;
use crate::{
    decompose::{self, Algorithm, AuxMode, Schema},
    execution::U4Gate,
};
use num::Complex;
use serde::{Deserialize, Serialize};
use std::f64::consts::{FRAC_1_SQRT_2, FRAC_PI_2, FRAC_PI_4, FRAC_PI_8, PI};

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum QuantumGate {
    PauliX,
    PauliY,
    PauliZ,
    RotationX(f64),
    RotationY(f64),
    RotationZ(f64),
    Phase(f64),
    Hadamard,
}

pub type Cf64 = Complex<f64>;
pub type Matrix = [[Cf64; 2]; 2];

impl QuantumGate {
    pub fn s() -> Self {
        Self::Phase(FRAC_PI_2)
    }

    pub fn sd() -> Self {
        Self::Phase(-FRAC_PI_2)
    }

    pub fn t() -> Self {
        Self::Phase(FRAC_PI_4)
    }

    pub fn td() -> Self {
        Self::Phase(-FRAC_PI_4)
    }

    pub fn sqrt_t() -> Self {
        Self::Phase(FRAC_PI_8)
    }

    pub fn sqrt_td() -> Self {
        Self::Phase(-FRAC_PI_8)
    }

    pub(crate) fn is_identity(&self) -> bool {
        let (angle, n) = match self {
            QuantumGate::RotationX(angle) => (angle, 4.0),
            QuantumGate::RotationY(angle) => (angle, 4.0),
            QuantumGate::RotationZ(angle) => (angle, 4.0),
            QuantumGate::Phase(angle) => (angle, 2.0),
            _ => return false,
        };

        (angle % (n * PI)).abs() < 1e-14
    }

    pub(crate) fn is_minus_identity(&self) -> bool {
        let angle = match self {
            QuantumGate::RotationX(angle) => angle,
            QuantumGate::RotationY(angle) => angle,
            QuantumGate::RotationZ(angle) => angle,
            _ => return false,
        };

        (angle % (2.0 * PI)).abs() < 1e-14
    }

    pub(crate) fn is_inverse(&self, other: &Self) -> bool {
        match self {
            QuantumGate::PauliX => matches!(other, QuantumGate::PauliX),
            QuantumGate::PauliY => matches!(other, QuantumGate::PauliY),
            QuantumGate::PauliZ => matches!(other, QuantumGate::PauliZ),
            QuantumGate::RotationX(angle) => {
                if let QuantumGate::RotationX(other) = other {
                    QuantumGate::RotationX(angle + other).is_identity()
                } else {
                    false
                }
            }
            QuantumGate::RotationY(angle) => {
                if let QuantumGate::RotationY(other) = other {
                    QuantumGate::RotationY(angle + other).is_identity()
                } else {
                    false
                }
            }
            QuantumGate::RotationZ(angle) => {
                if let QuantumGate::RotationZ(other) = other {
                    QuantumGate::RotationZ(angle + other).is_identity()
                } else {
                    false
                }
            }
            QuantumGate::Phase(angle) => {
                if let QuantumGate::Phase(other) = other {
                    QuantumGate::Phase(angle + other).is_identity()
                } else {
                    false
                }
            }
            QuantumGate::Hadamard => matches!(other, QuantumGate::Hadamard),
        }
    }

    pub(crate) fn matrix(&self) -> Matrix {
        match self {
            QuantumGate::PauliX => [[0.0.into(), 1.0.into()], [1.0.into(), 0.0.into()]],
            QuantumGate::PauliY => [[0.0.into(), -Cf64::i()], [Cf64::i(), 0.0.into()]],
            QuantumGate::PauliZ => [[1.0.into(), 0.0.into()], [0.0.into(), (-1.0).into()]],
            QuantumGate::RotationX(angle) => [
                [(angle / 2.0).cos().into(), -Cf64::i() * (angle / 2.0).sin()],
                [-Cf64::i() * (angle / 2.0).sin(), (angle / 2.0).cos().into()],
            ],
            QuantumGate::RotationY(angle) => [
                [(angle / 2.0).cos().into(), (-(angle / 2.0).sin()).into()],
                [(angle / 2.0).sin().into(), (angle / 2.0).cos().into()],
            ],
            QuantumGate::RotationZ(angle) => [
                [(-Cf64::i() * (angle / 2.0)).exp(), 0.0.into()],
                [0.0.into(), (Cf64::i() * (angle / 2.0)).exp()],
            ],
            QuantumGate::Phase(angle) => [
                [1.0.into(), 0.0.into()],
                [0.0.into(), (Cf64::i() * angle).exp()],
            ],
            QuantumGate::Hadamard => [
                [(1.0 / 2.0f64.sqrt()).into(), (1.0 / 2.0f64.sqrt()).into()],
                [(1.0 / 2.0f64.sqrt()).into(), (-1.0 / 2.0f64.sqrt()).into()],
            ],
        }
    }

    pub(crate) fn su2_matrix(&self) -> Matrix {
        match self {
            QuantumGate::PauliX => QuantumGate::RotationX(PI).matrix(),
            QuantumGate::PauliY => QuantumGate::RotationY(PI).matrix(),
            QuantumGate::PauliZ => QuantumGate::RotationZ(PI).matrix(),
            QuantumGate::Phase(angle) => QuantumGate::RotationZ(*angle).matrix(),
            QuantumGate::Hadamard => [
                [-Cf64::i() * FRAC_1_SQRT_2, -Cf64::i() * FRAC_1_SQRT_2],
                [-Cf64::i() * FRAC_1_SQRT_2, Cf64::i() * FRAC_1_SQRT_2],
            ],
            _ => self.matrix(),
        }
    }

    pub(crate) fn su2_phase(&self) -> f64 {
        match self {
            QuantumGate::PauliX => FRAC_PI_2,
            QuantumGate::PauliY => FRAC_PI_2,
            QuantumGate::PauliZ => FRAC_PI_2,
            QuantumGate::Phase(angle) => angle / 2.0,
            QuantumGate::Hadamard => FRAC_PI_2,
            _ => 0.0,
        }
    }

    pub(crate) fn inverse(&self) -> Self {
        match self {
            QuantumGate::PauliX => QuantumGate::PauliX,
            QuantumGate::PauliY => QuantumGate::PauliY,
            QuantumGate::PauliZ => QuantumGate::PauliZ,
            QuantumGate::RotationX(angle) => QuantumGate::RotationX(-angle),
            QuantumGate::RotationY(angle) => QuantumGate::RotationY(-angle),
            QuantumGate::RotationZ(angle) => QuantumGate::RotationZ(-angle),
            QuantumGate::Phase(angle) => QuantumGate::Phase(-angle),
            QuantumGate::Hadamard => QuantumGate::Hadamard,
        }
    }

    pub(crate) fn decomposition_list(&self, control_size: usize) -> Vec<Algorithm> {
        match self {
            QuantumGate::PauliX | QuantumGate::PauliY | QuantumGate::PauliZ => {
                if control_size <= 3 {
                    vec![Algorithm::Optimal]
                } else if control_size == 4 {
                    vec![
                        Algorithm::VChain(AuxMode::Clean),
                        Algorithm::VChain(AuxMode::Dirty),
                        Algorithm::Optimal,
                    ]
                } else {
                    vec![
                        Algorithm::VChain(AuxMode::Clean),
                        Algorithm::VChain(AuxMode::Dirty),
                        Algorithm::SingleAux(AuxMode::Clean),
                        Algorithm::SingleAux(AuxMode::Dirty),
                        Algorithm::LinearDepth,
                    ]
                }
            }
            QuantumGate::RotationX(_) | QuantumGate::RotationY(_) | QuantumGate::RotationZ(_) => {
                if control_size > 1 {
                    vec![Algorithm::Network, Algorithm::SU2]
                } else {
                    vec![Algorithm::CU2]
                }
            }
            QuantumGate::Phase(_) | QuantumGate::Hadamard => {
                if control_size > 1 {
                    vec![
                        Algorithm::Network,
                        Algorithm::SU2Rewrite,
                        Algorithm::LinearDepth,
                    ]
                } else {
                    vec![Algorithm::CU2]
                }
            }
        }
    }

    pub(crate) fn decompose(
        &self,
        target: LogicalQubit,
        control: &[LogicalQubit],
        schema: Schema,
        u4_gate: U4Gate,
    ) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
        match self {
            QuantumGate::PauliX => Self::decompose_x(target, control, schema, u4_gate),
            QuantumGate::PauliY => Self::decompose_y(target, control, schema, u4_gate),
            QuantumGate::PauliZ => Self::decompose_z(target, control, schema, u4_gate),
            QuantumGate::RotationX(_) | QuantumGate::RotationY(_) | QuantumGate::RotationZ(_) => {
                self.decompose_r(target, control, schema, u4_gate)
            }
            QuantumGate::Phase(angle) => {
                Self::decompose_phase(*angle, target, control, schema, u4_gate)
            }
            QuantumGate::Hadamard => Self::decompose_hadamard(target, control, schema, u4_gate),
        }
    }

    fn decompose_r(
        &self,
        target: LogicalQubit,
        control: &[LogicalQubit],
        schema: Schema,
        u4_gate: U4Gate,
    ) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
        match &schema.algorithm {
            Algorithm::Network => {
                decompose::u2::network(*self, control, &schema.aux_qubits.unwrap(), target, u4_gate)
            }
            Algorithm::SU2 => decompose::su2::decompose(*self, control, target, u4_gate),
            Algorithm::CU2 => decompose::u2::cu2(self.matrix(), control[0], target, u4_gate),
            _ => panic!("Invalid Decomposition for Rotation Gate"),
        }
    }

    fn decompose_x(
        target: LogicalQubit,
        control: &[LogicalQubit],
        schema: Schema,
        u4_gate: U4Gate,
    ) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
        match &schema.algorithm {
            Algorithm::VChain(aux_mode) => match aux_mode {
                AuxMode::Clean => decompose::x::v_chain_clean(
                    control,
                    &schema.aux_qubits.unwrap(),
                    target,
                    u4_gate,
                ),
                AuxMode::Dirty => decompose::x::v_chain_dirty(
                    control,
                    &schema.aux_qubits.unwrap(),
                    target,
                    u4_gate,
                ),
            },
            Algorithm::SingleAux(aux_mode) => decompose::x::mxc_1_aux(
                control,
                schema.aux_qubits.unwrap()[0],
                target,
                u4_gate,
                *aux_mode,
            ),
            Algorithm::LinearDepth => {
                decompose::u2::decompose(QuantumGate::PauliX, control, target, u4_gate)
            }
            Algorithm::Optimal => match control.len() {
                1 => u4_gate.cnot(control[0], target),
                2 => decompose::x::c2x(control[0], control[1], target, u4_gate),
                3 => decompose::x::c3x(control[0], control[1], control[2], target, u4_gate),
                _ => decompose::x::c4x(
                    control[0], control[1], control[2], control[3], target, u4_gate,
                ),
            },
            _ => panic!("Invalid Decomposition for Pauli Gate"),
        }
    }

    fn decompose_y(
        target: LogicalQubit,
        control: &[LogicalQubit],
        schema: Schema,
        u4_gate: U4Gate,
    ) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
        [
            (QuantumGate::sd(), target, None),
            (QuantumGate::Hadamard, target, None),
        ]
        .into_iter()
        .chain(Self::decompose_x(target, control, schema, u4_gate))
        .chain([
            (QuantumGate::Hadamard, target, None),
            (QuantumGate::s(), target, None),
        ])
        .collect()
    }

    fn decompose_z(
        target: LogicalQubit,
        control: &[LogicalQubit],
        schema: Schema,
        u4_gate: U4Gate,
    ) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
        [(QuantumGate::Hadamard, target, None)]
            .into_iter()
            .chain(Self::decompose_x(target, control, schema, u4_gate))
            .chain([(QuantumGate::Hadamard, target, None)])
            .collect()
    }

    fn decompose_phase(
        angle: f64,
        target: LogicalQubit,
        control: &[LogicalQubit],
        schema: Schema,
        u4_gate: U4Gate,
    ) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
        match &schema.algorithm {
            Algorithm::LinearDepth => {
                decompose::u2::decompose(Self::Phase(angle), control, target, u4_gate)
            }
            Algorithm::Network => decompose::u2::network(
                Self::Phase(angle),
                control,
                &schema.aux_qubits.unwrap(),
                target,
                u4_gate,
            ),
            Algorithm::SU2Rewrite => {
                let control: Vec<_> = control.iter().cloned().chain([target]).collect();
                decompose::su2::decompose(
                    QuantumGate::RotationZ(-2.0 * angle),
                    &control,
                    schema.aux_qubits.unwrap()[0],
                    u4_gate,
                )
            }
            Algorithm::CU2 => decompose::u2::cu2(
                QuantumGate::Phase(angle).matrix(),
                control[0],
                target,
                u4_gate,
            ),
            _ => panic!("Invalid Decomposition for Phase Gate"),
        }
    }

    fn decompose_hadamard(
        target: LogicalQubit,
        control: &[LogicalQubit],
        schema: Schema,
        u4_gate: U4Gate,
    ) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
        match &schema.algorithm {
            Algorithm::LinearDepth => {
                decompose::u2::decompose(Self::Hadamard, control, target, u4_gate)
            }
            Algorithm::Network => decompose::u2::network(
                Self::Hadamard,
                control,
                &schema.aux_qubits.unwrap(),
                target,
                u4_gate,
            ),
            Algorithm::SU2Rewrite => {
                let phase = QuantumGate::Hadamard.su2_phase();

                decompose::su2::decompose(QuantumGate::Hadamard, control, target, u4_gate)
                    .into_iter()
                    .chain(decompose::su2::decompose(
                        QuantumGate::RotationZ(-2.0 * phase),
                        control,
                        schema.aux_qubits.unwrap()[0],
                        u4_gate,
                    ))
                    .collect()
            }
            Algorithm::CU2 => {
                decompose::u2::cu2(QuantumGate::Hadamard.matrix(), control[0], target, u4_gate)
            }
            _ => panic!("Invalid Decomposition for Hadamard Gate"),
        }
    }
}

pub(crate) fn matrix_dot(matrix_a: &Matrix, matrix_b: &Matrix) -> Matrix {
    [
        [
            matrix_a[0][0] * matrix_b[0][0] + matrix_a[0][1] * matrix_b[1][0],
            matrix_a[0][0] * matrix_b[0][1] + matrix_a[0][1] * matrix_b[1][1],
        ],
        [
            matrix_a[1][0] * matrix_b[0][0] + matrix_a[1][1] * matrix_b[1][0],
            matrix_a[1][0] * matrix_b[0][1] + matrix_a[1][1] * matrix_b[1][1],
        ],
    ]
}
