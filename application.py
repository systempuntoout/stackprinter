"""
    StackPrinter: The Stack Exchange Printer Suite
"""
import webob, urlparse
import logging

from google.appengine.ext.webapp.util import run_wsgi_app

import web
from app.config.urls import urls
from app.config.constant import UNICORN_MESSAGE_ERROR, NOT_FOUND_ERROR, SERVER_ERROR
from app.config.constant import TEX_ENABLED_SERVICES
from app.core.stackprinterdownloader import StackAuthDownloader
import app.utility.utils as utils



web.render = render = web.template.render('app/views/', globals = {'date_from':utils.date_from,
                                               'suppify_body':utils.suppify_body,
                                               'commify': web.utils.commify,
                                               'urlquote':web.net.urlquote,
                                               'htmlquote':web.net.htmlquote,
                                               'supported_services': StackAuthDownloader.get_supported_services(),
                                               'ERROR_MESSAGE' : UNICORN_MESSAGE_ERROR,
                                               'TEX_ENABLED_SERVICES' : TEX_ENABLED_SERVICES,
                                               }, cache = True)
def notfound():
    return web.notfound(render.oops(NOT_FOUND_ERROR))
def internalerror():
    return web.internalerror(render.oops(SERVER_ERROR))

def redirect_from_appspot(wsgi_app):
    """Handle redirect to my domain if called from appspot (and not SSL)"""
    from_server = "stackprinter-hrd.appspot.com"
    to_server = "www.stackprinter.com"

    def redirect_if_needed(env, start_response):
        if env["HTTP_HOST"].endswith(from_server) and env["HTTPS"] == "off":
            # Parse the URL
            request = webob.Request(env)
            scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
            url = urlparse.urlunsplit([scheme, to_server, path, query, fragment])
            if not path.startswith('/admin'):
                start_response("301 Moved Permanently", [("Location", url)])
                return ["301 Moved Peramanently", "Click Here %s" % url]
        return wsgi_app(env, start_response)
    return redirect_if_needed

app = web.application(urls, globals()).wsgifunc() 
app.notfound = notfound
app.internalerror = internalerror
logging.getLogger().setLevel(logging.ERROR)
app = redirect_from_appspot(app)



