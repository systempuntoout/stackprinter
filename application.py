"""
    StackPrinter: The Stack Exchange Printer Suite
"""
from app.config.urls import urls
from app.config.constant import *
from app.core.APIdownloader import StackAuthDownloader
import app.utility.utils as utils
import logging
import web

logging.getLogger().setLevel(logging.ERROR)
    
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

#StackPrinter boot
app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
main = app.cgirun()



