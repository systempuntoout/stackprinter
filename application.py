"""
    StackPrinter: The Stack Exchange Printer Suite
"""
from app.config.urls import urls
from app.config.constant import *
import app.lib.sopy as sopy
import app.utility.utils as utils
import logging
import web

logging.getLogger().setLevel(logging.ERROR)
    
web.render = render = web.template.render('app/views/',globals={'date_from':utils.date_from,
                                               'suppify_body':utils.suppify_body,
                                               'supported_services': sopy.supported_services,
                                               'supported_services_keys': sopy.supported_services_keys,
                                               'commify': web.utils.commify,
                                               'urlquote':web.net.urlquote,
                                               'htmlquote':web.net.htmlquote,
                                               'ERROR_MESSAGE' : UNICORN_MESSAGE_ERROR
                                               })
def notfound():
    return web.notfound(render.oops(NOT_FOUND_ERROR))
def internalerror():
    return web.internalerror(render.oops(SERVER_ERROR))

#StackPrinter boot
app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
main = app.cgirun()



