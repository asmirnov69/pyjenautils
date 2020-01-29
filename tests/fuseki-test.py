import fuargs
import sys, time
sys.path.append("..")
from pyjenautils import fuseki, prefix
from pyjenautils.ULB import U

@fuargs.action
def test():
    conn = fuseki.FusekiConnection("http://localhost:3030/testdb")
    #rq = 'select * { ?s ?p ?q }'
    rq = 'select ?class_uri { ?class_uri rdf:type rdfs:Class }'
    for i in xrange(60):
        df = conn.select(rq, {})
        print i, df.shape
        #time.sleep(2)

@fuargs.action
def test_insert(v):
    conn = fuseki.FusekiConnection("http://localhost:3030/testdb")
    prefix.set_base_uri("pht:")
    rq = 'insert {  ?s <test> ?v } where {}'
    conn.update(rq, {"v": U(v), 's': U("aaa")})
    rq = 'select * { ?s <test> ?o }'
    df = conn.select(rq, {})
    print df
        
if __name__ == "__main__":
    fuargs.exec_actions(sys.argv[1:])
    
