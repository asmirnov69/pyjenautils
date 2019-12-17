#import ipdb
import pandas as pd
import jenaimports as ji
import conversions
import prefix

class U:
    def __init__(self, uri = None):
        self.jena_resource = ji.ResourceFactory.createResource(prefix.expand_curi(uri)) if uri else None

    def set(self, jena_resource_or_property):
        if not self.jena_resource is None:
            raise Exception("U::set jena_resource is already defined")
        if jena_resource_or_property.isResource():
            self.jena_resource = jena_resource_or_property
        elif jena_resource_or_property.isProperty():
            self.jena_resource = ji.ResourceFactory.createResource(jena_resource_or_property.getURI())
        else:
            raise Exception("U::set: unexpected jena_resource_or_property value %s" % jena_resource_or_property)

    def get(self):
        return self.jena_resource

    def __hash__(self):
        return self.jena_resource.asNode().hashCode()

    def __eq__(self, o):
        #print "__eq__"
        return self.jena_resource.asNode().hashCode() == o.jena_resource.asNode().hashCode()
    
    def __repr__(self):
        uri = self.jena_resource.getURI()
        if prefix.PREFIX_MAP:            
            abbr_uri = prefix.PREFIX_MAP.abbreviate(uri)
            if abbr_uri:
                visible_uri = "u(" + abbr_uri + ")"
            else:
                visible_uri = "U(" + uri + ")"
        else:
            visible_uri = "U(" + uri + ")"
        return visible_uri

class L:
    def __init__(self, python_value_ = None):
        self.jena_literal = conversions.python_value_to_jena_literal__(python_value_) if python_value_ else None

    def set(self, jena_literal):
        if not self.jena_literal is None:
            raise Exception("L::set: jena_literal is already defined")
        self.jena_literal = jena_literal

    def get(self):
        return self.jena_literal

    def __hash__(self):
        return self.jena_literal.asNode().hashCode()

    def __eq__(self, o):
        return self.jena_literal.asNode().hashCode() == o.jena_literal.asNode().hashCode()
    
    def __repr__(self):
        literal_dt = self.jena_literal.asLiteral().getDatatypeURI()
        literal = self.jena_literal.asLiteral().getLexicalForm()
        if literal_dt:
            literal_dt_prefix, suffix = literal_dt.split("#")
            literal_dt_prefix += "#"
            if literal_dt_prefix in prefix.dflt_prefixes_inv:
                literal_dt = prefix.dflt_prefixes_inv[literal_dt_prefix]
            ret = 'l("' + literal + '"^^' + literal_dt + ":" + suffix + ')'
        else:
            ret = 'L(' + literal + ')'
        return ret

class B:
    def __init__(self, jena_anon_resource_):
        if jena_anon_resource_.isAnon():
            self.jena_anon_resource = jena_anon_resource_.asResource()
        else:
            raise Exception("B can be used to represent anon resources")

    def get(self):
        return self.jena_anon_resource

    def __hash__(self):
        return self.jena_anon_resource.asNode().hashCode()

    def __eq__(self, o):
        return self.jena_anon_resource.asNode().sameValueAs(o.jena_anon_resource.asNode())
    
    def __repr__(self):
        return 'B(' + self.jena_anon_resource.toString() + ')'
    
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
