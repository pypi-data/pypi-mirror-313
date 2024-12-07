// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use std::f64::consts::{FRAC_PI_2, FRAC_PI_4, FRAC_PI_8};

use crate::{
    execution::U4Gate,
    ir::{gate::QuantumGate, qubit::LogicalQubit},
};

use super::AuxMode;

pub(crate) fn c2x(
    control_0: LogicalQubit,
    control_1: LogicalQubit,
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    [(QuantumGate::Hadamard, target, None)]
        .into_iter()
        .chain(u4_gate.cnot(control_1, target))
        .chain([(QuantumGate::td(), target, None)])
        .chain(u4_gate.cnot(control_0, target))
        .chain([(QuantumGate::t(), target, None)])
        .chain(u4_gate.cnot(control_1, target))
        .chain([(QuantumGate::td(), target, None)])
        .chain(u4_gate.cnot(control_0, target))
        .chain([
            (QuantumGate::t(), control_1, None),
            (QuantumGate::t(), target, None),
        ])
        .chain(u4_gate.cnot(control_0, control_1))
        .chain([
            (QuantumGate::Hadamard, target, None),
            (QuantumGate::t(), control_0, None),
            (QuantumGate::td(), control_1, None),
        ])
        .chain(u4_gate.cnot(control_0, control_1))
        .collect()
}

pub(crate) fn c3x(
    control_0: LogicalQubit,
    control_1: LogicalQubit,
    control_2: LogicalQubit,
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    [
        (QuantumGate::Hadamard, target, None),
        (QuantumGate::sqrt_t(), control_0, None),
        (QuantumGate::sqrt_t(), control_1, None),
        (QuantumGate::sqrt_t(), control_2, None),
        (QuantumGate::sqrt_t(), target, None),
    ]
    .into_iter()
    .chain(u4_gate.cnot(control_0, control_1))
    .chain([(QuantumGate::sqrt_td(), control_1, None)])
    .chain(u4_gate.cnot(control_0, control_1))
    .chain(u4_gate.cnot(control_1, control_2))
    .chain([(QuantumGate::sqrt_td(), control_2, None)])
    .chain(u4_gate.cnot(control_0, control_2))
    .chain([(QuantumGate::sqrt_t(), control_2, None)])
    .chain(u4_gate.cnot(control_1, control_2))
    .chain([(QuantumGate::sqrt_td(), control_2, None)])
    .chain(u4_gate.cnot(control_0, control_2))
    .chain(u4_gate.cnot(control_2, target))
    .chain([(QuantumGate::sqrt_td(), target, None)])
    .chain(u4_gate.cnot(control_1, target))
    .chain([(QuantumGate::sqrt_t(), target, None)])
    .chain(u4_gate.cnot(control_2, target))
    .chain([(QuantumGate::sqrt_td(), target, None)])
    .chain(u4_gate.cnot(control_0, target))
    .chain([(QuantumGate::sqrt_t(), target, None)])
    .chain(u4_gate.cnot(control_2, target))
    .chain([(QuantumGate::sqrt_td(), target, None)])
    .chain(u4_gate.cnot(control_1, target))
    .chain([(QuantumGate::sqrt_t(), target, None)])
    .chain(u4_gate.cnot(control_2, target))
    .chain([(QuantumGate::sqrt_td(), target, None)])
    .chain(u4_gate.cnot(control_0, target))
    .chain([(QuantumGate::Hadamard, target, None)])
    .collect()
}

pub(crate) fn c4x(
    control_0: LogicalQubit,
    control_1: LogicalQubit,
    control_2: LogicalQubit,
    control_3: LogicalQubit,
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    [(QuantumGate::Hadamard, target, None)]
        .into_iter()
        .chain(cp(FRAC_PI_2, control_3, target, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(rc3x(control_0, control_1, control_2, control_3, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(cp(-FRAC_PI_2, control_3, target, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(
            rc3x(control_0, control_1, control_2, control_3, u4_gate)
                .into_iter()
                .rev()
                .map(|(gate, target, control)| (gate.inverse(), target, control))
                .collect::<Vec<_>>(),
        )
        .chain(c3sx(control_0, control_1, control_2, target, u4_gate))
        .collect()
}

fn cp(
    lambda: f64,
    control: LogicalQubit,
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    [(QuantumGate::Phase(lambda / 2.0), control, None)]
        .into_iter()
        .chain(u4_gate.cnot(control, target))
        .chain([(QuantumGate::Phase(-lambda / 2.0), target, None)])
        .chain(u4_gate.cnot(control, target))
        .chain([(QuantumGate::Phase(lambda / 2.0), target, None)])
        .collect()
}

fn c3sx(
    control_0: LogicalQubit,
    control_1: LogicalQubit,
    control_2: LogicalQubit,
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    [(QuantumGate::Hadamard, target, None)]
        .into_iter()
        .chain(cp(FRAC_PI_8, control_0, target, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(u4_gate.cnot(control_0, control_1))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(cp(-FRAC_PI_8, control_1, target, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(u4_gate.cnot(control_0, control_1))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(cp(FRAC_PI_8, control_1, target, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(u4_gate.cnot(control_1, control_2))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(cp(-FRAC_PI_8, control_2, target, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(u4_gate.cnot(control_0, control_2))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(cp(FRAC_PI_8, control_2, target, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(u4_gate.cnot(control_1, control_2))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(cp(-FRAC_PI_8, control_2, target, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(u4_gate.cnot(control_0, control_2))
        .chain([(QuantumGate::Hadamard, target, None)])
        .chain(cp(FRAC_PI_8, control_2, target, u4_gate))
        .chain([(QuantumGate::Hadamard, target, None)])
        .collect()
}

fn rc3x(
    control_0: LogicalQubit,
    control_1: LogicalQubit,
    control_2: LogicalQubit,
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    [
        (QuantumGate::Hadamard, target, None),
        (QuantumGate::t(), target, None),
    ]
    .into_iter()
    .chain(u4_gate.cnot(control_2, target))
    .chain([
        (QuantumGate::td(), target, None),
        (QuantumGate::Hadamard, target, None),
    ])
    .chain(u4_gate.cnot(control_0, target))
    .chain([(QuantumGate::t(), target, None)])
    .chain(u4_gate.cnot(control_1, target))
    .chain([(QuantumGate::td(), target, None)])
    .chain(u4_gate.cnot(control_0, target))
    .chain([(QuantumGate::t(), target, None)])
    .chain(u4_gate.cnot(control_1, target))
    .chain([
        (QuantumGate::td(), target, None),
        (QuantumGate::Hadamard, target, None),
        (QuantumGate::t(), target, None),
    ])
    .chain(u4_gate.cnot(control_2, target))
    .chain([
        (QuantumGate::td(), target, None),
        (QuantumGate::Hadamard, target, None),
    ])
    .collect()
}

pub(crate) fn c2x_pi4(
    cancel_right: bool,
    cancel_left: bool,
    control_0: LogicalQubit,
    control_1: LogicalQubit,
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    let mut instructions = Vec::new();

    if !cancel_left {
        instructions.push((QuantumGate::RotationY(-FRAC_PI_4), target, None));
        instructions.extend(u4_gate.cnot(control_0, target));
        instructions.push((QuantumGate::RotationY(-FRAC_PI_4), target, None));
    }

    instructions.extend(u4_gate.cnot(control_1, target));

    if !cancel_right {
        instructions.push((QuantumGate::RotationY(FRAC_PI_4), target, None));
        instructions.extend(u4_gate.cnot(control_0, target));
        instructions.push((QuantumGate::RotationY(FRAC_PI_4), target, None));
    }
    instructions
}

fn mcx_n_action(
    control: &[LogicalQubit],
    aux_control: &[LogicalQubit],
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    let mut instructions = c2x(
        control[control.len() - 1],
        aux_control[aux_control.len() - 1],
        target,
        u4_gate,
    );

    for i in 1..aux_control.len() {
        instructions.extend(c2x_pi4(
            true,
            false,
            control[control.len() - i - 1],
            aux_control[aux_control.len() - i - 1],
            aux_control[aux_control.len() - i],
            u4_gate,
        ));
    }

    instructions.extend(c2x_pi4(
        false,
        false,
        control[0],
        control[1],
        aux_control[0],
        u4_gate,
    ));

    instructions
}

pub(crate) fn v_chain_dirty(
    control: &[LogicalQubit],
    aux_qubit: &[LogicalQubit],
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    if control.len() == 1 {
        return u4_gate.cnot(control[0], target);
    } else if control.len() == 2 {
        return c2x(control[0], control[1], target, u4_gate);
    }

    let num_aux = control.len() - 2;
    let aux_control = &aux_qubit[..num_aux];

    let mut instructions = Vec::new();

    for _ in 0..2 {
        instructions.extend(mcx_n_action(control, aux_control, target, u4_gate));

        for i in 0..num_aux - 1 {
            instructions.extend(c2x_pi4(
                false,
                true,
                control[2 + i],
                aux_control[i],
                aux_control[i + 1],
                u4_gate,
            ));
        }
    }

    instructions
}

pub(crate) fn v_chain_clean(
    control: &[LogicalQubit],
    aux_qubit: &[LogicalQubit],
    target: LogicalQubit,
    u4_gate: U4Gate,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    if control.len() == 1 {
        return u4_gate.cnot(control[0], target);
    } else if control.len() == 2 {
        return c2x(control[0], control[1], target, u4_gate);
    }

    let num_aux = control.len() - 2;
    let aux_control = &aux_qubit[..num_aux];

    let mut instructions = Vec::new();

    let mut half_instructions =
        c2x_pi4(false, false, control[0], control[1], aux_qubit[0], u4_gate);

    for i in 0..num_aux - 1 {
        half_instructions.extend(c2x_pi4(
            false,
            false,
            control[2 + i],
            aux_control[i],
            aux_control[i + 1],
            u4_gate,
        ));
    }

    instructions.extend(half_instructions.iter());
    instructions.extend(c2x(
        *control.last().unwrap(),
        *aux_control.last().unwrap(),
        target,
        u4_gate,
    ));
    instructions.extend(
        half_instructions
            .into_iter()
            .rev()
            .map(|(gate, target, control)| (gate.inverse(), target, control)),
    );

    instructions
}

pub(crate) fn mxc_1_aux(
    control: &[LogicalQubit],
    aux_qubit: LogicalQubit,
    target: LogicalQubit,
    u4_gate: U4Gate,
    aux_mode: AuxMode,
) -> Vec<(QuantumGate, LogicalQubit, Option<LogicalQubit>)> {
    let control_size = control.len();
    let ctrl_0 = &control[..control_size / 2];
    let ctrl_1 = control[control_size / 2..]
        .iter()
        .cloned()
        .chain([aux_qubit])
        .collect::<Vec<_>>();

    v_chain_dirty(ctrl_0, &ctrl_1, aux_qubit, u4_gate)
        .into_iter()
        .chain(v_chain_dirty(&ctrl_1, ctrl_0, target, u4_gate))
        .chain(v_chain_dirty(ctrl_0, &ctrl_1, aux_qubit, u4_gate))
        .chain(if matches!(aux_mode, AuxMode::Dirty) {
            v_chain_dirty(&ctrl_1, ctrl_0, target, u4_gate)
        } else {
            vec![]
        })
        .collect()
}
