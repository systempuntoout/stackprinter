from google.appengine.api import memcache
from config.constant import *
import lib.sopy as sopy
import web


class JsonQuestion:
    """
    Return a Json formatted question's title
    """
    def GET(self):
        web.header('Content-type', 'application/json')
        try:
            question_id = web.input()['question']
            service = web.input()['service']
            title = memcache.get(str(question_id) + service)
            if title is  None:
                title = sopy.get_question(int(question_id), service, pagesize = 1)['title']
                memcache.add(str(question_id) + service, title)
            return '{"title":"%s"}' % title.replace('"','\\"')
        except Exception :
            return '{"title":"%s"}' % NOT_FOUND_ERROR