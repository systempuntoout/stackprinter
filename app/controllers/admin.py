import logging, web, re
from google.appengine.api import urlfetch
from app.lib.key import api_key
from google.appengine.api import memcache
from app.core.stackprinterdownloader import StackAuthDownloader,StackExchangeDownloader
from app.utility.utils import TokenManager
from google.appengine.ext import deferred
import app.utility.worker as worker
from google.appengine.api.taskqueue import taskqueue
import app.db.question as dbquestion

VOTES_ENTRY_LEVEL = 15

render = web.render 

class Admin:
    """
    Admin homepage
    """
    def POST(self):
        return self.GET()
        
    def GET(self):
        result = {}
        action = web.input(action = None)['action']
        
        if action=='quota': 
            result = (urlfetch.fetch('http://api.stackoverflow.com/1.0/questions/9?pagesize=0&key=%s' % api_key, headers = {'User-Agent': 'StackPrinter','Accept-encoding': 'gzip, deflate'}, deadline = 10)).headers
        if action=='quotaauth': 
            result = (urlfetch.fetch('http://api.stackoverflow.com/1.0/questions/9?pagesize=0&key=%s&auth=%s' % (api_key, TokenManager.get_auth_token()), headers = {'User-Agent': 'StackPrinter','Accept-encoding': 'gzip, deflate'}, deadline = 10)).headers
        if action=='authkey': 
            result['result'] = TokenManager.get_auth_token()
        elif action =='memcachestats':
            result = memcache.get_stats()        
        elif action =='memcacheflush':
            result['result'] = memcache.flush_all()
        elif action =='normalize':
            deferred.defer(worker.deferred_normalize_printed_question)    
            result['result'] = True
        elif action =='delete':
            service = web.input(service = None)['service']
            question_id = web.input(question_id = None)['question_id']
            result['printed_question_deletion'] = dbquestion.delete_printed_question(question_id,service)
            result['question_deletion'] = dbquestion.delete_question(question_id,service)
            result['answers_deletion'] = dbquestion.delete_answers(question_id,service)
            
        return render.admin(result)

class AuthTokenRenewal:
    """
    Renew the Auth Token
    """
    def GET(self):
        result = {}
        result['result'] = StackAuthDownloader.renew_auth_token()
        return render.admin(result)

class TopQuestionsRetriever:
    """
    Retrieve the hottest questions (week by default)
    """
    def GET(self):
        
        result = {}
        service_parameter = web.input(service = None)['service']
        question_id_parameter = web.input(question_id = None)['question_id']
        sort_parameter = web.input(sort = 'week')['sort']
        pagesize_parameter = web.input(pagesize = 30)['pagesize']

        if service_parameter:
            se_downloader = StackExchangeDownloader(service_parameter)
            if question_id_parameter:
                se_downloader.get_post(question_id_parameter)
            else:
                questions = se_downloader.get_questions_by_hotness(pagesize = pagesize_parameter, 
                                                                   sort = sort_parameter)
                for question in questions:
                    question_id = int(question['question_id'])
                    score = int(question['score'])
                    if score > VOTES_ENTRY_LEVEL:
                        taskqueue.add(url='/admin/topquestionsretriever?service=%s&question_id=%s&sort=%s' % \
                                      (service_parameter, question_id, sort_parameter) , 
                                      method = 'GET', 
                                      queue_name = 'retriever')
        else:
            supported_services = StackAuthDownloader.get_supported_services()
            for service in supported_services.keys:
                if not service.startswith('meta.'):
                    taskqueue.add(url='/admin/topquestionsretriever?service=%s&sort=%s' % \
                                  (service, sort_parameter), 
                                  method = 'GET', 
                                  queue_name = 'retriever')
        result['result'] = True
        return render.admin(result)

        
class Warmup:
    """
    Warming Requests for avoiding latency
    """
    def GET(self):
        pass