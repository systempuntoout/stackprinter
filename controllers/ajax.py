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
            title = memcache.get("%s%s" % (str(question_id), service))
            if title is  None:
                title = sopy.get_question(int(question_id), service, pagesize = 1)['title']
                memcache.add("%s%s" % (str(question_id), service), title)
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
                tags = "\n".join([tag['name'] for tag in sopy.get_tags(tag_filter, service, page = 1, pagesize = 10)])
                memcache.add("%s|%s" % (tag_filter, service), tags)
            return tags
        except Exception, exception:
            return ""