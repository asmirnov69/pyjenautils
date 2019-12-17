import os, jnius_config
jnius_config.set_classpath(os.path.join(os.getenv("JENA_HOME"), "lib/*"))
import jnius

System = jnius.autoclass('java.lang.System')
FileOutputStream = jnius.autoclass('java.io.FileOutputStream')
OutputStreamWriter = jnius.autoclass('java.io.OutputStreamWriter')

PrefixMapFactory = jnius.autoclass('org.apache.jena.riot.system.PrefixMapFactory')
ResourceFactory = jnius.autoclass('org.apache.jena.rdf.model.ResourceFactory')
ModelFactory = jnius.autoclass('org.apache.jena.rdf.model.ModelFactory')
QueryFactory = jnius.autoclass('org.apache.jena.query.QueryFactory')
QuerySolutionMap = jnius.autoclass('org.apache.jena.query.QuerySolutionMap')
PrefixMappingZero = jnius.autoclass('org.apache.jena.sparql.graph.PrefixMappingZero')
Algebra = jnius.autoclass('org.apache.jena.sparql.algebra.Algebra')
QueryExecutionFactory = jnius.autoclass('org.apache.jena.query.QueryExecutionFactory')
ResultSetFormatter = jnius.autoclass('org.apache.jena.query.ResultSetFormatter')

RDFNode = jnius.autoclass('org.apache.jena.rdf.model.RDFNode')
XSDDatatype = jnius.autoclass('org.apache.jena.datatypes.xsd.XSDDatatype')

RDFConnectionFuseki = jnius.autoclass('org.apache.jena.rdfconnection.RDFConnectionFuseki')
ParameterizedSparqlString = jnius.autoclass('org.apache.jena.query.ParameterizedSparqlString')
