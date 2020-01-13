import jenaimports as ji
import jenagraph as jg
import conversions
import jnius, exception

class FusekiConnection:
    def __init__(self, fuseki_url):
        self.fuseki_url = fuseki_url
        builder = ji.RDFConnectionFuseki.create().destination(self.fuseki_url)
        self.conn = builder.build()

    def select(self, rq, initial_binding = None, convert_to_python = False):
        try:
            pss = conversions.create_parametrized_query(rq, initial_binding)
            rq = pss.asQuery()        
            qexec = self.conn.query(rq)
        
            results = qexec.execSelect()
            res = conversions.rq_select_results_to_ulb_dataframe(results, convert_to_python)
            qexec.close()
            return res
        except jnius.JavaException as e:
            raise exception.PyJenaUtilsException(e, "FusekiConnection::select failed")

    def construct(self, rq, initial_binding = None, convert_to_python = False):
        pss = conversions.create_parametrized_query(rq, initial_binding)
        rq = pss.asQuery()
        res_model = self.conn.queryConstruct(rq)
        g = jg.JenaGraph(res_model)
        return g.triples(None, None, None)
    
    def update(self, rq, initial_binding = None):
        pss = conversions.create_parametrized_query(rq, initial_binding)
        rq = pss.asUpdate()
        self.conn.update(rq)
    
    def write_model(self, m, g_uri = None):
        if g_uri:
            self.conn.load(g_uri, m.g)
        else:
            self.conn.load(m.g)
            

