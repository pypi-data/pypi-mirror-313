// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use crate::{
    execution::U4Gate,
    ir::{gate::QuantumGate, qubit::LogicalQubit},
};

use super::{
    util::{eigen, zyz},
    x::v_chain_dirty,
};

pub(crate) fn decompose(
    gate: QuantumGate,
    control: &[LogicalQubit],
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    let (v, a) = if gate.is_minus_identity() {
        (vec![], QuantumGate::Hadamard)
    } else {
        let ((_, v1), (l2, v2)) = eigen(gate.su2_matrix());

        let (_, theta_0, theta_1, theta_2) = zyz([[v1.0, v2.0], [v1.1, v2.1]]);

        (
            vec![
                QuantumGate::RotationZ(theta_2),
                QuantumGate::RotationY(theta_1),
                QuantumGate::RotationZ(theta_0),
            ],
            QuantumGate::RotationZ(-2.0 * l2.powf(1.0 / 4.0).arg()),
        )
    };

    let mut instruction = Vec::new();

    instruction.append(
        &mut v
            .iter()
            .rev()
            .map(|gate| (gate.inverse(), target, None))
            .collect(),
    );

    let ctrl_0 = &control[..control.len() / 2];
    let ctrl_1 = &control[control.len() / 2..];

    for _ in 0..2 {
        instruction.extend(v_chain_dirty(ctrl_0, ctrl_1, target, u4_gate));
        instruction.push((a, target, None));
        instruction.extend(v_chain_dirty(ctrl_1, ctrl_0, target, u4_gate));
        instruction.push((a.inverse(), target, None));
    }

    instruction.extend(
        v.iter()
            .map(|gate| (*gate, target, None))
            .collect::<Vec<_>>(),
    );

    instruction
}
