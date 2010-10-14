from google.appengine.api import memcache
from app.config.constant import GENERIC_ERROR, NOT_FOUND_ERROR
from app.core.stackprinterdownloader import StackExchangeDownloader
from app.core.stackprinterdownloader import UnsupportedServiceError
import app.lib.sepy as sepy
import logging, web
from google.appengine.ext import ereporter

ereporter.register_logger()

class Question:
    """
    Return a Json formatted question's title
    """
    def GET(self):
        web.header('Content-type', 'application/json')
        try:
            question_id = web.input()['question']
            service = web.input()['service']
            title = memcache.get("%s%s" % (str(question_id), service))
            if title is  None:
                se_downloader = StackExchangeDownloader(service)
                title = se_downloader.get_question_title(question_id)
                memcache.add("%s%s" % (str(question_id), service), title, 7200)
            return '{"title":"%s"}' % title.replace('"','\\"')
        except Exception :
            return '{"title":"%s"}' % NOT_FOUND_ERROR
            
class Tags:
    """
    Return tags for auto completion
    """
    def GET(self):
        web.header('Content-type', 'text/plain')
        try:
            tag_filter = web.input()['q']
            service = web.input()['service']
            tags = memcache.get("%s|%s" % (tag_filter, service))
            if tags is  None:
                se_downloader = StackExchangeDownloader(service)
                tags = se_downloader.get_tags(tag_filter)
                memcache.add("%s|%s" % (tag_filter, service), tags)
            return tags
        except Exception, exception:
            return ""
            
class Quicklook:
    """
    Quicklook question and accepted_answer where available
    """
    def GET(self):
        try:
            render = web.render
            question_id = web.input()['question']
            service = web.input()['service']
            
            se_downloader = StackExchangeDownloader(service)
            question = se_downloader.get_question_quicklook(question_id)
            if not question:
                return render.oops(NOT_FOUND_ERROR)
                
            if question.has_key('accepted_answer_id'):
                accepted_answer = se_downloader.get_answer_quicklook(question['accepted_answer_id'])
            else:
                accepted_answer = None
                
            return render.quicklook(service, question, accepted_answer)
        except (sepy.ApiRequestError, UnsupportedServiceError), exception:
            logging.error(exception)
            return render.oops(exception.message)
        except Exception, exception:
            logging.exception("Generic exception")
            return render.oops(GENERIC_ERROR)
            
