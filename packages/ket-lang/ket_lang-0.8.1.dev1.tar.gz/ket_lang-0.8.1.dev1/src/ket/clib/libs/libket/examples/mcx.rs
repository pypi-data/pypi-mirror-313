// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use ket::prelude::*;

fn main() -> Result<(), KetError> {
    set_log_level(4);

    let config = Configuration {
        num_qubits: 12,
        qpu: Some(QPU::new(
            // 0--1--2--3
            // |  |  |  |
            // 4--5--6--7
            // |  |  |  |
            // 8--9--A--B
            Some(vec![
                (0, 4),
                (0, 1),
                (1, 2),
                (1, 5),
                (2, 3),
                (2, 6),
                (3, 7),
                (4, 8),
                (4, 5),
                (5, 9),
                (5, 6),
                (6, 10),
                (6, 7),
                (7, 11),
                (8, 9),
                (9, 10),
                (10, 11),
            ]),
            12,
            Default::default(),
            Default::default(),
        )),
        ..Default::default()
    };

    let mut process = Process::new(config);

    let size = 6;

    let qubits: Vec<_> = (0..size).map(|_| process.alloc().unwrap()).collect();
    ctrl(&mut process, &qubits[1..], |process| {
        process.gate(QuantumGate::PauliZ, qubits[0])
    })?;

    let _ = process.sample(&qubits, 1024)?;
    process.transpile();

    println!("Instructions:");
    for line in process.instructions() {
        println!("\t{:?}", line);
    }

    println!("ISA Instructions:");
    if let Some(isa) = process.isa_instructions() {
        for line in isa {
            println!("\t{:?}", line);
        }
    }

    Ok(())
}
