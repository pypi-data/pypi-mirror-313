import relibmss as ms

def test_test2():
    bdd = ms.BddMgr()
    x, y, z = bdd.vars(["x", "y", "z"])
    v = bdd.rpn("x y z & &")
    assert v is not None  # RPN結果がNoneでないことを確認
    
    n = v.mcs()
    print(n.dot())
    print(n.extract())
    assert n is not None  # MCS結果がNoneでないことを確認
    
    probability = v.prob({"x": 0.1, "y": 0.2, "z": 0.01})
    assert 0 <= probability <= 1  # 確率が妥当な範囲内であることを確認
    
    extracted = n.extract()
    assert extracted is not None  # 抽出結果がNoneでないことを確認
