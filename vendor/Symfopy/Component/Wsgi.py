# -*- coding: utf-8 *-
from Symfopy.Component.HttpFoundation import Request, Response
from Symfopy.Component.Routing import Router
from Symfopy.Component.Templating import has_template
from jinja2 import Environment, FileSystemLoader
import sys
import traceback


class WsgiApp(object):

    def __init__(self, routes, views_path = None, debug = False):
        self.template_env = Environment(loader=FileSystemLoader(views_path))\
                if views_path else None
        self.router = Router(routes)
        self.debug = debug

    def __call__(self, environ, start_response):
        request = Request.createFromEnviron(environ)
        response = Router.notfound('Path not found')
        for name in self.router.routes:
            regex, controller, vars = self.router.routes[name]
            match = regex.match(request.get_path_info())
            if match:
                urlvars = vars
                urlvars.update(match.groupdict())
                for k in urlvars:
                    urlvars[k] = urlvars[k].decode('utf-8')
                try:
                    if isinstance(controller, basestring):
                        controller = self.router.\
                                load_controller(controller)
                    template = has_template(controller, self.template_env, request, **urlvars)
                    if template:
                        response = controller(request, template, **urlvars)
                    else:
                        response = controller(request, **urlvars)
                    if isinstance(response, (basestring, list)):
                        response = Response(response)
                except Exception as e:
                    tb = traceback.format_list(\
                            traceback.extract_tb(sys.exc_traceback))
                    response = self.error(e, tb)
                break
        try:
            output = response.getContent()
            status = response.getStatusCode()
            headers = response.getHeaders()
        except Exception as e:
            tb = traceback.format_list(\
                    traceback.extract_tb(sys.exc_traceback))
            response = self.error(e, tb)
            output = response.getContent()
            status = response.getStatusCode()
            headers = response.getHeaders()

        start_response(status, headers)
        if isinstance(output, basestring):
            yield output if not response.encoding\
                else output.encode(response.encoding)
        elif isinstance(output, list):
            for ou in output:
                if isinstance(ou, basestring):
                    yield ou if not response.encoding\
                        else ou.encode(response.encoding)
        

    def error(self, exception, tb):
        content = ['<h1>An Error Ocurred</h1>']
        if self.debug:
            content.append('<h2>Traceback:</h2>')
            for x in tb:
                content.append('<p>' + x + '</p>')
            content.append('<p><strong>' +\
                    exception.__class__.__name__ + '</strong>: ' +\
                    str(exception) + '</p>')
        else:
            content.append('<p>Please contact the administrator</p>')
        return Response(content, 500)


