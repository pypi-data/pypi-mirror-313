// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use crate::decomposition::util;
use crate::ir::Matrix;
use crate::{Instruction, QuantumGate, U4GateType};
use log::debug;
use num::complex::ComplexFloat;

use super::util::decompose_c1u2;

pub fn dec_u2_step(
    matrix: Matrix,
    qubits: &[usize],
    first: bool,
    inverse: bool,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
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
        let param = 2.0.powi(exponent);
        let signal = control == 0 && !first;
        let signal = signal ^ inverse;
        if target == qubits.len() - 1 && first {
            let gate = util::exp_gate(matrix, 1.0 / param, signal);
            instructions.extend(decompose_c1u2(
                gate,
                qubits[control],
                qubits[target],
                u4_gate_type,
            ));
        } else {
            instructions.extend(decompose_c1u2(
                QuantumGate::RotationX(crate::Angle::Scalar(
                    std::f64::consts::PI * (if signal { -1.0 } else { 1.0 }) / param,
                ))
                .matrix(),
                qubits[control],
                qubits[target],
                u4_gate_type,
            ));
        }
    }

    instructions
}

pub fn decompose(
    gate: QuantumGate,
    control: &[usize],
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    debug!(
        "Performing U2 decomposition: gate={:?}; target={}; control={:?}",
        gate, target, control
    );

    let matrix = gate.matrix();
    let mut control_target = control.to_vec();
    control_target.push(target);

    let mut instruction = Vec::new();

    instruction.extend(dec_u2_step(
        matrix,
        &control_target,
        true,
        false,
        u4_gate_type,
    ));
    instruction.extend(dec_u2_step(
        matrix,
        &control_target,
        true,
        true,
        u4_gate_type,
    ));
    instruction.extend(dec_u2_step(matrix, control, false, false, u4_gate_type));
    instruction.extend(dec_u2_step(matrix, control, false, true, u4_gate_type));

    instruction
}

#[cfg(test)]
mod tests {
    use crate::{Configuration, Process};

    use super::*;

    #[test]
    fn print_decomposition() {
        let config = Configuration::new(100, Some(Default::default()));
        let mut p = Process::new(config);

        let n = 3;

        let trt_qubit = p.allocate_qubit().unwrap();
        let ctr_qubits: Vec<usize> = (0..n - 1).map(|_| p.allocate_qubit().unwrap()).collect();

        p.ctrl_push(&ctr_qubits).unwrap();
        p.apply_gate(QuantumGate::PauliY, trt_qubit).unwrap();
        p.ctrl_pop().unwrap();

        println!("{:#?}", p.circuit.instructions)
    }
}
