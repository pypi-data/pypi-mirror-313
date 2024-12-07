//

use dd::bdd;
use dd::count::*;
use dd::dot::Dot;
use pyo3::exceptions::PyValueError;
use std::collections::HashSet;

use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;
use std::rc::Weak;

use pyo3::prelude::*;

use crate::ft;

#[pyclass(unsendable)]
pub struct BddMgr {
    pub bdd: Rc<RefCell<bdd::Bdd>>,
    pub vars: HashMap<String, bdd::BddNode>,
}

#[pyclass(unsendable)]
#[derive(Clone)]
pub struct BddNode {
    parent: Weak<RefCell<bdd::Bdd>>,
    node: bdd::BddNode,
}

#[pymethods]
impl BddMgr {
    // constructor
    #[new]
    pub fn new() -> Self {
        BddMgr {
            bdd: Rc::new(RefCell::new(bdd::Bdd::new())),
            vars: HashMap::new(),
        }
    }

    // size
    pub fn size(&self) -> (usize, usize, usize) {
        self.bdd.borrow().size()
    }

    // zero
    pub fn zero(&self) -> BddNode {
        BddNode::new(self.bdd.clone(), self.bdd.borrow().zero())
    }

    // one
    pub fn one(&self) -> BddNode {
        BddNode::new(self.bdd.clone(), self.bdd.borrow().one())
    }

    // defvar
    pub fn defvar(&mut self, var: &str) -> BddNode {
        if let Some(node) = self.vars.get(var) {
            return BddNode::new(self.bdd.clone(), node.clone());
        } else {
            let level = self.vars.len();
            let mut bdd = self.bdd.borrow_mut();
            let h = bdd.header(level, var);
            let x0 = bdd.zero();
            let x1 = bdd.one();
            let node = bdd.create_node(&h, &x0, &x1);
            self.vars.insert(var.to_string(), node.clone());
            BddNode::new(self.bdd.clone(), node)
        }
    }

    pub fn var(&self, var: &str) -> Option<BddNode> {
        if let Some(node) = self.vars.get(var) {
            return Some(BddNode::new(self.bdd.clone(), node.clone()));
        } else {
            return None;
        }
    }

    pub fn rpn(&mut self, expr: &str, vars: HashSet<String>) -> PyResult<BddNode> {
        let mut stack = Vec::new();
        // let mut bdd = self.bdd.borrow_mut();
        for token in expr.split_whitespace() {
            match token {
                "0" | "False" => {
                    let bdd = self.bdd.borrow();
                    stack.push(bdd.zero());
                },
                "1" | "True" => {
                    let bdd = self.bdd.borrow();
                    stack.push(bdd.one());
                },
                "&" => {
                    let mut bdd = self.bdd.borrow_mut();
                    let right = stack.pop().unwrap();
                    let left = stack.pop().unwrap();
                    stack.push(bdd.and(&left, &right));
                }
                "|" => {
                    let mut bdd = self.bdd.borrow_mut();
                    let right = stack.pop().unwrap();
                    let left = stack.pop().unwrap();
                    stack.push(bdd.or(&left, &right));
                }
                "^" => {
                    let mut bdd = self.bdd.borrow_mut();
                    let right = stack.pop().unwrap();
                    let left = stack.pop().unwrap();
                    stack.push(bdd.xor(&left, &right));
                }
                "~" => {
                    let mut bdd = self.bdd.borrow_mut();
                    let node = stack.pop().unwrap();
                    stack.push(bdd.not(&node));
                }
                "?" => {
                    let mut bdd = self.bdd.borrow_mut();
                    let else_ = stack.pop().unwrap();
                    let then = stack.pop().unwrap();
                    let cond = stack.pop().unwrap();
                    stack.push(bdd.ite(&cond, &then, &else_));
                }
                _ => {
                    if let Some(node) = self.vars.get(token) {
                        stack.push(node.clone());
                    } else if let Some(_) = vars.get(token) {
                            let node = self.defvar(token);
                            self.vars.insert(token.to_string(), node.node.clone());
                            stack.push(node.node.clone());
                    } else {
                        return Err(PyValueError::new_err("unknown token"));
                    }
                }
            }
        }
        if let Some(node) = stack.pop() {
            return Ok(BddNode::new(self.bdd.clone(), node));
        } else {
            return Err(PyValueError::new_err("Invalid expression"));
        }
    }

    // pub fn and(&self, nodes: Vec<BddNode>) -> BddNode {
    //     let mut bdd = self.bdd.borrow_mut();
    //     let bnodes = nodes.iter().map(|n| n.node()).collect::<Vec<_>>();
    //     let result = ft::_and(&mut bdd, bnodes);
    //     BddNode::new(self.bdd.clone(), result)
    // }

    // pub fn or(&self, nodes: Vec<BddNode>) -> BddNode {
    //     let mut bdd = self.bdd.borrow_mut();
    //     let bnodes = nodes.iter().map(|n| n.node()).collect::<Vec<_>>();
    //     let result = ft::_or(&mut bdd, bnodes);
    //     BddNode::new(self.bdd.clone(), result)
    // }

    // pub fn kofn(&self, k: usize, nodes: Vec<BddNode>) -> BddNode {
    //     let mut bdd = self.bdd.borrow_mut();
    //     let bnodes = nodes.iter().map(|n| n.node()).collect::<Vec<_>>();
    //     let result = ft::kofn(&mut bdd, k, bnodes);
    //     BddNode::new(self.bdd.clone(), result)
    // }

    pub fn ifelse(&self, cond: &BddNode, then: &BddNode, else_: &BddNode) -> BddNode {
        let bdd = self.bdd.clone();
        BddNode::new(
            bdd.clone(),
            bdd.clone()
                .borrow_mut()
                .ite(&cond.node, &then.node, &else_.node),
        )
    }
}

impl BddNode {
    pub fn new(bdd: Rc<RefCell<bdd::Bdd>>, node: bdd::BddNode) -> Self {
        BddNode {
            parent: Rc::downgrade(&bdd),
            node: node,
        }
    }

    pub fn node(&self) -> bdd::BddNode {
        self.node.clone()
    }
}

#[pymethods]
impl BddNode {
    pub fn dot(&self) -> String {
        self.node.dot_string()
    }

    fn __and__(&self, other: &BddNode) -> BddNode {
        let bdd = self.parent.upgrade().unwrap();
        BddNode::new(
            bdd.clone(),
            bdd.clone().borrow_mut().and(&self.node, &other.node),
        )
    }

    fn __or__(&self, other: &BddNode) -> BddNode {
        let bdd = self.parent.upgrade().unwrap();
        BddNode::new(
            bdd.clone(),
            bdd.clone().borrow_mut().or(&self.node, &other.node),
        )
    }

    fn __xor__(&self, other: &BddNode) -> BddNode {
        let bdd = self.parent.upgrade().unwrap();
        BddNode::new(
            bdd.clone(),
            bdd.clone().borrow_mut().xor(&self.node, &other.node),
        )
    }

    fn __invert__(&self) -> BddNode {
        let bdd = self.parent.upgrade().unwrap();
        BddNode::new(bdd.clone(), bdd.clone().borrow_mut().not(&self.node))
    }

    pub fn prob(&self, pv: HashMap<String, f64>) -> f64 {
        let bdd = self.parent.upgrade().unwrap();
        ft::prob(&mut bdd.clone().borrow_mut(), &self.node, pv)
    }

    pub fn mcs(&self) -> BddNode {
        let bdd = self.parent.upgrade().unwrap();
        BddNode::new(
            bdd.clone(),
            ft::minsol(&mut bdd.clone().borrow_mut(), &self.node),
        )
    }

    pub fn extract(&self) -> Vec<Vec<String>> {
        let bdd = self.parent.upgrade().unwrap();
        ft::extract(&mut bdd.clone().borrow_mut(), &self.node)
    }

    pub fn count(&self) -> (usize, u64) {
        self.node.count()
    }
}

// #[pyfunction]
// pub fn kofn(k: usize, nodes: Vec<BddNode>) -> PyResult<BddNode> {
//     if nodes.len() < k {
//         return Err(PyValueError::new_err("Invalid expression"));
//     }
//     let bdd = nodes[0].parent.upgrade().unwrap();
//     let nodes = nodes.iter().map(|n| n.node()).collect::<Vec<_>>();
//     Ok(BddNode::new(
//         bdd.clone(),
//         ft::kofn(&mut bdd.clone().borrow_mut(), k, nodes),
//     ))
// }
