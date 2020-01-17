import fuargs
import sys, time
sys.path.append("..")
from pyjenautils import fuseki

@fuargs.action
def test():
    conn = fuseki.FusekiConnection("http://localhost:3030/testdb")
    #rq = 'select * { ?s ?p ?q }'
    rq = 'select ?class_uri { ?class_uri rdf:type rdfs:Class }'
    for i in xrange(60):
        df = conn.select(rq)
        print i, df.shape
        #time.sleep(2)

@fuargs.action
def test_insert(v):
    conn = fuseki.FusekiConnection("http://localhost:3030/testdb")    
    rq = 'insert { graph <testdb:shacl-defs> { ?s <testdb:test> "%s" } } where { bind(<testdb:aaa> as ?s) }' % v
    conn.update(rq)
    rq = 'select * from <testdb:shacl-defs> { ?s <testdb:test> ?o }'
    df = conn.select(rq)
    print df
        
if __name__ == "__main__":
    fuargs.exec_actions(sys.argv[1:])
    
