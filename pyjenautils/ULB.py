import prefix

class U:
    def __init__(self, uri = None):
        ex_uri = prefix.expand_uri(uri) if uri else None
        self.jena_resource = ji.ResourceFactory.createResource(ex_uri) if ex_uri else None

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
            if literal_dt_prefix in prefix.DFLT_PREFIXES_INV:
                literal_dt = prefix.DFLT_PREFIXES_INV[literal_dt_prefix]
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
    
