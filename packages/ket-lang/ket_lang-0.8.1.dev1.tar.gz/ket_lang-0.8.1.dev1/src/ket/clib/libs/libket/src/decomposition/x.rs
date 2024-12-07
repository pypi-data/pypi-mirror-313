// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0
use crate::{Angle, Instruction, QuantumGate, U4GateType};
use log::debug;

fn toffoli(
    control_0: usize,
    control_1: usize,
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    [Instruction::Gate {
        // H(t)
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }]
    .into_iter()
    .chain(u4_gate_type.cnot(control_1, target))
    .chain([Instruction::Gate {
        // TD(t)
        gate: QuantumGate::Phase(Angle::PiFraction {
            numer: -1,
            denom: 4,
        }),
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_0, target))
    .chain([Instruction::Gate {
        // T(t)
        gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 4 }),
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_1, target))
    .chain([Instruction::Gate {
        // TD(target)
        gate: QuantumGate::Phase(Angle::PiFraction {
            numer: -1,
            denom: 4,
        }),
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_0, target))
    .chain([
        Instruction::Gate {
            // T(c1)
            gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 4 }),
            target: control_1,
            control: vec![],
        },
        Instruction::Gate {
            // T(t)
            gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 4 }),
            target,
            control: vec![],
        },
    ])
    .chain(u4_gate_type.cnot(control_0, control_1))
    .chain([
        Instruction::Gate {
            // H(t)
            gate: QuantumGate::Hadamard,
            target,
            control: vec![],
        },
        Instruction::Gate {
            // T(c0)
            gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 4 }),
            target: control_0,
            control: vec![],
        },
        Instruction::Gate {
            // TD(c1)
            gate: QuantumGate::Phase(Angle::PiFraction {
                numer: -1,
                denom: 4,
            }),
            target: control_1,
            control: vec![],
        },
    ])
    .chain(u4_gate_type.cnot(control_0, control_1))
    .collect()
}

fn toffoli_pi4(
    cancel_right: bool,
    cancel_left: bool,
    control_0: usize,
    control_1: usize,
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    let mut instructions = Vec::new();

    if !cancel_left {
        instructions.push(Instruction::Gate {
            gate: QuantumGate::RotationY(Angle::PiFraction {
                numer: -1,
                denom: 4,
            }),
            target,
            control: vec![],
        });

        instructions.extend(u4_gate_type.cnot(target, control_0));

        instructions.push(Instruction::Gate {
            gate: QuantumGate::RotationY(Angle::PiFraction {
                numer: -1,
                denom: 4,
            }),
            target,
            control: vec![],
        });
    }

    instructions.extend(u4_gate_type.cnot(control_1, target));

    if !cancel_right {
        instructions.push(Instruction::Gate {
            gate: QuantumGate::RotationY(Angle::PiFraction { numer: 1, denom: 4 }),
            target,
            control: vec![],
        });

        instructions.extend(u4_gate_type.cnot(target, control_0));

        instructions.push(Instruction::Gate {
            gate: QuantumGate::RotationY(Angle::PiFraction { numer: 1, denom: 4 }),
            target,
            control: vec![],
        });
    }
    instructions
}

pub fn c3x(
    control_0: usize,
    control_1: usize,
    control_2: usize,
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    [
        Instruction::Gate {
            gate: QuantumGate::Hadamard,
            target,
            control: vec![],
        },
        Instruction::Gate {
            gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 8 }),
            target: control_0,
            control: vec![],
        },
        Instruction::Gate {
            gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 8 }),
            target: control_1,
            control: vec![],
        },
        Instruction::Gate {
            gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 8 }),
            target: control_2,
            control: vec![],
        },
        Instruction::Gate {
            gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 8 }),
            target,
            control: vec![],
        },
    ]
    .into_iter()
    .chain(u4_gate_type.cnot(control_0, control_1))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction {
            numer: -1,
            denom: 8,
        }),
        control: vec![],
        target: control_1,
    }])
    .chain(u4_gate_type.cnot(control_0, control_1))
    .chain(u4_gate_type.cnot(control_1, control_2))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction {
            numer: -1,
            denom: 8,
        }),
        control: vec![],
        target: control_2,
    }])
    .chain(u4_gate_type.cnot(control_0, control_2))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 8 }),
        control: vec![],
        target: control_2,
    }])
    .chain(u4_gate_type.cnot(control_1, control_2))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction {
            numer: -1,
            denom: 8,
        }),
        control: vec![],
        target: control_2,
    }])
    .chain(u4_gate_type.cnot(control_0, control_2))
    .chain(u4_gate_type.cnot(control_2, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction {
            numer: -1,
            denom: 8,
        }),
        control: vec![],
        target,
    }])
    .chain(u4_gate_type.cnot(control_1, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 8 }),
        control: vec![],
        target,
    }])
    .chain(u4_gate_type.cnot(control_2, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction {
            numer: -1,
            denom: 8,
        }),
        control: vec![],
        target,
    }])
    .chain(u4_gate_type.cnot(control_0, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 8 }),
        control: vec![],
        target,
    }])
    .chain(u4_gate_type.cnot(control_2, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction {
            numer: -1,
            denom: 8,
        }),
        control: vec![],
        target,
    }])
    .chain(u4_gate_type.cnot(control_1, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction { numer: 1, denom: 8 }),
        control: vec![],
        target,
    }])
    .chain(u4_gate_type.cnot(control_2, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::PiFraction {
            numer: -1,
            denom: 8,
        }),
        control: vec![],
        target,
    }])
    .chain(u4_gate_type.cnot(control_0, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .collect()
}

fn cp(lambda: f64, control: usize, target: usize, u4_gate_type: U4GateType) -> Vec<Instruction> {
    [Instruction::Gate {
        gate: QuantumGate::Phase(Angle::Scalar(lambda / 2.0)),
        target: control,
        control: vec![],
    }]
    .into_iter()
    .chain(u4_gate_type.cnot(control, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::Scalar(-lambda / 2.0)),
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::Scalar(lambda / 2.0)),
        target,
        control: vec![],
    }])
    .collect()
}

fn c3sx(
    control_0: usize,
    control_1: usize,
    control_2: usize,
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    [Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }]
    .into_iter()
    .chain(cp(
        std::f64::consts::PI / 8.0,
        control_0,
        target,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_0, control_1))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(cp(
        -std::f64::consts::PI / 8.0,
        control_1,
        target,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_0, control_1))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(cp(
        std::f64::consts::PI / 8.0,
        control_1,
        target,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_1, control_2))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(cp(
        -std::f64::consts::PI / 8.0,
        control_2,
        target,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_0, control_2))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(cp(
        std::f64::consts::PI / 8.0,
        control_2,
        target,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_1, control_2))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(cp(
        -std::f64::consts::PI / 8.0,
        control_2,
        target,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_0, control_2))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(cp(
        std::f64::consts::PI / 8.0,
        control_2,
        target,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .collect()
}

fn rc3x(
    control_0: usize,
    control_1: usize,
    control_2: usize,
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    [
        Instruction::Gate {
            gate: QuantumGate::Hadamard,
            target,
            control: vec![],
        },
        Instruction::Gate {
            gate: QuantumGate::Phase(Angle::Scalar(std::f64::consts::PI / 4.0)),
            target,
            control: vec![],
        },
    ]
    .into_iter()
    .chain(u4_gate_type.cnot(control_2, target))
    .chain([
        Instruction::Gate {
            gate: QuantumGate::Phase(Angle::Scalar(-std::f64::consts::PI / 4.0)),
            target,
            control: vec![],
        },
        Instruction::Gate {
            gate: QuantumGate::Hadamard,
            target,
            control: vec![],
        },
    ])
    .chain(u4_gate_type.cnot(control_0, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::Scalar(std::f64::consts::PI / 4.0)),
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_1, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::Scalar(-std::f64::consts::PI / 4.0)),
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_0, target))
    .chain([Instruction::Gate {
        gate: QuantumGate::Phase(Angle::Scalar(std::f64::consts::PI / 4.0)),
        target,
        control: vec![],
    }])
    .chain(u4_gate_type.cnot(control_1, target))
    .chain([
        Instruction::Gate {
            gate: QuantumGate::Phase(Angle::Scalar(-std::f64::consts::PI / 4.0)),
            target,
            control: vec![],
        },
        Instruction::Gate {
            gate: QuantumGate::Hadamard,
            target,
            control: vec![],
        },
        Instruction::Gate {
            gate: QuantumGate::Phase(Angle::Scalar(std::f64::consts::PI / 4.0)),
            target,
            control: vec![],
        },
    ])
    .chain(u4_gate_type.cnot(control_2, target))
    .chain([
        Instruction::Gate {
            gate: QuantumGate::Phase(Angle::Scalar(-std::f64::consts::PI / 4.0)),
            target,
            control: vec![],
        },
        Instruction::Gate {
            gate: QuantumGate::Hadamard,
            target,
            control: vec![],
        },
    ])
    .collect()
}

fn c4x(
    control_0: usize,
    control_1: usize,
    control_2: usize,
    control_3: usize,
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    [Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }]
    .into_iter()
    .chain(cp(
        std::f64::consts::PI / 2.0,
        control_3,
        target,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(rc3x(
        control_0,
        control_1,
        control_2,
        control_3,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(cp(
        -std::f64::consts::PI / 2.0,
        control_3,
        target,
        u4_gate_type,
    ))
    .chain([Instruction::Gate {
        gate: QuantumGate::Hadamard,
        target,
        control: vec![],
    }])
    .chain(
        rc3x(control_0, control_1, control_2, control_3, u4_gate_type)
            .iter()
            .rev()
            .map(Instruction::get_inverse)
            .collect::<Vec<_>>(),
    )
    .chain(c3sx(control_0, control_1, control_2, target, u4_gate_type))
    .collect()
}

fn mcx_dirty_action(
    control: &[usize],
    aux_control: &[usize],
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    let mut instructions = Vec::new();

    instructions.extend(toffoli(
        control[control.len() - 1],
        aux_control[aux_control.len() - 1],
        target,
        u4_gate_type,
    ));

    for i in 1..aux_control.len() {
        instructions.extend(toffoli_pi4(
            true,
            false,
            control[control.len() - i - 1],
            aux_control[aux_control.len() - i - 1],
            aux_control[aux_control.len() - i],
            u4_gate_type,
        ));
    }

    instructions.extend(toffoli_pi4(
        false,
        false,
        control[0],
        control[1],
        aux_control[0],
        u4_gate_type,
    ));

    instructions
}

pub fn mcx_dirty(
    control: &[usize],
    aux_control: &[usize],
    target: usize,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    if control.len() == 1 {
        return vec![Instruction::Gate {
            gate: QuantumGate::PauliX,
            target,
            control: control.to_vec(),
        }];
    }

    if control.len() == 2 {
        return toffoli(control[0], control[1], target, u4_gate_type);
    }

    let num_aux = control.len() - 2;
    let aux_control = &aux_control[..num_aux];

    let mut instructions = Vec::new();

    for _ in 0..2 {
        instructions.extend(mcx_dirty_action(control, aux_control, target, u4_gate_type));

        for i in 0..num_aux - 1 {
            instructions.extend(toffoli_pi4(
                false,
                true,
                control[2 + i],
                aux_control[i],
                aux_control[i + 1],
                u4_gate_type,
            ));
        }
    }

    instructions
}

pub fn decompose(
    control: &[usize],
    target: usize,
    auxiliary: Option<usize>,
    u4_gate_type: U4GateType,
) -> Vec<Instruction> {
    debug!(
        "Performing Pauli X decomposition: target={}; control={:?}; auxiliary={:?}",
        target, control, auxiliary
    );

    let control_size = control.len();

    match control_size {
        1 => u4_gate_type.cnot(control[0], target),
        2 => toffoli(control[0], control[1], target, u4_gate_type),
        3 => c3x(control[0], control[1], control[2], target, u4_gate_type),
        4 => c4x(
            control[0],
            control[1],
            control[2],
            control[3],
            target,
            u4_gate_type,
        ),
        _ => {
            if let Some(auxiliary) = auxiliary {
                let ctrl_0 = &control[..control_size / 2];
                let mut ctrl_1 = control[control_size / 2..].to_vec();
                ctrl_1.push(auxiliary);

                let mut instruction = Vec::new();

                instruction.extend(mcx_dirty(ctrl_0, &ctrl_1, auxiliary, u4_gate_type));

                instruction.extend(mcx_dirty(&ctrl_1, ctrl_0, target, u4_gate_type));

                instruction.extend(mcx_dirty(ctrl_0, &ctrl_1, auxiliary, u4_gate_type));

                instruction
            } else {
                crate::decomposition::u2::decompose(
                    QuantumGate::PauliX,
                    control,
                    target,
                    u4_gate_type,
                )
            }
        }
    }
}
