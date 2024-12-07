use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

use crate::bdd::BddMgr;
use crate::bdd::BddNode;

// use crate::bdd::ifelse;
// use crate::bdd::kofn;

// use crate::ftnode::ftkofn;
// use crate::ftnode::FtMgr;
// use crate::ftnode::FtNode;

use crate::mdd::MddMgr;
use crate::mdd::MddNode;

// use crate::mdd::SymbolicMgr;
// use crate::mdd::SymbolicNode;

#[pymodule]
pub fn relibmss(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<BddNode>()?;
    m.add_class::<BddMgr>()?;
    // m.add_function(wrap_pyfunction!(ifelse, m)?)?;
    // m.add_function(wrap_pyfunction!(kofn, m)?)?;
    // m.add_class::<FtNode>()?;
    // m.add_class::<FtMgr>()?;
    // m.add_function(wrap_pyfunction!(ftkofn, m)?)?;
    m.add_class::<MddNode>()?;
    m.add_class::<MddMgr>()?;
    Ok(())
}
