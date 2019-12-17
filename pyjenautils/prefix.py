import jenaimports as ji

# use add_prefix func defined below to add prefixes
dflt_prefixes = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'sh': "http://www.w3.org/ns/shacl#",
    'alg': 'http://drakon.su/ADF#'
}
dflt_prefixes_inv = {v:k for k, v in dflt_prefixes.items()}

def expand_curi(curi):
    idx = curi.find(":")
    prefix = curi[:idx]
    if prefix in dflt_prefixes:
        ret = dflt_prefixes[prefix] + curi[idx+1:]
    else:
        ret = curi
    return ret
        
def rq_prolog():
    prefixes = dflt_prefixes
    prolog = []
    for prefix, prefix_uri in prefixes.items():
        prolog.append("prefix %s: <%s>" % (prefix, prefix_uri))
    return prolog

def get_prefix_map__(d):
    pm = ji.PrefixMapFactory.create()
    for prefix, prefix_uri in d.items():
        pm.add(prefix, prefix_uri)
    return pm

PREFIX_MAP = get_prefix_map__(dflt_prefixes)

def add_prefix(prefix_value, prefix_uri):
    global dflt_prefixes, dflt_prefixes_inv, PREFIX_MAP
    dflt_prefixes[prefix_value] = prefix_uri
    dflt_prefixes_inv = {v:k for k, v in dflt_prefixes.items()}
    PREFIX_MAP = get_prefix_map__(dflt_prefixes)
    
