// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use std::{collections::HashMap, hash::Hash};

use itertools::Itertools;

use crate::{
    execution::U2Gates,
    graph::GraphMatrix,
    ir::{
        gate::{matrix_dot, QuantumGate},
        hamiltonian::Hamiltonian,
        instructions::Instruction,
        qubit::{LogicalQubit, PhysicalQubit, Qubit},
    },
};

#[derive(Debug)]
pub(crate) struct Circuit<Q> {
    pub(crate) instructions: Vec<Instruction<Q>>,
    pub(crate) lines: HashMap<Q, Vec<usize>>,
    pub(crate) gate_count: HashMap<usize, usize>,
}

impl<Q> Circuit<Q>
where
    Q: Qubit + Eq + Hash + Copy + From<usize> + Sync,
{
    fn last_gate_index(&self, qubit: Q) -> Option<usize> {
        if let Some(gate_line) = self.lines.get(&qubit) {
            for index in gate_line.iter().rev() {
                match self.instructions[*index] {
                    Instruction::Gate { .. } => return Some(*index),
                    Instruction::Identity => continue,
                    _ => return None,
                }
            }
        }
        None
    }

    fn matches_inverse(&self, index: usize, gate: &QuantumGate, target: Q, control: &[Q]) -> bool {
        if let Instruction::Gate {
            gate: last_gate,
            target: last_target,
            control: last_control,
        } = &self.instructions[index]
        {
            target == *last_target
                && gate.is_inverse(last_gate)
                && control.len() == last_control.len()
                && control.iter().all(|c| last_control.contains(c))
                && control.iter().all(|qubit| {
                    self.last_gate_index(*qubit)
                        .map_or(false, |last_index| last_index == index)
                })
        } else {
            panic!("expecting a gate")
        }
    }

    pub fn line_instructions(&self, qubit: Q) -> impl Iterator<Item = &Instruction<Q>> {
        use genawaiter::{rc::gen, yield_};

        gen!({
            if let Some(gate_line) = self.lines.get(&qubit) {
                for index in gate_line.iter() {
                    yield_!(&self.instructions[*index]);
                }
            }
        })
        .into_iter()
    }

    pub fn line_instructions_rev(&self, qubit: Q) -> impl Iterator<Item = &Instruction<Q>> {
        use genawaiter::{rc::gen, yield_};

        gen!({
            if let Some(gate_line) = self.lines.get(&qubit) {
                for index in gate_line.iter().rev() {
                    yield_!(&self.instructions[*index]);
                }
            }
        })
        .into_iter()
    }

    pub fn instruction(&self, index: usize) -> &Instruction<Q> {
        &self.instructions[index]
    }

    pub fn gate(&mut self, gate: QuantumGate, target: Q, control: &[Q]) {
        if gate.is_identity() {
            return;
        }

        let gate_index = self.instructions.len();
        let num_qubits = control.len() + 1;

        if let Some(last_gate_index) = self.last_gate_index(target) {
            if self.matches_inverse(last_gate_index, &gate, target, control) {
                std::mem::take(&mut self.instructions[last_gate_index]);
                *self.gate_count.entry(num_qubits).or_insert(1) -= 1;
                return;
            }
        }

        for qubit in control.iter().chain([&target]) {
            self.lines.entry(*qubit).or_default().push(gate_index);
        }

        self.instructions.push(Instruction::Gate {
            gate,
            target,
            control: control.to_owned(),
        });

        *self.gate_count.entry(num_qubits).or_insert(0) += 1;
    }

    pub fn depth(&self) -> usize {
        let mut head_gates = self
            .lines
            .keys()
            .map(|qubit| (*qubit, 0))
            .collect::<HashMap<_, _>>();
        let mut front = HashMap::new();
        let mut frozen = HashMap::new();
        let mut active = Vec::new();

        let mut depth = 0;
        loop {
            for (qubit, head) in head_gates.iter_mut() {
                if !*frozen.entry(*qubit).or_insert(false) {
                    while let Some(index) = self
                        .lines
                        .get(qubit)
                        .and_then(|line: &Vec<usize>| line.get(*head))
                    {
                        let instruction = self.instruction(*index);

                        if !instruction.is_ctrl_gate() {
                            *head += 1;
                            continue;
                        }

                        front.insert(*qubit, *index);

                        if instruction
                            .qubits()
                            .all(|qubit| front.get(qubit).map_or(false, |gate| *gate == *index))
                        {
                            for qubit in instruction.qubits() {
                                front.remove(qubit);
                            }

                            active.push(*index);
                        }

                        frozen.insert(*qubit, true);
                        break;
                    }
                }
            }

            if active.is_empty() {
                break;
            }

            for index in active.drain(..) {
                let instruction = self.instruction(index);
                for qubit in instruction.qubits() {
                    *head_gates.get_mut(qubit).unwrap() += 1;
                    frozen.insert(*qubit, false);
                }
            }

            depth += 1;
        }

        depth
    }
}

impl Circuit<PhysicalQubit> {
    pub(crate) fn add_instruction(&mut self, instruction: Instruction<PhysicalQubit>) {
        let index = self.instructions.len();
        for qubit in instruction.qubits() {
            self.lines.entry(*qubit).or_default().push(index);
        }

        if let Instruction::Gate { control, .. } = &instruction {
            *self.gate_count.entry(control.len() + 1).or_insert(0) += 1;
        }

        self.instructions.push(instruction);
    }

    pub(crate) fn gate_map(&mut self, u2_gates: U2Gates) {
        if matches!(u2_gates, U2Gates::All) {
            return;
        }

        for (qubit, line) in self.lines.iter() {
            let mut gates = line.iter();
            while let Some(index) = gates.next() {
                let instruction = self.instruction(*index);
                if !instruction.one_qubit_gate() {
                    continue;
                }
                let mut matrix = instruction.matrix();

                for next_index in gates.by_ref() {
                    let next_gate = self.instruction(*next_index);
                    if next_gate.one_qubit_gate() {
                        matrix = matrix_dot(&next_gate.matrix(), &matrix);
                        std::mem::take(&mut self.instructions[*next_index]);
                    } else {
                        break;
                    }
                }
                self.instructions[*index] = Instruction::U2Gates {
                    gates: u2_gates.decompose(&matrix),
                    qubit: *qubit,
                };
            }
        }

        let mut new_circuit = Self::default();
        for instruction in self.instructions.iter() {
            match instruction {
                Instruction::Identity => {}
                Instruction::U2Gates { gates, qubit } => {
                    for gate in gates {
                        if gate.is_identity() {
                            continue;
                        }
                        new_circuit.add_instruction(Instruction::Gate {
                            gate: *gate,
                            target: *qubit,
                            control: vec![],
                        });
                    }
                }
                _ => {
                    new_circuit.add_instruction(instruction.clone());
                }
            }
        }

        *self = new_circuit;
    }
}

impl Circuit<LogicalQubit> {
    pub fn measure(&mut self, qubits: &[LogicalQubit], index: usize) {
        let inst_index = self.instructions.len();
        for qubit in qubits {
            self.lines.entry(*qubit).or_default().push(inst_index);
        }

        self.instructions.push(Instruction::Measure {
            qubits: qubits.to_owned(),
            index,
        });
    }

    pub fn sample(&mut self, qubits: &[LogicalQubit], shots: usize, index: usize) {
        let inst_index = self.instructions.len();
        for qubit in qubits {
            self.lines.entry(*qubit).or_default().push(inst_index);
        }

        self.instructions.push(Instruction::Sample {
            qubits: qubits.to_owned(),
            index,
            shots,
        });
    }

    pub fn exp_value(&mut self, hamiltonian: Hamiltonian<LogicalQubit>, index: usize) {
        let inst_index = self.instructions.len();
        for qubit in hamiltonian.qubits() {
            self.lines.entry(*qubit).or_default().push(inst_index);
        }

        self.instructions
            .push(Instruction::ExpValue { hamiltonian, index });
    }

    pub fn dump(&mut self, qubits: &[LogicalQubit], index: usize) {
        let inst_index = self.instructions.len();
        for qubit in qubits {
            self.lines.entry(*qubit).or_default().push(inst_index);
        }

        self.instructions.push(Instruction::Dump {
            qubits: qubits.to_owned(),
            index,
        });
    }

    pub fn interacting_qubits(&self, qubit: LogicalQubit) -> impl Iterator<Item = &LogicalQubit> {
        use genawaiter::{rc::gen, yield_};
        gen!({
            for instruction in self.line_instructions(qubit) {
                for inst_qubit in instruction.qubits() {
                    if *inst_qubit != qubit {
                        yield_!(inst_qubit);
                    }
                }
            }
        })
        .into_iter()
        .unique()
    }

    pub fn interacting_qubits_rev(
        &self,
        qubit: LogicalQubit,
    ) -> impl Iterator<Item = &LogicalQubit> {
        use genawaiter::{rc::gen, yield_};
        gen!({
            for instruction in self.line_instructions_rev(qubit) {
                for inst_qubit in instruction.qubits() {
                    if *inst_qubit != qubit {
                        yield_!(inst_qubit);
                    }
                }
            }
        })
        .into_iter()
        .unique()
    }

    pub fn alloc_aux_qubit(&mut self, aux_qubit: LogicalQubit, main_qubit: LogicalQubit) {
        assert!(aux_qubit.is_aux());
        assert!(main_qubit.is_main());
        let aux_line = self.lines.remove(&aux_qubit);
        if let Some(line) = aux_line {
            for index in line {
                self.instructions
                    .get_mut(index)
                    .unwrap()
                    .replace_qubit(aux_qubit, main_qubit);
                self.lines.entry(main_qubit).or_default().push(index);
            }
        }
    }

    pub fn interaction_graph(&self) -> GraphMatrix<LogicalQubit> {
        let mut graph = GraphMatrix::new(self.lines.len());
        for (index, instruction) in self.instructions.iter().enumerate() {
            if instruction.is_ctrl_gate() {
                let mut qubits = instruction.qubits();
                let i = *qubits.next().unwrap();
                let j = *qubits.next().unwrap();
                if graph.edge(i, j).is_none() {
                    graph.set_edge(i, j, index as i64);
                }
            }
        }
        for i in self.lines.keys() {
            for j in self.lines.keys() {
                if i != j && graph.edge(*i, *j).is_none() {
                    graph.set_edge(*i, *j, self.instructions.len() as i64);
                }
            }
        }
        graph.calculate_distance();
        graph
    }
}

impl<Q> Default for Circuit<Q> {
    fn default() -> Self {
        Self {
            instructions: Default::default(),
            lines: Default::default(),
            gate_count: Default::default(),
        }
    }
}
