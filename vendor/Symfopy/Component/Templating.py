# -*- coding: utf-8 *-

from jinja2 import Environment

def template(name):
    def decorator(func):
        def replacement(request, template, **urlvars):
            return func(request, template, **urlvars)
        func.template_name = name
        return func
    return decorator

def template_rest(name):
    def decorator(func):
        def replacement(self, request, template):
            return func(self, request, template)
        func.template_name = name
        return func
    return decorator

def has_template(func, template_env, request, **urlvars):
    if hasattr(func, 'member_func'):
        cls = func.member_func
        action = urlvars.get('action', None)
        if action:
            action += '_' + request.get_method().lower()
        else:
            action = request.get_method().lower()
        method = getattr(cls, action)
        if hasattr(method, 'template_name'):
            func.template_name = method.template_name

    if hasattr(func, 'template_name'):
        template = template_env.get_template(func.template_name)
        return template
    return None


