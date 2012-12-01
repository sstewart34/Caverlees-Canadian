from bottle import route, run, template
from mako.template import Template
import bottle
import json

@route('/')
def index():
    open(jobs.json)
    #data = json.load(open(jobs.json))
    close(jobs.json)
    return Template("hello ${data}!").render(data="world")

@route('/help')
def index():
    return '<b>Hello again Brady<b>!'

run(host='localhost', port=8080)
