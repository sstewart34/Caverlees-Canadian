import ujson
import fileinput

def read_docs():
    for line in fileinput.input():
        yield ujson.loads(line)

