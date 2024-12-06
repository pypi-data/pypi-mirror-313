//

use dd::bdd;
use pyo3::exceptions::PyValueError;
use std::io::BufWriter;
use dd::dot::Dot;
use dd::count::*;

use std::rc::Weak;
use std::rc::Rc;
use std::cell::RefCell;
use std::collections::HashMap;

use pyo3::prelude::*;

use crate::ft;

#[pyclass(unsendable)]
pub struct BddMgr {
    pub bdd: Rc<RefCell<bdd::Bdd>>,
    pub vars: RefCell<HashMap<String, bdd::BddNode>>,
}

#[pymethods]
impl BddMgr {
    // constructor
    #[new]
    pub fn new() -> Self {
        BddMgr {
            bdd: Rc::new(RefCell::new(bdd::Bdd::new())),
            vars: RefCell::new(HashMap::new()),
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

    // var
    pub fn var(&self, var: &str) -> BddNode {
        let level = self.vars.borrow().len();
        let mut bdd = self.bdd.borrow_mut();
        let h = bdd.header(level, var);
        let x0 = bdd.zero();
        let x1 = bdd.one();
        let node = bdd.create_node(&h, &x0, &x1);
        self.vars.borrow_mut().insert(var.to_string(), node.clone());
        BddNode::new(self.bdd.clone(), node)
    }

    // vars
    pub fn vars(&self, vars: Vec<&str>) -> Vec<BddNode> {
        let mut bdd = self.bdd.borrow_mut();
        let mut nodes = Vec::new();
        for (level, v) in vars.iter().enumerate() {
            let h = bdd.header(level, v);
            let x0 = bdd.zero();
            let x1 = bdd.one();
            let b = vec![bdd.zero(), bdd.one()];
            let node = bdd.create_node(&h, &x0, &x1);
            self.vars.borrow_mut().insert(v.to_string(), node.clone());
            let x = BddNode::new(self.bdd.clone(), node);
            nodes.push(x);
        }
        nodes
    }

    pub fn rpn(&self, expr: &str) -> PyResult<BddNode> {
        let mut stack = Vec::new();
        let mut bdd = self.bdd.borrow_mut();
        for token in expr.split_whitespace() {
            match token {
                "0" => stack.push(bdd.zero()),
                "1" => stack.push(bdd.one()),
                "&" => {
                    let right = stack.pop().unwrap();
                    let left = stack.pop().unwrap();
                    stack.push(bdd.and(&left, &right));
                }
                "|" => {
                    let right = stack.pop().unwrap();
                    let left = stack.pop().unwrap();
                    stack.push(bdd.or(&left, &right));
                }
                "^" => {
                    let right = stack.pop().unwrap();
                    let left = stack.pop().unwrap();
                    stack.push(bdd.xor(&left, &right));
                }
                "~" => {
                    let node = stack.pop().unwrap();
                    stack.push(bdd.not(&node));
                }
                "?" => {
                    let else_ = stack.pop().unwrap();
                    let then = stack.pop().unwrap();
                    let cond = stack.pop().unwrap();
                    stack.push(bdd.ite(&cond, &then, &else_));
                }
                _ => {
                    if let Some(node) = self.vars.borrow().get(token) {
                        stack.push(node.clone());
                    } else {
                        return Err(PyValueError::new_err("unknown token"));
                    }
                }
            }
        }
        if stack.len() != 1 {
            return Err(PyValueError::new_err("Invalid expression"));
        }
        Ok(BddNode::new(self.bdd.clone(), stack.pop().unwrap()))        
    }

    pub fn and(&self, nodes: Vec<BddNode>) -> BddNode {
        let mut bdd = self.bdd.borrow_mut();
        let bnodes = nodes.iter().map(|n| n.node()).collect::<Vec<_>>();
        let result = ft::_and(&mut bdd, bnodes);
        BddNode::new(self.bdd.clone(), result)
    }

    pub fn or(&self, nodes: Vec<BddNode>) -> BddNode {
        let mut bdd = self.bdd.borrow_mut();
        let bnodes = nodes.iter().map(|n| n.node()).collect::<Vec<_>>();
        let result = ft::_or(&mut bdd, bnodes);
        BddNode::new(self.bdd.clone(), result)
    }

    pub fn kofn(&self, k: usize, nodes: Vec<BddNode>) -> BddNode {
        let mut bdd = self.bdd.borrow_mut();
        let bnodes = nodes.iter().map(|n| n.node()).collect::<Vec<_>>();
        let result = ft::kofn(&mut bdd, k, bnodes);
        BddNode::new(self.bdd.clone(), result)
    }
}

#[pyclass(unsendable)]
#[derive(Clone)]
pub struct BddNode {
    bdd: Weak<RefCell<bdd::Bdd>>,
    node: bdd::BddNode,
}

impl BddNode {
    pub fn new(bdd: Rc<RefCell<bdd::Bdd>>, node: bdd::BddNode) -> Self {
        BddNode {
            bdd: Rc::downgrade(&bdd),
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
        let mut buf = vec![];
        {
            let mut io = BufWriter::new(&mut buf);
            self.node.dot(&mut io);
        }
        std::str::from_utf8(&buf).unwrap().to_string()
    }

    fn __and__(&self, other: &BddNode) -> BddNode {
        let bdd = self.bdd.upgrade().unwrap();
        BddNode::new(bdd.clone(), bdd.clone().borrow_mut().and(&self.node, &other.node))
    }

    fn __or__(&self, other: &BddNode) -> BddNode {
        let bdd = self.bdd.upgrade().unwrap();
        BddNode::new(bdd.clone(), bdd.clone().borrow_mut().or(&self.node, &other.node))
    }

    fn __xor__(&self, other: &BddNode) -> BddNode {
        let bdd = self.bdd.upgrade().unwrap();
        BddNode::new(bdd.clone(), bdd.clone().borrow_mut().xor(&self.node, &other.node))
    }

    fn __invert__(&self) -> BddNode {
        let bdd = self.bdd.upgrade().unwrap();
        BddNode::new(bdd.clone(), bdd.clone().borrow_mut().not(&self.node))
    }

    pub fn prob(&self, pv: HashMap<String, f64>) -> f64 {
        let bdd = self.bdd.upgrade().unwrap();
        ft::prob(&mut bdd.clone().borrow_mut(), &self.node, pv)
    }

    pub fn mcs(&self) -> BddNode {
        let bdd = self.bdd.upgrade().unwrap();
        BddNode::new(bdd.clone(), ft::minsol(&mut bdd.clone().borrow_mut(), &self.node))
    }

    pub fn extract(&self) -> Vec<Vec<String>> {
        let bdd = self.bdd.upgrade().unwrap();
        ft::extract(&mut bdd.clone().borrow_mut(), &self.node)
    }

    pub fn count(&self) -> (usize, u64) {
        self.node.count()
    }
}

#[pyfunction]
pub fn ifelse(cond: &BddNode, then: &BddNode, else_: &BddNode) -> BddNode {
    let bdd = cond.bdd.upgrade().unwrap();
    BddNode::new(bdd.clone(), bdd.clone().borrow_mut().ite(&cond.node, &then.node, &else_.node))
}

#[pyfunction]
pub fn kofn(k: usize, nodes: Vec<BddNode>) -> PyResult<BddNode> {
    if nodes.len() < k {
        return Err(PyValueError::new_err("Invalid expression"));
    }
    let bdd = nodes[0].bdd.upgrade().unwrap();
    let nodes = nodes.iter().map(|n| n.node()).collect::<Vec<_>>();
    Ok(BddNode::new(bdd.clone(), ft::kofn(&mut bdd.clone().borrow_mut(), k, nodes)))
}

