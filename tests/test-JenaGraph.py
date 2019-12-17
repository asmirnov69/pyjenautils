import sys
sys.path.append("..")
from pyjenautils import jenagraph as j, output, jenaimports as ji, conversions, prefix

def test1():
    g = j.JenaGraph()
    g.read("./data/test.ttl")
    output.dot_write(g, "./data/test.png", "png")

def test2():
    g = j.JenaGraph()
    pmm = g.g.getNsPrefixMap()
    if 0: print "after model created:", zip(pmm.keySet().toArray(), pmm.values().toArray())

    g.read("./data/test.ttl")
    pmm = g.g.getNsPrefixMap()
    if 0: print "after read from ttl with prefixes:", zip(pmm.keySet().toArray(), pmm.values().toArray())

    df = g.select("select * { ?s ?p ?o }")
    print df
    print df.dtypes

def test3():
    g = j.JenaGraph()
    g.read("./data/d-nops.ttl")
    rqs = ["select ?s (count(*) as ?c) where {?s ?p ?o} group by ?s",
           "select ?s ?o ?p where {?s ?p ?o}"]
    for rq in rqs:
        print "RQ:", rq
        print g.select(rq)
        print g.select(rq, convert_to_python = True)
    
    output.dot_write(g, "./data/d-nops.png", "png")
    gg = g.construct("construct { ?s ?p ?o } where { ?s ?p ?o filter(STRSTARTS(STR(?p), 'http://drakon.su/ADF#')) }")
    output.dot_write(gg, "./data/d-nops-brief.png", "png")

def test4():
    pm = prefix.PREFIX_MAP
    pmm = pm.getMappingCopyStr()
    print type(pm)
    print zip(pmm.keySet().toArray(), pmm.values().toArray())
    print pm.expand("alg:start"), pm.abbreviate(pm.expand("alg:start"))
    print pm.expand("rdf:type"), pm.abbreviate(pm.expand("rdf:type"))
    print pm.expand("rdf:label"), pm.abbreviate(pm.expand("rdf:label"))
    print pm.expand("hello:w"), pm.abbreviate("hello:w")

def test5():
    g = j.JenaGraph()
    g.read("./data/d-nops.ttl")
    triple_masks = [(None, None, None), (None, j.U("rdf:type"), None),
                    (j.U("e:nop1"), None, None), (None, None, j.L("End")),
                    (None, None, j.U("rdf:yes")), (j.U("e:nop1-start"), j.U("alg:next"), None)]
    c = 0
    for t in triple_masks:
        print c, g.triples(*t)
        c += 1

def test6():
    g = j.JenaGraph()
    g.read("./data/d-nops.ttl")
    ts = g.triples(j.U("e:nop1-start"), j.U("alg:next"), None)
    print ts[0][2]

    res = g.triples(ts[0][2], None, None)
    print res
    print len(res)

    new_triples = [(ts[0][2], j.U("rdfs:label"), j.L("Chudo"))]
    g.add_triples(new_triples)
    res = g.triples(ts[0][2], None, None)
    print res
    print len(res)

    g.remove_triples(new_triples)
    res = g.triples(ts[0][2], None, None)
    print res
    print len(res)

def test7():
    g = j.JenaGraph()
    g.read("./data/d-nops.ttl")
    df = g.select("select * { ?s ?p ?o }", initial_binding = {'s': j.U("e:nop1-start")})
    print df
    print g.select("select * { ?s ?p ?o }", initial_binding = {'s': df.loc[0, 'o']}) # blank node in binding works
    print "===="
    print g.select("select * { ?s ?p ?o }", initial_binding = {'p': j.U("rdf:type")})
    print g.select("select * { ?s ?p ?o }", initial_binding = {'o': j.U("alg:AlgorithmEnd")})
    print g.select("select * { ?s ?p ?o }", initial_binding = {'o': j.L("Start")})

def test8():
    g = j.JenaGraph()
    g.read("./data/d-nops.ttl")
    nodes = g.select("select distinct ?s { ?s ?p ?o }")
    nodes_d = {}
    print nodes
    for node in nodes.itertuples():
        nodes_d[node.s] = True
    print nodes_d
    keys = sorted(nodes_d.keys())
    last_key = j.U(keys[-1].jena_resource.getURI())
    #last_key = keys[-1]
    for key in keys:
        print nodes_d[key], key

    print "LAST KEY:", last_key, last_key in nodes_d, nodes_d[last_key] if last_key in nodes_d else None
    print [isinstance(x.get(), ji.RDFNode) for x in nodes_d.keys()]
    
if __name__ == "__main__":    
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    #test8()
