"""
    StackPrinter: The Stack Exchange Printer Suite
"""
import webob, urlparse
import logging,sys

from google.appengine.ext.webapp.util import run_wsgi_app

import web
from app.config.urls import urls
from app.config.constant import UNICORN_MESSAGE_ERROR, NOT_FOUND_ERROR, SERVER_ERROR
from app.core.stackprinterdownloader import StackAuthDownloader
import app.utility.utils as utils
import os

if 'app/libauth' not in sys.path:
    sys.path.insert(0, '/Users/micheletrimarchi/Project/GoogleAppEngine/stackprinter/app/libauth')
    sys.path.insert(1,'app/libauth')

web.render = render = web.template.render('app/views/', globals = {'date_from':utils.date_from,
                                               'suppify_body':utils.suppify_body,
                                               'commify': web.utils.commify,
                                               'urlquote':web.net.urlquote,
                                               'htmlquote':web.net.htmlquote,
                                               'supported_services': StackAuthDownloader.get_supported_services(),
                                               'ERROR_MESSAGE' : UNICORN_MESSAGE_ERROR,
                                               }, cache = True)
def notfound():
    return web.notfound(render.oops(NOT_FOUND_ERROR))
def internalerror():
    return web.internalerror(render.oops(SERVER_ERROR))

def redirect_from_appspot(wsgi_app):
    """Handle redirect to my domain if called from appspot (and not SSL)"""
    from_server = "stackprinter-hrd.appspot.com"
    from_server_oldMS = "stackprinter.appspot.com"
    to_server = "www.stackprinter.com"

    def redirect_if_needed(env, start_response):
        if (env["HTTP_HOST"].endswith(from_server) or env["HTTP_HOST"].endswith(from_server_oldMS)) and env["HTTPS"] == "off":
            # Parse the URL
            request = webob.Request(env)
            scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
            url = urlparse.urlunsplit([scheme, to_server, path, query, fragment])
            if not path.startswith('/admin'):
                start_response("301 Moved Permanently", [("Location", url)])
                return ["301 Moved Permanently", "Click Here %s" % url]
        return wsgi_app(env, start_response)
    return redirect_if_needed

app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
app = app.wsgifunc() 
app = redirect_from_appspot(app)
logging.getLogger().setLevel(logging.INFO)



