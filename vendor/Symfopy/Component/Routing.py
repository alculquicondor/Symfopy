# -*- coding: utf-8 *-
import pprint
import re
import sys
import importlib
from Symfopy.Component.HttpFoundation import Request, Response

class Router(object):

    var_regex = re.compile(r'\{(\w+)(?::([^}]+))?\}')

    def __init__(self, routes = {}):
        self.routes = dict()
        for name in routes:
            vars = routes[name].get('defaults', {})
            self.add_route(name, routes[name]['route'],\
                    routes[name]['controller'], **vars)

    def load_controller(self, string):
        module_name, func_name = string.split(':', 1)
        module = importlib.import_module(module_name)
        #__import__(module_name)
        #module = sys.modules[module_name]
        func = getattr(module, func_name)
        return func

    def add_route(self, name, route, controller, **vars):
        #if isinstance(controller, basestring):
        #    controller = self.load_controller(controller)
        self.routes[name] = (re.compile(self.template_to_regex(route)),
                controller, vars)

    @staticmethod
    def template_to_regex(template):
        regex = ''
        last_pos = 0
        for match in Router.var_regex.finditer(template):
            regex += re.escape(template[last_pos:match.start()])
            var_name = match.group(1)
            expr = match.group(2) or '[^/]+'
            expr = '(?P<%s>%s)' % (var_name, expr)
            regex += expr
            last_pos = match.end()
        regex += re.escape(template[last_pos:])
        regex = '^%s$' % regex
        return regex

    def __str__(self):
        return pprint.pformat(self.__dict__)

    @staticmethod
    def notfound(message = None, **kwargs):
        content = ['<h1>Not Found</h1>']
        if isinstance(message, basestring):
            content.append('<p>'+ message + '</p>')
        elif isinstance(message, list):
            for x in message:
                if isinstance(x, basestring):
                    content.append('<p>'+ x + '</p>')
        return Response(content, 404)


def rest_controller(cls):
    def replacement(request, **urlvars):
        action = urlvars.get('action', None)
        if action:
            action += '_' + request.get_method().lower()
            urlvars.pop('action')
        else:
            if isinstance(action, basestring):
                urlvars.pop('action')
            action = request.get_method().lower()
        instance = cls(request, **urlvars)
        try:
            method = getattr(instance, action)
        except Exception:
            return Router.notfound('No action ' + action)
        return method()
    return replacement


