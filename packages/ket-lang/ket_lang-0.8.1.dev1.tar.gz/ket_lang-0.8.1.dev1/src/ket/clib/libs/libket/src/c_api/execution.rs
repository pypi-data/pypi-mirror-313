// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
// SPDX-FileCopyrightText: 2024 2024 Otávio Augusto de Santana Jatobá <otavio.jatoba@grad.ufsc.br>
//
// SPDX-License-Identifier: Apache-2.0

use crate::execution::*;

#[repr(C)]
#[derive(Debug, Clone)]
pub struct BatchCExecution {
    submit_execution: fn(*const u8, usize, *const u8, usize),
    get_results: fn(data: &mut *const u8, len: &mut usize),
}

impl BatchExecution for BatchCExecution {
    fn submit_execution(
        &mut self,
        logical_circuit: &[Instruction<LogicalQubit>],
        physical_circuit: Option<&[Instruction<PhysicalQubit>]>,
    ) {
        let logical_circuit = serde_json::to_vec(logical_circuit).unwrap();
        let physical_circuit = serde_json::to_vec(&physical_circuit).unwrap();
        (self.submit_execution)(
            logical_circuit.as_ptr(),
            logical_circuit.len(),
            physical_circuit.as_ptr(),
            physical_circuit.len(),
        );
    }

    fn get_results(&mut self) -> ResultData {
        let mut buffer = std::ptr::null();
        let mut len: usize = 0;
        (self.get_results)(&mut buffer, &mut len);
        let buffer = unsafe { std::slice::from_raw_parts(buffer, len) };
        serde_json::from_slice(buffer).unwrap()
    }
}

#[no_mangle]
/// # Safety
pub unsafe extern "C" fn ket_make_configuration(
    num_qubits: usize,
    batch_execution: *const BatchCExecution,
    measure: i32,
    sample: i32,
    exp_value: i32,
    dump: i32,
    define_qpu: bool,
    coupling_graph: *const (usize, usize),
    coupling_graph_size: usize,
    u4_gate: i32,
    u2_gates: i32,
    result: &mut *mut Configuration,
) -> i32 {
    let execution: Option<QuantumExecution> = if batch_execution.is_null() {
        None
    } else {
        Some(QuantumExecution::Batch(Box::new(unsafe {
            (*batch_execution).clone()
        })))
    };

    let qpu = if define_qpu {
        let coupling_graph = if coupling_graph_size == 0 {
            None
        } else {
            let coupling_graph = std::slice::from_raw_parts(coupling_graph, coupling_graph_size);
            Some(coupling_graph.to_owned())
        };

        let u4_gate = match u4_gate {
            0 => U4Gate::CX,
            1 => U4Gate::CZ,
            _ => panic!("undefined U4 gate type"),
        };

        let u2_gates = match u2_gates {
            0 => U2Gates::All,
            1 => U2Gates::ZYZ,
            2 => U2Gates::RzSx,
            _ => panic!("undefined U2 gate set"),
        };
        Some(QPU::new(coupling_graph, num_qubits, u2_gates, u4_gate))
    } else {
        None
    };

    *result = Box::into_raw(Box::new(Configuration {
        num_qubits,
        execution,
        qpu,
        measure: FeatureStatus::from(measure),
        sample: FeatureStatus::from(sample),
        exp_value: FeatureStatus::from(exp_value),
        dump: FeatureStatus::from(dump),
    }));

    0
}
