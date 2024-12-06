//


use std::borrow::BorrowMut;
use std::collections::HashMap;
use std::rc::Weak;
use std::rc::Rc;
use std::cell::RefCell;

use pyo3::prelude::*;

use crate::bdd as pybdd;

pub enum _Node {
    Basic {
        id: usize,
        name: String,
    },
    Repeat {
        id: usize,
        name: String,
    },
    And {
        id: usize,
        args: Vec<FtNode>,
    },
    Or {
        id: usize,
        args: Vec<FtNode>,
    },
    KofN {
        id: usize,
        k: usize,
        args: Vec<FtNode>,
    },
}

#[pyclass(unsendable)]
#[derive(Clone)]
pub struct FtNode {
    parent_ftmgr: Weak<RefCell<_Mgr>>,
    node: Rc<_Node>,
}

struct _Mgr {
    id: RefCell<usize>,
    bddtable: RefCell<HashMap<usize,pybdd::BddNode>>,
    bddmgr: Rc<RefCell<pybdd::BddMgr>>,
}

#[pyclass(unsendable)]
pub struct FtMgr {
    ftmgr: Rc<RefCell<_Mgr>>,
}

impl _Mgr {
    pub fn new() -> _Mgr {
        _Mgr {
            id: RefCell::new(0),
            // events: RefCell::new(HashMap::new()),
            bddtable: RefCell::new(HashMap::new()),
            bddmgr: Rc::new(RefCell::new(pybdd::BddMgr::new())),
        }
    }

    pub fn id(&self) -> usize {
        *self.id.borrow()
    }

    fn basic(mgr: &Rc<RefCell<Self>>, name: &str) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = _Node::Basic { id: mgr_borrow.id(), name: name.to_string() };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn repeat(mgr: &Rc<RefCell<Self>>, name: &str) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = _Node::Repeat { id: mgr_borrow.id(), name: name.to_string() };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn and(mgr: &Rc<RefCell<Self>>, args: Vec<FtNode>) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = _Node::And { id: mgr_borrow.id(), args };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn or(mgr: &Rc<RefCell<Self>>, args: Vec<FtNode>) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = _Node::Or { id: mgr_borrow.id(), args };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn kofn(mgr: &Rc<RefCell<Self>>, k: usize, args: Vec<FtNode>) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = _Node::KofN { id: mgr_borrow.id(), k, args };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn tobdd(mgr: &Rc<RefCell<Self>>, bddmgr: &Rc<RefCell<pybdd::BddMgr>>, top: FtNode) -> pybdd::BddNode {
        let ftmgr = mgr.borrow();
        let node = top.node();
        match node.as_ref() {
            _Node::Basic { id, name } => bddmgr.borrow().var(&name),
            _Node::Repeat { id, name } => {
                if let Some(x) = ftmgr.bddtable.borrow().get(id) {
                    return x.clone()
                }
                let x = bddmgr.borrow().var(&name);
                {
                    let mut bddnodes = ftmgr.bddtable.borrow_mut();
                    bddnodes.insert(*id, x.clone());
                }
                x
            }
            _Node::And { id, args } => {
                if let Some(x) = ftmgr.bddtable.borrow().get(id) {
                    return x.clone();
                }
                let b = args.iter().map(|x| Self::tobdd(mgr, bddmgr, x.clone())).collect::<Vec<_>>();
                let x = bddmgr.borrow().and(b);
                {
                    let mut bddnodes = ftmgr.bddtable.borrow_mut();
                    bddnodes.insert(*id, x.clone());
                }
                x
            }
            _Node::Or { id, args } => {
                if let Some(x) = ftmgr.bddtable.borrow().get(id) {
                    return x.clone();
                }
                let b = args.iter().map(|x| Self::tobdd(mgr, bddmgr, x.clone())).collect::<Vec<_>>();
                let x = bddmgr.borrow().or(b);
                {
                    let mut bddnodes = ftmgr.bddtable.borrow_mut();
                    bddnodes.insert(*id, x.clone());
                }
                x
            }
            _Node::KofN { id, k, args } => {
                if let Some(x) = ftmgr.bddtable.borrow().get(id) {
                    return x.clone();
                }
                let b = args.iter().map(|x| Self::tobdd(mgr, bddmgr, x.clone())).collect::<Vec<_>>();
                let x = bddmgr.borrow().kofn(*k, b);
                {
                    let mut bddnodes = ftmgr.bddtable.borrow_mut();
                    bddnodes.insert(*id, x.clone());
                }
                x
            }
        }
    }
    
}

#[pymethods]
impl FtMgr {
    #[new]
    pub fn new() -> FtMgr {
        FtMgr {
            ftmgr: Rc::new(RefCell::new(_Mgr::new())),
        }
    }

    pub fn basic(&self, name: &str) -> FtNode {
        _Mgr::basic(&self.ftmgr, name)
    }

    pub fn repeat(&self, name: &str) -> FtNode {
        _Mgr::repeat(&self.ftmgr, name)
    }

    pub fn and(&self, args: Vec<FtNode>) -> FtNode {
        _Mgr::and(&self.ftmgr, args)
    }

    pub fn or(&self, args: Vec<FtNode>) -> FtNode {
        _Mgr::or(&self.ftmgr, args)
    }

    pub fn kofn(&self, k: usize, args: Vec<FtNode>) -> FtNode {
        _Mgr::kofn(&self.ftmgr, k, args)
    }
}

impl FtNode {
    fn new(ftmgr: Rc<RefCell<_Mgr>>, node: Rc<_Node>) -> Self {
        FtNode {
            parent_ftmgr: Rc::downgrade(&ftmgr),
            node: node,
        }
    }

    fn ftmgr(&self) -> Rc<RefCell<_Mgr>> {
        self.parent_ftmgr.upgrade().unwrap()
    }

    pub fn node(&self) -> Rc<_Node> {
        self.node.clone()
    }
}

#[pymethods]
impl FtNode {
    fn __repr__(&self) -> String {
        match self.node.as_ref() {
            _Node::Basic { name, .. } => name.clone(),
            _Node::Repeat { name, .. } => name.clone(),
            _Node::And { args, .. } => args.iter().map(|x| x.__repr__()).collect::<Vec<String>>().join(" & "),
            _Node::Or { args, .. } => args.iter().map(|x| x.__repr__()).collect::<Vec<String>>().join(" | "),
            _Node::KofN { k, args, .. } => format!("{} of {}", k, args.iter().map(|x| x.__repr__()).collect::<Vec<String>>().join(" | ")),
        }
    }

    fn __and__(&self, other: &FtNode) -> FtNode {
        let ftmgr = self.ftmgr();
        let args = vec![self.clone(), other.clone()];
        _Mgr::and(&ftmgr, args)
    }

    fn __or__(&self, other: &FtNode) -> FtNode {
        let ftmgr = self.ftmgr();
        let args = vec![self.clone(), other.clone()];
        _Mgr::or(&ftmgr, args)
    }

    pub fn bdd(&self) -> pybdd::BddNode {
        let ftmgr = self.ftmgr();
        _Mgr::tobdd(&ftmgr, &ftmgr.clone().borrow().bddmgr, self.clone())
    }
}

#[pyfunction]
pub fn ftkofn(k: usize, args: Vec<FtNode>) -> FtNode {
    let ftmgr = args[0].ftmgr();
    _Mgr::kofn(&ftmgr, k, args)
}
