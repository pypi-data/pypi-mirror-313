// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use crate::{
    execution::U4Gate,
    ir::{
        gate::{Matrix, QuantumGate},
        qubit::LogicalQubit,
    },
};

use super::{
    util::{exp_gate, zyz},
    Schema,
};

pub(crate) fn cu2(
    matrix: Matrix,
    control: LogicalQubit,
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    let (alpha, beta, gamma, delta) = zyz(matrix);

    let mut instructions = vec![
        (QuantumGate::Phase(alpha), control, None),
        (QuantumGate::RotationZ((delta - beta) / 2.0), target, None),
    ];
    instructions.extend(u4_gate.cnot(control, target));
    instructions.extend([
        (QuantumGate::RotationZ(-(delta + beta) / 2.0), target, None),
        (QuantumGate::RotationY(-gamma / 2.0), target, None),
    ]);
    instructions.extend(u4_gate.cnot(control, target));
    instructions.extend([
        (QuantumGate::RotationY(gamma / 2.0), target, None),
        (QuantumGate::RotationZ(beta), target, None),
    ]);

    instructions
}

pub(crate) fn mcu2_step(
    matrix: Matrix,
    qubits: &[LogicalQubit],
    first: bool,
    inverse: bool,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    let mut instructions = Vec::new();

    let start = if inverse { 1 } else { 0 };

    let mut qubit_pairs: Vec<(usize, usize)> = (0..qubits.len())
        .enumerate()
        .flat_map(|(i, t)| {
            if i > start {
                (start..i).map(|c| (c, t)).collect::<Vec<(usize, usize)>>()
            } else {
                vec![]
            }
        })
        .collect();

    qubit_pairs.sort_by_key(|(c, t)| c + t);
    if !inverse {
        qubit_pairs.reverse();
    }

    for (control, target) in qubit_pairs {
        let exponent: i32 = target as i32 - control as i32;
        let exponent = if control == 0 { exponent - 1 } else { exponent };
        let param = 2.0_f64.powi(exponent);
        let signal = control == 0 && !first;
        let signal = signal ^ inverse;
        if target == qubits.len() - 1 && first {
            let gate = exp_gate(matrix, 1.0 / param, signal);
            instructions.extend(cu2(gate, qubits[control], qubits[target], u4_gate));
        } else {
            instructions.extend(cu2(
                QuantumGate::RotationX(
                    std::f64::consts::PI * (if signal { -1.0 } else { 1.0 }) / param,
                )
                .matrix(),
                qubits[control],
                qubits[target],
                u4_gate,
            ));
        }
    }

    instructions
}

pub(crate) fn decompose(
    gate: QuantumGate,
    control: &[LogicalQubit],
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    let matrix = gate.matrix();
    let mut control_target = control.to_vec();
    control_target.push(target);

    let mut instruction = Vec::new();

    instruction.extend(mcu2_step(matrix, &control_target, true, false, u4_gate));
    instruction.extend(mcu2_step(matrix, &control_target, true, true, u4_gate));
    instruction.extend(mcu2_step(matrix, control, false, false, u4_gate));
    instruction.extend(mcu2_step(matrix, control, false, true, u4_gate));

    instruction
}

pub(crate) fn network(
    gate: QuantumGate,
    control: &[LogicalQubit],
    aux_qubit: &[LogicalQubit],
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    let mut instructions = Vec::new();

    instructions.extend(crate::decompose::x::c2x_pi4(
        false,
        false,
        control[0],
        control[1],
        aux_qubit[0],
        u4_gate,
    ));

    for i in 2..control.len() {
        instructions.extend(crate::decompose::x::c2x_pi4(
            false,
            false,
            control[i],
            aux_qubit[i - 2],
            aux_qubit[i - 1],
            u4_gate,
        ));
    }

    let half_instructions = instructions.clone();

    let schema = Schema {
        algorithm: match gate {
            QuantumGate::PauliX | QuantumGate::PauliY | QuantumGate::PauliZ => {
                super::Algorithm::Optimal
            }
            _ => super::Algorithm::CU2,
        },
        aux_qubits: None,
    };

    instructions.extend(gate.decompose(target, &[*aux_qubit.last().unwrap()], schema, u4_gate));

    instructions.extend(
        half_instructions
            .into_iter()
            .rev()
            .map(|(gate, target, control)| (gate.inverse(), target, control)),
    );

    instructions
}
