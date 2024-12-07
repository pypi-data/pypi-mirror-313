// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use serde::Serialize;

use crate::execution::LogicalQubit;

pub(crate) mod su2;
pub(crate) mod u2;
pub(crate) mod util;
pub(crate) mod x;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Hash)]
pub enum AuxMode {
    Clean,
    Dirty,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Default, Hash)]
pub enum Algorithm {
    VChain(AuxMode),
    SingleAux(AuxMode),
    #[default]
    LinearDepth,
    Network,
    SU2,
    SU2Rewrite,
    Optimal,
    CU2,
}

impl std::fmt::Display for Algorithm {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

#[derive(Debug, Clone, Default)]
pub(crate) struct Schema {
    pub algorithm: Algorithm,
    pub aux_qubits: Option<Vec<LogicalQubit>>,
}

#[derive(Debug, Clone, Default)]
pub(crate) enum State {
    #[default]
    Begin,
    End,
}

#[derive(Debug, Clone, Default)]
pub(crate) struct Registry {
    pub algorithm: Algorithm,
    pub aux_qubits: Option<Vec<LogicalQubit>>,
    pub interacting_qubits: Option<Vec<LogicalQubit>>,
    pub state: State,
    pub num_u4: usize,
}

impl Algorithm {
    pub fn aux_needed(&self, control_size: usize) -> usize {
        match self {
            Algorithm::VChain(_) => control_size - 2,
            Algorithm::SingleAux(_) => 1,
            Algorithm::LinearDepth => 0,
            Algorithm::Network => control_size - 1,
            Algorithm::SU2 => 0,
            Algorithm::SU2Rewrite => 1,
            Algorithm::Optimal => 0,
            Algorithm::CU2 => 0,
        }
    }

    pub fn aux_mode(&self) -> AuxMode {
        match self {
            Algorithm::VChain(mode) => *mode,
            Algorithm::SingleAux(mode) => *mode,
            _ => AuxMode::Clean,
        }
    }

    pub fn need_aux(&self) -> bool {
        self.aux_needed(100) > 0
    }
}
