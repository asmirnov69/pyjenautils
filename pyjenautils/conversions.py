#import ipdb
import jenaimports as ji
import jenagraph as j
from collections import OrderedDict
import pandas as pd
import datetime
import prefix

def python_value_to_jena_literal__(v):
    ret = None
    if isinstance(v, str):
        ret = ji.ResourceFactory.createStringLiteral(v)
    elif isinstance(v, datetime.datetime):
        ret = ji.ResourceFactory.createTypedLiteral(v, ji.XSDDatatype.XSDdateTime)
    else:
        ret = ji.ResourceFactory.createTypedLiteral(v)
    return ret

def jena_literal_to_python_value__(jena_literal):
    l = jena_literal.asLiteral()
    dt_uri = l.getDatatypeURI()
    lexical_form = l.getLexicalForm()

    if len(lexical_form) == 0:
        return None

    xsd_prefix = "http://www.w3.org/2001/XMLSchema#"
    if dt_uri == xsd_prefix + "boolean":
        ret = lexical_form == "true"
    elif dt_uri == xsd_prefix + "string":
        ret = lexical_form
    elif dt_uri == xsd_prefix + "integer":
        ret = int(float(lexical_form))
    elif dt_uri == xsd_prefix + "float":
        ret = float(lexical_form)
    elif dt_uri == xsd_prefix + "decimal":
        ret = float(lexical_form)
    else:
        raise Exception("unknown xsd datatype uri %s" % dt_uri)
    return ret

def jena_object_to_ULB(jo):
    ret = None
    if jo.isURIResource():
        ret = j.U(); ret.set(jo.asResource())
    elif jo.isLiteral():
        ret = j.L(); ret.set(jo)
    elif jo.isAnon():
        ret = j.B(jo)
    else:
        #ipdb.set_trace()
        raise Exception("unknown rdfnode")
    return ret

def jena_object_to_python(jo):
    ret = None
    if jo.isURIResource():
        ret = jo.asResource().getURI()
    elif jo.isLiteral():
        ret = jena_literal_to_python_value__(jo)
    elif jo.isAnon():
        ret = "_:" + jo.toString()
    else:
        #ipdb.set_trace()
        raise Exception("unknown rdfnode")
    return ret
    

def ULB_triple_to_jena_statement(ulb_triple):
    s, p, o = ulb_triple

    if isinstance(s, j.U):
        jena_s = s.jena_resource
    elif isinstance(s, j.B):
        jena_s = s.jena_anon_resource
    else:
        raise Exception("ULB subject must be either U or B")

    if isinstance(p, j.U):
        jena_p = ji.ResourceFactory.createProperty(p.jena_resource.getURI())
    else:
        raise Exception("ULB predicate must be U")

    if isinstance(o, j.U):
        jena_o = o.jena_resource
    elif isinstance(o, j.B):
        jena_o = o.jena_anon_resource
    elif isinstance(o, j.L):
        jena_o = o.jena_literal
    else:
        raise Exception("ULB object must be either of U, B or L")

    #ipdb.set_trace()
    return ji.ResourceFactory.createStatement(jena_s, jena_p, jena_o)
                              

def rq_select_results_to_ulb_dataframe(results, convert_to_python):
    ret = []
    while results.hasNext():
        qs = results.nextSolution()
        qs_it = qs.varNames()
        row = {}
        while qs_it.hasNext():
            try:
                v = qs_it.next()
                n = qs.get(v)
                # qs.get(v) sometimes returns None for some internal sparql variables which are not part of query
                if n: 
                    if convert_to_python:
                        row[v] = jena_object_to_python(n)
                    else:
                        row[v] = jena_object_to_ULB(n)
            except ValueError as ex:
                raise

        ret.append(row)

    out_cols = results.resultVars.toArray()
    return pd.DataFrame.from_records(ret, columns = out_cols)

def create_parametrized_query(rq, initial_binding):
    pss = ji.ParameterizedSparqlString()
    for k, v in prefix.dflt_prefixes.items():
        pss.setNsPrefix(k, v)
    if initial_binding:
        for k, v in initial_binding.items():
            if isinstance(v, j.U):
                pss.setParam(k, v.jena_resource)
            elif isinstance(v, j.B):
                #pss.setParam(k, v.jena_anon_resource)
                raise Exception("can't bind blank node URI %s" % v )
            elif isinstance(v, j.L):
                pss.setLiteral(k, v.jena_literal)
            else:
                raise Exception("unknown value type for value %s" % v)                
    pss.setCommandText(rq)

    return pss
