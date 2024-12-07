use std::vec;

use log::debug;

// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0
use crate::{decomposition::util, Angle, Instruction, QuantumGate, U4GateType};

use super::x::mcx_dirty;

pub fn decompose(
    gate: QuantumGate,
    control: &[usize],
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    debug!(
        "Performing SU2 decomposition: gate={:?}; target={}; control={:?}",
        gate, target, control
    );

    let (v, a) = if gate.is_minus_identity() {
        (vec![], QuantumGate::Hadamard)
    } else {
        let ((_, v1), (l2, v2)) = util::eigen(gate.su2_matrix());

        let (_, theta_0, theta_1, theta_2) = util::zyz([[v1.0, v2.0], [v1.1, v2.1]]);

        (
            vec![
                QuantumGate::RotationZ(crate::Angle::Scalar(theta_2)),
                QuantumGate::RotationY(crate::Angle::Scalar(theta_1)),
                QuantumGate::RotationZ(crate::Angle::Scalar(theta_0)),
            ],
            QuantumGate::RotationZ(Angle::Scalar(-2.0 * l2.powf(1.0 / 4.0).arg())),
        )
    };

    let mut instruction = Vec::new();

    instruction.append(
        &mut v
            .iter()
            .rev()
            .map(|gate| Instruction::Gate {
                gate: gate.inverse(),
                target,
                control: vec![],
            })
            .collect(),
    );

    let ctrl_0 = &control[..control.len() / 2];
    let ctrl_1 = &control[control.len() / 2..];

    for _ in 0..2 {
        instruction.extend(mcx_dirty(ctrl_0, ctrl_1, target, u4_gate_type));
        instruction.push(Instruction::Gate {
            gate: a.clone(),
            target,
            control: vec![],
        });

        instruction.extend(mcx_dirty(ctrl_1, ctrl_0, target, u4_gate_type));

        instruction.push(Instruction::Gate {
            gate: a.inverse(),
            target,
            control: vec![],
        });
    }

    instruction.append(
        &mut v
            .iter()
            .map(|gate| Instruction::Gate {
                gate: gate.clone(),
                target,
                control: vec![],
            })
            .collect(),
    );

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
        p.apply_gate(
            QuantumGate::RotationZ(Angle::PiFraction { numer: 1, denom: 1 }),
            trt_qubit,
        )
        .unwrap();
        p.ctrl_pop().unwrap();

        println!("{:#?}", p.circuit.instructions)
    }
}
