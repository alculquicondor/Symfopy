# -*- cmding: utf-8 -*-

#sample controller

from Symfopy.Component.HttpFoundation import Request, Response
from Symfopy.Component.Routing import rest_controller

def main(request):
  return Response('<h1>Hello World</h1>', 200, {
    'Content-Type': 'text/html'})

def greet(request, name = 'Aldo'):
  return '<h1>Hello ' + name + '</h1>'


class Hello(object):
    def __init__(self, request):
        self.request = request

    def get(self):
        return '''<form method="POST">
        You're name: <input type="text" name="name">
        <input type="submit">
        </form>'''

    def post(self):
        return 'Hello %s!' % self.request.request['name']


hello = rest_controller(Hello)

