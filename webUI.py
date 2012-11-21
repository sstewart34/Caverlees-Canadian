from bottle import route, run, template
import bottle
import json

@route('/')
def index():
    f = open('languages.txt', 'r')
    msg = ''
    for line in f.readlines():
        msg += line.lower().strip
    return msg

@route('/help')
def index():
    return '<b>Hello again Brady<b>!'

run(host='localhost', port=8080)
