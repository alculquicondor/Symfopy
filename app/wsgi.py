# -*- coding: utf-8 -*-
import sys
import os

__DIR__ = os.path.dirname(__file__)
sys.path.append(__DIR__ + '/../vendor')
sys.path.append(__DIR__ + '/controllers')

from Symfopy.Component.Wsgi import WsgiApp

# sample routes
routes = {
    'main' : {
      'route' : '/',
      'controller' : 'main:main'
      },
    'greeter' : {
      'route' : '/greet/{name:.*}',
      'controller' : 'main:greet'
      },
    'hello' : {
      'route' : '/hello/',
      'controller' : 'main:hello'
      }
    }
        
application = WsgiApp(routes, debug = True)

