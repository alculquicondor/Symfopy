# -*- coding: utf-8 *-

#sample controller

from Symfopy.Component.HttpFoundation import Request, Response
from Symfopy.Component.Routing import rest_controller
from Symfopy.Component.Templating import template

@template('main.html')
def main(request, template):
    return template.render(title = u'Hello World')

def greet(request, name = 'Aldo'):
    return Response('<h1>Hello ' + name + '</h1>', 200,
            {'Content-Type' : 'text/html'})


@rest_controller
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


