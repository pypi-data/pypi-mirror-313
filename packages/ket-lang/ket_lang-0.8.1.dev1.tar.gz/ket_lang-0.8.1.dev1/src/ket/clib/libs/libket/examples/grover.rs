// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use std::f64::consts::FRAC_PI_4;

use ket::prelude::*;

fn main() -> Result<(), KetError> {
    set_log_level(3);

    let config = Configuration {
        num_qubits: 12,
        qpu: Some(QPU::new(
            // 0--1--2--3
            // |  |  |  |
            // 4--5--6--7
            // |  |  |  |
            // 8--9--A--B
            Some(ket::ex_arch::GRID12.to_vec()),
            12,
            U2Gates::RzSx,
            U4Gate::CZ,
        )),
        ..Default::default()
    };

    let mut process = Process::new(config);

    let size = 8;

    let qubits: Vec<_> = (0..size).map(|_| process.alloc().unwrap()).collect();

    for qubit in &qubits {
        process.gate(QuantumGate::Hadamard, *qubit)?;
    }

    let steps = ((FRAC_PI_4) * f64::sqrt((1 << size) as f64)) as i64;

    for _ in 0..steps {
        around(
            &mut process,
            |process| {
                for qubit in &qubits {
                    process.gate(QuantumGate::PauliX, *qubit)?;
                }
                Ok(())
            },
            |process| {
                ctrl(process, &qubits[1..], |process| {
                    process.gate(QuantumGate::PauliZ, qubits[0])
                })
            },
        )?;

        around(
            &mut process,
            |process| {
                for qubit in &qubits {
                    process.gate(QuantumGate::Hadamard, *qubit)?;
                }

                for qubit in &qubits {
                    process.gate(QuantumGate::PauliX, *qubit)?;
                }
                Ok(())
            },
            |process| {
                ctrl(process, &qubits[1..], |process| {
                    process.gate(QuantumGate::PauliZ, qubits[0])
                })
            },
        )?;
    }

    let _ = process.sample(&qubits, 1024)?;
    process.transpile();

    println!("{:#?}", process.metadata());

    Ok(())
}
