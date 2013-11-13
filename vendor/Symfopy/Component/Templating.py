# -*- coding: utf-8 *-

from jinja2 import Environment

def template(name):
    def decorator(func):
        def replacement(request, template, **urlvars):
            return func(request, template, **urlvars)
        func.template_name = name
        return func
    return decorator

def has_template(func, template_env):
    if hasattr(func, 'template_name'):
        template = template_env.get_template(func.template_name)
        return template
    return None


