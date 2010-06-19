"""
    StackPrinter: The StackOverflow Trilogy Printer Suite
"""
from google.appengine.api import memcache
from models.question import Question
from config.urls import urls
from config.constant import *
import lib.sopy as sopy
import utility.utils as utils
import logging
import web

logging.getLogger().setLevel(logging.DEBUG)
    
web.render = render = web.template.render('views/',globals={'date_from':utils.date_from,
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



