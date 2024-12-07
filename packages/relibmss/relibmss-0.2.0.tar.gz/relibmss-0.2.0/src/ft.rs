// mod ft

use std::collections::HashMap;

use dd::bdd::*;
use dd::common::NodeId;
use dd::nodes::NonTerminal;

// pub fn kofn(bdd: &mut Bdd, k: usize, nodes: Vec<BddNode>) -> BddNode {
//     match k {
//         1 => _or(bdd, nodes),
//         _ if nodes.len() == k => _and(bdd, nodes),
//         _ => {
//             let tmp1 = kofn(bdd, k - 1, nodes[1..].to_vec());
//             let tmp2 = kofn(bdd, k, nodes[1..].to_vec());
//             bdd.ite(&nodes[0], &tmp1, &tmp2)
//         }
//     }
// }

// pub fn _and(bdd: &mut Bdd, nodes: Vec<BddNode>) -> BddNode {
//     let mut res = bdd.one();
//     for node in nodes.iter() {
//         res = bdd.and(&res, &node);
//     }
//     res
// }

// pub fn _or(bdd: &mut Bdd, nodes: Vec<BddNode>) -> BddNode {
//     let mut res = bdd.zero();
//     for node in nodes.iter() {
//         res = bdd.or(&res, &node);
//     }
//     res
// }

// prob
pub fn prob(bdd: &mut Bdd, node: &BddNode, pv: HashMap<String, f64>) -> f64 {
    let cache = &mut HashMap::new();
    _prob(bdd, &node, &pv, cache)
}

fn _prob(
    bdd: &mut Bdd,
    node: &BddNode,
    pv: &HashMap<String, f64>,
    cache: &mut HashMap<NodeId, f64>,
) -> f64 {
    let key = node.id();
    match cache.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match node {
                BddNode::Zero => 1.0,
                BddNode::One => 0.0,
                BddNode::NonTerminal(fnode) => {
                    let x = fnode.header().label();
                    let fp = pv.get(x).unwrap_or(&0.0).clone();
                    let low = _prob(bdd, &fnode[0], pv, cache);
                    let high = _prob(bdd, &fnode[1], pv, cache);
                    fp * low + (1.0 - fp) * high
                }
            };
            cache.insert(key, result);
            result
        }
    }
}

pub fn minsol(bdd: &mut Bdd, node: &BddNode) -> BddNode {
    let cache = &mut HashMap::new();
    _minsol(bdd, &node, cache)
}

fn _minsol(dd: &mut Bdd, node: &BddNode, cache: &mut HashMap<NodeId, BddNode>) -> BddNode {
    let key = node.id();
    match cache.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match node {
                BddNode::Zero => dd.zero(),
                BddNode::One => dd.one(),
                BddNode::NonTerminal(fnode) => {
                    let tmp = _minsol(dd, &fnode[1], cache);
                    let high = dd.setdiff(&tmp, &fnode[0]);
                    let low = _minsol(dd, &fnode[0], cache);
                    dd.create_node(fnode.header(), &low, &high)
                }
            };
            cache.insert(key, result.clone());
            result
        }
    }
}

pub fn extract(bdd: &mut Bdd, node: &BddNode) -> Vec<Vec<String>> {
    let mut pathset = Vec::new();
    _extract(node, &mut Vec::new(), &mut pathset);
    pathset
}

fn _extract(node: &BddNode, path: &mut Vec<String>, pathset: &mut Vec<Vec<String>>) {
    match node {
        BddNode::Zero => (),
        BddNode::One => pathset.push(path.clone()),
        BddNode::NonTerminal(fnode) => {
            let x = fnode.header().label();
            path.push(x.to_string());
            _extract(&fnode[1], path, pathset);
            path.pop();
            _extract(&fnode[0], path, pathset);
        }
    }
}
