import relibmss as ms

# def test_test1():
#     bdd = ms.BddMgr()
#     c = bdd.vars(["c" + str(i) for i in range(61)])
    
#     g62 = c[0] & c[1]
#     g63 = c[0] & c[2]
#     g64 = c[0] & c[3]
#     g65 = c[0] & c[4]
#     g66 = c[0] & c[5]
#     g67 = c[0] & c[6]
#     g68 = c[0] & c[7]
#     g69 = c[0] & c[8]
#     g70 = g62 | c[9]
#     g71 = g63 | c[10]
#     g72 = g64 | c[11]
#     g73 = g65 | c[12]
#     g74 = g62 | c[13]
#     g75 = g63 | c[14]
#     g76 = g64 | c[15]
#     g77 = g65 | c[16]
#     g78 = g62 | c[17]
#     g79 = g63 | c[18]
#     g80 = g64 | c[19]
#     g81 = g65 | c[20]
#     g82 = g62 | c[21]
#     g83 = g63 | c[22]
#     g84 = g64 | c[23]
#     g85 = g65 | c[24]
#     g86 = g62 | c[25]
#     g87 = g63 | c[26]
#     g88 = g64 | c[27]
#     g89 = g65 | c[28]
#     g90 = g66 | c[29]
#     g91 = g68 | c[30]
#     g92 = g67 | c[31]
#     g93 = g69 | c[32]
#     g94 = g66 | c[33]
#     g95 = g68 | c[34]
#     g96 = g67 | c[35]
#     g97 = g69 | c[36]
#     g98 = g66 | c[37]
#     g99 = g68 | c[38]
#     g100 = g67 | c[39]
#     g101 = g69 | c[40]
#     g102 = g66 | c[41]
#     g103 = g68 | c[42]
#     g104 = g67 | c[43]
#     g105 = g69 | c[44]
#     g106 = ms.kofn(3, [g70, g71, g72, g73])
#     g107 = ms.kofn(3, [g74, g75, g76, g77])
#     g108 = ms.kofn(3, [g78, g79, g80, g81])
#     g109 = ms.kofn(3, [g82, g83, g84, g85])
#     g110 = ms.kofn(3, [g86, g87, g88, g89])
#     g111 = ms.kofn(3, [g94, g95, g96, g97])
#     g112 = ms.kofn(3, [g98, g99, g100, g101])
#     g113 = g90 & g92
#     g114 = g91 & g93
#     g115 = g102 & g104
#     g116 = g103 & g105
#     g117 = g113 | c[45]
#     g118 = g114 | c[46]
#     g119 = g107 | g108 | c[51]
#     g120 = g109 | g110
#     g121 = g66 | g117 | c[47]
#     g122 = g68 | g118 | c[48]
#     g123 = g67 | g117 | c[49]
#     g124 = g69 | g118 | c[50]
#     g125 = ms.kofn(2, [g121, g123, g122, g124])
#     g126 = g111 | g112 | g125 | c[52]
#     g127 = g115 & g120
#     g128 = g116 & g120
#     g129 = g62 | g127 | c[53]
#     g130 = g63 | g128 | c[54]
#     g131 = g64 | g127 | c[55]
#     g132 = g65 | g128 | c[56]
#     g133 = g62 | g129 | c[57]
#     g134 = g63 | g130 | c[58]
#     g135 = g64 | g131 | c[59]
#     g136 = g65 | g132 | c[60]
#     g137 = ms.kofn(3, [g133, g134, g135, g136])
#     g138 = g106 | g119 | g137

#     assert bdd.size() > 0  # 簡単なチェックとしてBDDのサイズが0でないことを確認
#     n = g138.mcs()
#     assert n is not None  # mcsの結果がNoneでないことを確認

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
