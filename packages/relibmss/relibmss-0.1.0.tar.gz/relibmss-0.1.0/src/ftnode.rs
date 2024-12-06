//


use std::borrow::BorrowMut;
use std::collections::HashMap;
use std::rc::Weak;
use std::rc::Rc;
use std::cell::RefCell;

use pyo3::prelude::*;

use crate::bdd as pybdd;

pub enum FTNode {
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

pub struct Var {
    pub node: Vec<String>,
    pub bddnode: pybdd::BddNode,
}

struct FTMgr {
    pub id: RefCell<usize>,
    pub events: RefCell<HashMap<String,Var>>,
    pub bddnode: RefCell<HashMap<usize,pybdd::BddNode>>,
}

impl FTMgr {
    pub fn new() -> FTMgr {
        FTMgr {
            id: RefCell::new(0),
            events: RefCell::new(HashMap::new()),
            bddnode: RefCell::new(HashMap::new()),
        }
    }

    pub fn id(&self) -> usize {
        *self.id.borrow()
    }

    fn basic(mgr: &Rc<RefCell<Self>>, name: &str) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = FTNode::Basic { id: mgr_borrow.id(), name: name.to_string() };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn repeat(mgr: &Rc<RefCell<Self>>, name: &str) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = FTNode::Repeat { id: mgr_borrow.id(), name: name.to_string() };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn and(mgr: &Rc<RefCell<Self>>, args: Vec<FtNode>) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = FTNode::And { id: mgr_borrow.id(), args };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn or(mgr: &Rc<RefCell<Self>>, args: Vec<FtNode>) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = FTNode::Or { id: mgr_borrow.id(), args };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn kofn(mgr: &Rc<RefCell<Self>>, k: usize, args: Vec<FtNode>) -> FtNode {
        let mgr_borrow = mgr.borrow();
        let node = FTNode::KofN { id: mgr_borrow.id(), k, args };
        *mgr_borrow.id.borrow_mut() += 1;
        FtNode::new(mgr.clone(), Rc::new(node))
    }

    fn create(mgr: &Rc<RefCell<Self>>, bddmgr: &mut pybdd::BddMgr, top: FtNode) -> pybdd::BddNode {
        let ftmgr = mgr.borrow();
        let node = top.node();
        match node.as_ref() {
            FTNode::Basic { id, name } => {
                if let Some(v) = ftmgr.events.borrow_mut().get_mut(name) {
                    let u = v.node.len();
                    let name_ = format!("{}_{}", name, u);
                    let x = bddmgr.var(&name_);
                    v.node.push(name_);
                    v.bddnode = x.clone();
                    return x
                }
                let name_ = format!("{}_0", name);
                let x = bddmgr.var(&name_);
                let v = Var { node: vec![name_], bddnode: x.clone() };
                {
                    let mut events = ftmgr.events.borrow_mut();
                    events.insert(name.clone(), v);
                }
                x
            }
            FTNode::Repeat { id, name } => {
                if let Some(v) = ftmgr.events.borrow().get(name) {
                    return v.bddnode.clone();
                }
                let x = bddmgr.var(&name);
                let v = Var { node: vec![name.clone()], bddnode: x.clone() };
                {
                    let mut events = ftmgr.events.borrow_mut();
                    events.insert(name.clone(), v);
                }
                x
            }
            FTNode::And { id, args } => {
                if let Some(x) = ftmgr.bddnode.borrow().get(id) {
                    return x.clone();
                }
                let mut b = Vec::new();
                for arg in args.iter() {
                    let tmp = Self::create(mgr, bddmgr, arg.clone());
                    b.push(tmp);
                }
                let x = bddmgr.and(b);
                {
                    let mut bddnodes = ftmgr.bddnode.borrow_mut();
                    bddnodes.insert(*id, x.clone());
                }
                x
            }
            FTNode::Or { id, args } => {
                if let Some(x) = ftmgr.bddnode.borrow().get(id) {
                    return x.clone();
                }
                let mut b = Vec::new();
                for arg in args.iter() {
                    let tmp = Self::create(mgr, bddmgr, arg.clone());
                    b.push(tmp);
                }
                let x = bddmgr.or(b);
                {
                    let mut bddnodes = ftmgr.bddnode.borrow_mut();
                    bddnodes.insert(*id, x.clone());
                }
                x
            }
            FTNode::KofN { id, k, args } => {
                if let Some(x) = ftmgr.bddnode.borrow().get(id) {
                    return x.clone();
                }
                let mut b = Vec::new();
                for arg in args.iter() {
                    let tmp = Self::create(mgr, bddmgr, arg.clone());
                    b.push(tmp);
                }
                let x = bddmgr.kofn(*k, b);
                {
                    let mut bddnodes = ftmgr.bddnode.borrow_mut();
                    bddnodes.insert(*id, x.clone());    
                }
                x
            }
        }
    }
    
}

#[pyclass(unsendable)]
pub struct FtMgr {
    ftmgr: Rc<RefCell<FTMgr>>,
}

#[pymethods]
impl FtMgr {
    #[new]
    pub fn new() -> FtMgr {
        FtMgr {
            ftmgr: Rc::new(RefCell::new(FTMgr::new())),
        }
    }

    pub fn basic(&self, name: &str) -> FtNode {
        FTMgr::basic(&self.ftmgr, name)
    }

    pub fn repeat(&self, name: &str) -> FtNode {
        FTMgr::repeat(&self.ftmgr, name)
    }

    pub fn and(&self, args: Vec<FtNode>) -> FtNode {
        FTMgr::and(&self.ftmgr, args)
    }

    pub fn or(&self, args: Vec<FtNode>) -> FtNode {
        FTMgr::or(&self.ftmgr, args)
    }

    pub fn kofn(&self, k: usize, args: Vec<FtNode>) -> FtNode {
        FTMgr::kofn(&self.ftmgr, k, args)
    }
}

#[pyclass(unsendable)]
#[derive(Clone)]
pub struct FtNode {
    ftmgr: Weak<RefCell<FTMgr>>,
    node: Rc<FTNode>,
}

impl FtNode {
    fn new(ftmgr: Rc<RefCell<FTMgr>>, node: Rc<FTNode>) -> Self {
        FtNode {
            ftmgr: Rc::downgrade(&ftmgr),
            node: node,
        }
    }

    pub fn ftmgr(&self) -> Rc<RefCell<FTMgr>> {
        self.ftmgr.upgrade().unwrap()
    }

    pub fn node(&self) -> Rc<FTNode> {
        self.node.clone()
    }
}

#[pymethods]
impl FtNode {
    fn __repr__(&self) -> String {
        match self.node.as_ref() {
            FTNode::Basic { name, .. } => name.clone(),
            FTNode::Repeat { name, .. } => name.clone(),
            FTNode::And { args, .. } => args.iter().map(|x| x.__repr__()).collect::<Vec<String>>().join(" & "),
            FTNode::Or { args, .. } => args.iter().map(|x| x.__repr__()).collect::<Vec<String>>().join(" | "),
            FTNode::KofN { k, args, .. } => format!("{} of {}", k, args.iter().map(|x| x.__repr__()).collect::<Vec<String>>().join(" | ")),
        }
    }

    fn __and__(&self, other: &FtNode) -> FtNode {
        let ftmgr = self.ftmgr();
        let args = vec![self.clone(), other.clone()];
        FTMgr::and(&ftmgr, args)
    }

    fn __or__(&self, other: &FtNode) -> FtNode {
        let ftmgr = self.ftmgr();
        let args = vec![self.clone(), other.clone()];
        FTMgr::or(&ftmgr, args)
    }

    pub fn compile(&self, bddmgr: &mut pybdd::BddMgr) -> pybdd::BddNode {
        let ftmgr = self.ftmgr();
        FTMgr::create(&ftmgr, bddmgr, self.clone())
    }
}

#[pyfunction]
pub fn ftkofn(k: usize, args: Vec<FtNode>) -> FtNode {
    let ftmgr = args[0].ftmgr();
    FTMgr::kofn(&ftmgr, k, args)
}
