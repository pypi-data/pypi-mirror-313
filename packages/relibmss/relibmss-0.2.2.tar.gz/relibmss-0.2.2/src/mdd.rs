use core::panic;
use std::cell::RefCell;
use std::rc::Rc;
use std::rc::Weak;

use dd::dot::Dot;
use dd::mtmdd2;
use dd::mtmdd2::build_from_rpn;
use dd::mtmdd2::gen_var;
use pyo3::exceptions::PyValueError;
use pyo3::pyclass;
use pyo3::pymethods;
use pyo3::PyResult;
use std::collections::HashMap;

#[pyclass(unsendable)]
pub struct MddMgr {
    mdd: Rc<RefCell<mtmdd2::MtMdd2<i64>>>,
    vars: HashMap<String, MddNode>,
}

#[pyclass(unsendable)]
#[derive(Clone, Debug)]
pub struct MddNode {
    parent: Weak<RefCell<mtmdd2::MtMdd2<i64>>>,
    node: mtmdd2::MtMdd2Node<i64>,
}

impl MddNode {
    fn new(parent: Rc<RefCell<mtmdd2::MtMdd2<i64>>>, node: mtmdd2::MtMdd2Node<i64>) -> Self {
        MddNode {
            parent: Rc::downgrade(&parent),
            node,
        }
    }
}

#[pymethods]
impl MddMgr {
    #[new]
    pub fn new() -> Self {
        MddMgr {
            mdd: Rc::new(RefCell::new(mtmdd2::MtMdd2::new())),
            vars: HashMap::new(),
        }
    }

    pub fn size(&self) -> (usize, usize, usize, usize) {
        self.mdd.borrow().size()
    }

    pub fn zero(&self) -> MddNode {
        MddNode::new(self.mdd.clone(), self.mdd.borrow().zero())
    }

    pub fn one(&self) -> MddNode {
        MddNode::new(self.mdd.clone(), self.mdd.borrow().one())
    }

    pub fn val(&self, value: i64) -> MddNode {
        let mut mdd = self.mdd.borrow_mut();
        let node = mdd.value(value);
        MddNode::new(self.mdd.clone(), node)
    }

    pub fn defvar(&mut self, label: &str, range: Vec<i64>) -> MddNode {
        if let Some(node) = self.vars.get(label) {
            return node.clone();
        } else {
            let level = self.vars.len();
            let result = {
                let mut mdd = self.mdd.borrow_mut();
                let node = gen_var(&mut mdd, label, level, &range);
                MddNode::new(self.mdd.clone(), node)
            };
            self.vars.insert(label.to_string(), result.clone());
            result
        }
    }

    pub fn var(&self, label: &str) -> Option<MddNode> {
        if let Some(node) = self.vars.get(label) {
            Some(node.clone())
        } else {
            None
        }
    }

    pub fn rpn(&mut self, rpn: &str, vars: HashMap<String,Vec<i64>>) -> PyResult<MddNode> {
        let tokens = rpn
            .split_whitespace()
            .map(|x| {
                match x {
                    "+" => mtmdd2::Token::Add,
                    "-" => mtmdd2::Token::Sub,
                    "*" => mtmdd2::Token::Mul,
                    "/" => mtmdd2::Token::Div,
                    "==" => mtmdd2::Token::Eq,
                    "!=" => mtmdd2::Token::Neq,
                    "<" => mtmdd2::Token::Lt,
                    "<=" => mtmdd2::Token::Lte,
                    ">" => mtmdd2::Token::Gt,
                    ">=" => mtmdd2::Token::Gte,
                    "&&" => mtmdd2::Token::And,
                    "||" => mtmdd2::Token::Or,
                    "!" => mtmdd2::Token::Not,
                    "?" => mtmdd2::Token::IfElse,
                    "True" => {
                        let node = {
                            let mdd = self.mdd.borrow();
                            mdd.one()
                        };
                        mtmdd2::Token::Value(node)
                    }
                    "False" => {
                        let node = {
                            let mdd = self.mdd.borrow();
                            mdd.zero()
                        };
                        mtmdd2::Token::Value(node)
                    }
                    _ => {
                        // parse whether it is a number or a variable
                        match x.parse::<i64>() {
                            Ok(val) => {
                                let node = {
                                    let mut mdd = self.mdd.borrow_mut();
                                    mdd.value(val)
                                };
                                mtmdd2::Token::Value(node)
                            }
                            Err(_) => {
                                let result = self.vars.get(x);
                                if let Some(node) = result {
                                    mtmdd2::Token::Value(node.node.clone())
                                } else {
                                    match vars.get(x) {
                                        Some(range) => {
                                            let node = self.defvar(x, range.clone());
                                            mtmdd2::Token::Value(node.node.clone())
                                        }
                                        None => panic!("Unknown variable: {}", x),
                                    }
                                }
                            }
                        }
                    }
                }
            })
            .collect::<Vec<_>>();
        let mut mdd = self.mdd.borrow_mut();
        if let Ok(node) = build_from_rpn(&mut mdd, &tokens) {
            Ok(MddNode::new(self.mdd.clone(), node))
        } else {
            Err(PyValueError::new_err("Invalid expression"))
        }
    }
}

#[pymethods]
impl MddNode {
    pub fn dot(&self) -> String {
        self.node.dot_string()
    }
}

#[cfg(test)]
mod tests {
    use std::vec;

    use super::*;

    #[test]
    fn test_mdd_mgr() {
        let mut mgr = MddMgr::new();
        let zero = mgr.zero();
        let one = mgr.one();
        let two = mgr.val(2);
        let mut vars = HashMap::new();
        vars.insert("x".to_string(), vec![0, 1, 2]);
        vars.insert("y".to_string(), vec![0, 1, 2]);
        vars.insert("z".to_string(), vec![0, 1, 2]);
        // println!("vars: {:?}", mgr.vars.borrow());
        let rpn = "x y z + *";
        if let Ok(node) = mgr.rpn(rpn, vars) {
            println!("{}", node.dot());
        }
    }
}
