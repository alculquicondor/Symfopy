# -*- coding: utf-8 *-

#sample controller

from Symfopy.Component.HttpFoundation import Request, Response
from Symfopy.Component.Routing import rest_controller_template
from Symfopy.Component.Templating import template, template_rest

@template('main.html')
def main(request, template):
    return template.render(title = u'Hello World')

def greet(request, name = 'Aldo'):
    return Response('<h1>Hello ' + name + '</h1>', 200,
            {'Content-Type' : 'text/html'})


@rest_controller_template
class Hello(object):

    def get(self, request):
        return '''<form method="POST">
        You're name: <input type="text" name="name">
        <input type="submit">
        </form>'''

    @template_rest('main.html')
    def post(self, request, template):
        return template.render(title = request.request['name'])


