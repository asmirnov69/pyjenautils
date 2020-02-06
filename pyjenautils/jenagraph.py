#import ipdb
import pandas as pd
import jenaimports as ji
import conversions
import prefix
from ULB import *

class JenaGraph:
    def __init__(self, model = None):
        self.g = ji.ModelFactory.createDefaultModel() if model is None else model
        
    def read(self, ttl_fn):
        self.g.read(ttl_fn)

    def write(self, ttl_fn, format = "N-TRIPLES"):
        out_stream = ji.FileOutputStream(ttl_fn)
        out_w = ji.OutputStreamWriter(out_stream)
        self.g.write(out_w, format)
        out_w.close()

    def change_subject(self, subject_U, new_subject_U):
        subj_triples = self.triples(subject_U, None, None)
        new_subj_triples = [(new_subject_U, p, o) for s, p, o in subj_triples]
        self.remove_triples(subj_triples)
        self.add_triples(new_subj_triples)
        
    def add_triple(self, *ulb_triple):
        self.g.add(conversions.ULB_triple_to_jena_statement(ulb_triple))
        
    def add_triples(self, ulb_triples):
        self.g.add([conversions.ULB_triple_to_jena_statement(x) for x in ulb_triples])

    def remove_triples(self, ulb_triples):
        self.g.remove([conversions.ULB_triple_to_jena_statement(x) for x in ulb_triples])

    # will return ULB triples
    def triples(self, ulb_s, ulb_p, ulb_o):
        assert(isinstance(ulb_s, U) or isinstance(ulb_s, B) or ulb_s is None)
        assert(isinstance(ulb_p, U) or ulb_p is None)
        assert(isinstance(ulb_o, U) or isinstance(ulb_o, L) or ulb_o is None)

        if isinstance(ulb_s, U):
            s = ulb_s.jena_resource
        elif isinstance(ulb_s, B):
            s = ulb_s.jena_anon_resource
        else:
            s = None
        
        p = ji.ResourceFactory.createProperty(ulb_p.jena_resource.getURI()) if ulb_p else None

        if isinstance(ulb_o, U):
            o = ulb_o.jena_resource
        elif isinstance(ulb_o, L):
            o = ulb_o.jena_literal
        else:
            o = None

        it = self.g.listStatements(s, p, o)
        ret = []
        while it.hasNext():
            statement = it.next()
            conv = conversions.jena_object_to_ULB
            ret_t = (conv(statement.getSubject()), conv(statement.getPredicate()), conv(statement.getObject()))
            ret.append(ret_t)
        return ret
        
    def select(self, rq, initial_binding = None, convert_to_python = False):
        if initial_binding and not isinstance(initial_binding, dict):
            raise Exception("JenaGraph::select: initial_binding must be dictionary")
        rq = "\n".join(prefix.rq_prolog()) + "\n" + rq
        qf = ji.QueryFactory.create(rq)
        qexec = ji.QueryExecutionFactory.create(qf, self.g)
        if initial_binding:
            ## https://www.codota.com/code/java/methods/org.apache.jena.query.QueryExecution/setInitialBinding
            #QuerySolutionMap binding = new QuerySolutionMap();
            #binding.add("r", r);
            #qexec.setInitialBinding(binding);
            binding = ji.QuerySolutionMap()
            for k, v in initial_binding.items():
                assert(isinstance(v, U) or isinstance(v, L) or isinstance(v, B))
                binding.add(k, v.get())
            qexec.setInitialBinding(binding)
        results = qexec.execSelect()
        return conversions.rq_select_results_to_ulb_dataframe(results, convert_to_python)

    def construct(self, rq):
        rq = "\n".join(prefix.rq_prolog()) + "\n" + rq
        qf = ji.QueryFactory.create(rq)
        qexec = ji.QueryExecutionFactory.create(qf, self.g)
        new_m = qexec.execConstruct()
        return JenaGraph(new_m)
