# -*- coding: utf-8 *-
import pprint
import cgi
from urllib import unquote_plus


class Request(object):

    @staticmethod
    def createFromEnviron(environ):
        request = Request()
        request.__method = environ['REQUEST_METHOD']
        request.__pathInfo = environ['PATH_INFO']
        request.query = dict()
        if environ['QUERY_STRING']:
            for varval in environ['QUERY_STRING'].split('&'):
                try:
                    var, val = varval.split('=')
                    val = unquote_plus(val).decode('utf-8')
                except:
                    var = varval
                    val = 'true'
                if var in request.query:
                    tmp = request.query[var]
                    if isinstance(tmp, list):
                        request.query[var].append(val)
                    else:
                        request.query[var] = [tmp, val]
                else:
                    request.query[var] = val
        if request.__method == 'POST':
            post_env = environ.copy()
            post_env['QUERY_STRING'] = ''
            request.request = Request.fieldStorageToDict(\
                    cgi.FieldStorage(fp=environ['wsgi.input'],\
                        environ=post_env, keep_blank_values=True))
        else:
            request.request = request.query
        return request

    @staticmethod
    def fieldStorageToDict(fieldStorage):
        params = dict()
        for key in fieldStorage.keys():
            val = fieldStorage.getvalue(key)
            if isinstance(val, list):
                val = [x.decode('utf-8') for x in val]
            else:
                val = val.decode('utf-8')
            params[key] = val
        return params

    def __init__(self):
        self.__method = ''
        self.__pathInfo = ''
        self.request = dict()

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def get_method(self):
        return self.__method

    def get_path_info(self):
        return self.__pathInfo


class Response(object):

    statusCodes = {
        200: 'OK',
        404: 'Not Found',
        500: 'Internal Server Error',
        501: 'Not Implemented',
    }

    def __init__(self, content=[], statusCode=200, headers=None,\
        encoding = 'utf-8'):
        self.__content = content
        self.__statusCode = statusCode
        if headers:
            self.__headers = headers
        else:
            self.__headers = {
                'Content-Type': 'text/html'
            }
        self.encoding = encoding

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def getContent(self):
        return self.__content

    def setContent(self, content):
        self.__content = content

    def getStatusCode(self):
        return str(self.__statusCode) + ' ' + \
            self.statusCodes[self.__statusCode]

    def setStatusCode(self, statusCode):
        self.__statusCode = statusCode

    def setHeader(self, key, value):
        self.__headers[key] = value

    def getHeaders(self):
        return [(str(k), str(v)) for k, v in self.__headers.items()]

