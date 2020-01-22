import jenaimports as ji

BASE_URI = [None]
# use add_prefix func defined below to add prefixes
DFLT_PREFIXES = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'sh': "http://www.w3.org/ns/shacl#",
    'alg': 'http://drakon.su/ADF#'
}
DFLT_PREFIXES_INV = {v:k for k, v in DFLT_PREFIXES.items()}

def set_base_uri(uri):
    print "setting base uri:", uri
    base_uri_ref = globals()['BASE_URI']
    base_uri_ref[0] = uri

def get_base_uri():
    base_uri_ref = globals()['BASE_URI']
    return base_uri_ref[0]

# uses simplified uri representation 
def expand_uri(uri):
    idx = uri.find(":")
    if idx == -1:
        if BASE_URI[0] != None:
            return BASE_URI[0] + uri
        else:
            raise Exception("expand_uri: BASE_URI is not set")
    
    prefix = uri[:idx]
    if prefix in DFLT_PREFIXES:
        ret = DFLT_PREFIXES[prefix] + uri[idx+1:]
    else:
        ret = uri
    return ret

def rq_prolog():
    prefixes = DFLT_PREFIXES
    prolog = []
    if BASE_URI[0] != None:
        prolog.append("base <%s>" % BASE_URI[0])
    for prefix, prefix_uri in prefixes.items():
        prolog.append("prefix %s: <%s>" % (prefix, prefix_uri))
    return prolog

def get_prefix_map__(d):
    pm = ji.PrefixMapFactory.create()
    for prefix, prefix_uri in d.items():
        pm.add(prefix, prefix_uri)
    return pm

PREFIX_MAP = get_prefix_map__(DFLT_PREFIXES)

def add_prefix(prefix_value, prefix_uri):
    global dflt_prefixes, dflt_prefixes_inv, PREFIX_MAP
    dflt_prefixes[prefix_value] = prefix_uri
    dflt_prefixes_inv = {v:k for k, v in dflt_prefixes.items()}
    PREFIX_MAP = get_prefix_map__(dflt_prefixes)
    
