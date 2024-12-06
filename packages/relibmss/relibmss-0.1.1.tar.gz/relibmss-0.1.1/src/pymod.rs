use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

use crate::bdd::BddMgr;
use crate::bdd::BddNode;

use crate::bdd::kofn;
use crate::bdd::ifelse;

use crate::ftnode::FtMgr;
use crate::ftnode::FtNode;
use crate::ftnode::ftkofn;

#[pymodule]
pub fn relibmss(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<BddNode>()?;
    m.add_class::<BddMgr>()?;
    m.add_function(wrap_pyfunction!(ifelse, m)?)?;
    m.add_function(wrap_pyfunction!(kofn, m)?)?;
    m.add_class::<FtNode>()?;
    m.add_class::<FtMgr>()?;
    m.add_function(wrap_pyfunction!(ftkofn, m)?)?;
    Ok(())
}
