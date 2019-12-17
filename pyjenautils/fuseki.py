import jenaimports as ji
import conversions

class FusekiConnection:
    def __init__(self, fuseki_url):
        self.fuseki_url = fuseki_url
        builder = ji.RDFConnectionFuseki.create().destination(self.fuseki_url)
        self.conn = builder.build()

    def select(self, rq, initial_binding = None, convert_to_python = False):
        pss = conversions.create_parametrized_query(rq, initial_binding)
        rq = pss.asQuery()        
        qexec = self.conn.query(rq)
        
        results = qexec.execSelect()
        res = conversions.rq_select_results_to_ulb_dataframe(results, convert_to_python)
        return res

    def update(self, rq, initial_binding = None):
        pss = conversions.create_parametrized_query(rq, initial_binding)
        rq = pss.asUpdate()
        self.conn.update(rq)
    
    def write_model(self, m, g_uri):
        self.conn.load(g_uri, m)

