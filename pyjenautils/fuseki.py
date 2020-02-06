#import ipdb
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
            prq = pss.asQuery()        
            qexec = self.conn.query(prq)
        
            results = qexec.execSelect()
            res = conversions.rq_select_results_to_ulb_dataframe(results, convert_to_python)
            qexec.close()
            return res
        except jnius.JavaException as e:
            raise e
            #raise exception.PyJenaUtilsException(e, "FusekiConnection::select failed\n" + e.__repr__())

    def construct(self, rq, initial_binding = None, convert_to_python = False):
        pss = conversions.create_parametrized_query(rq, initial_binding)
        rq = pss.asQuery()
        qexec = self.conn.query(rq)
                
        res_model = qexec.execConstruct()
        res = jg.JenaGraph(res_model).triples(None, None, None) if convert_to_python else res_model
        qexec.close()
        return res
    
    def update(self, rq, initial_binding = None):
        pss = conversions.create_parametrized_query(rq, initial_binding)
        rq = pss.asUpdate()
        self.conn.update(rq)
    
    def write_model(self, m, g_uri = None):
        if g_uri:
            self.conn.load(g_uri, m.g)
        else:
            self.conn.load(m.g)

    def write_graph(self, g, g_uri, append):
        if append:
            self.conn.load(g_uri.get().getURI(), g.g)
        else:
            self.conn.put(g_uri.get().getURI(), g.g)
            

