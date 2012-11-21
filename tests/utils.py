import ujson
import fileinput

def read_docs(name):
    for line in fileinput.input():
        yield ujson.loads(line)

