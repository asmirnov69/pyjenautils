import os, tempfile

def dot_write(jena_graph, out_fn, fmt):
    #ipdb.set_trace()
    temp_fn = tempfile.NamedTemporaryFile(delete = True)
    jena_graph.write(temp_fn.name, format = "RDF/XML")
    dd = {'temp_fn': temp_fn.name, 'out_fn': out_fn, 'fmt': fmt}
    pipe_cmd = "cat {temp_fn} | rapper -q -i rdfxml -o dot - ex:ex | dot -x -T{fmt} -o {out_fn}".format(**dd)
    os.system(pipe_cmd)
