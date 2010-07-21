from google.appengine.api import memcache
from app.models.question import Question
from app.models.pagination import Pagination
from app.config.constant import *
import app.lib.sepy as sepy
import app.lib.deliciousapi as deliciousapi 
import app.utility.utils as utils
import web, re, logging

class UnsupportedServiceError(Exception):
    def __init__(self, service, message):
        self.args = (service, message)
        self.service = service
        self.message = message

class StackExchangeDownloader():
    def __init__(self, service):
        if service not in StackAuthDownloader.get_supported_services().keys:
            raise UnsupportedServiceError(service, UNSUPPORTED_SERVICE_ERROR)
        self.service = service
        self.api_endpoint = StackAuthDownloader.get_supported_services().info[self.service]['api_endpoint']
        self.retriever = sepy
        
    def get_question(self, question_id):  
        results = self.retriever.get_question(int(question_id), self.api_endpoint, body = True, comments = True, pagesize = 1)
        question = results["questions"]
        if len(question) > 0:
            return question[0]
        else:
            return None
    
    def get_question_title(self, question_id):  
        results = self.retriever.get_question(int(question_id), self.api_endpoint, pagesize = 1)
        question = results["questions"]
        if len(question) > 0:
            return question[0]['title']
        else:
            return None
    
    def get_question_quicklook(self, question_id):
        results = self.retriever.get_question(int(question_id), self.api_endpoint, body = True, comments = False, pagesize = 1)
        question = results["questions"]
        if len(question) > 0:
            return question[0]
        else:
            return None
    def get_answer_quicklook(self, answer_id):
        results = self.retriever.get_answer(int(answer_id), self.api_endpoint, body = True, comments = False, pagesize = 1)
        answer = results["answers"]
        if len(answer) > 0:
            return answer[0]
        else:
            return None
            
    def get_questions_by_tags(self, tagged, page):
        questions_by_tags = []
        results = self.retriever.get_questions_by_tags(";".join([web.net.urlquote(tag) for tag in tagged.strip().split()]), self.api_endpoint, page, pagesize = 30)
        questions = results["questions"]
        pagination = Pagination(results)
        for question in questions:
            questions_by_tags.append(Question(question['question_id'],
                                   "http://%s.com/questions/%d" % (self.service, question['question_id']),
                                   question['title'],
                                   question['tags'],
                                   utils.date_from(question['creation_date']),
                                   self.service,
                                   question['up_vote_count'],
                                   question['down_vote_count'],
                                   question['answer_count']
                                   ))
        return (questions_by_tags, pagination)

    def get_questions_by_votes(self, page):
        questions_by_votes = []
        results = self.retriever.get_questions(self.api_endpoint, page, pagesize = 30)
        questions = results["questions"]
        pagination = Pagination(results)
        for question in questions:
            questions_by_votes.append(Question(question['question_id'],
                                   "http://%s.com/questions/%d" % (self.service, question['question_id']),
                                   question['title'],
                                   question['tags'],
                                   utils.date_from(question['creation_date']),
                                   self.service,
                                   question['up_vote_count'],
                                   question['down_vote_count'],
                                   question['answer_count']
                                   ))
        return (questions_by_votes, pagination)     
           
    def get_answers(self, question_id):  
        answers = []
        page = 1
        while True:
            results = self.retriever.get_answers(int(question_id), self.api_endpoint, body = True, comments = True, pagesize = 50, page = page, sort = 'votes')
            answers_chunk = results["answers"] 
            answers = answers + answers_chunk
            if len(answers) == int(results["total"]):
                break
            else:
                page = page +1 
        return answers
        
    def get_users_by_id(self, user_id):   
        results = self.retriever.get_users_by_id(int(user_id), self.api_endpoint, page = 1, pagesize = 1)
        users = results['users']
        return users
        
    def get_users(self, username_filter):    
        results = self.retriever.get_users(web.net.urlquote(username_filter), self.api_endpoint, pagesize = 50)
        users = results['users']
        return users
    
    def get_favorites_questions(self, user_id, page): 
        favorites_questions = []
        results = self.retriever.get_favorites_questions(user_id, self.api_endpoint, page, pagesize= 30)
        questions = results["questions"]
        pagination = Pagination(results)
        for question in questions:
            favorites_questions.append(Question(question['question_id'],
                                   "http://%s.com/questions/%d" % (self.service, question['question_id']),
                                   question['title'],
                                   question['tags'], 
                                   utils.date_from(question['creation_date']),
                                   self.service,
                                   question['up_vote_count'],
                                   question['down_vote_count'],
                                   question['answer_count']
                                   ))
        return (favorites_questions, pagination)
        
    def get_tags(self, tag_filter):
        results = self.retriever.get_tags(tag_filter, self.api_endpoint, page = 1, pagesize = 10)
        tags = results['tags']
        return "\n".join([tag['name'] for tag in tags ])
   
class StackAuthDownloader():    
    @staticmethod    
    def get_supported_services():
        supported_services = memcache.get("supported_services")
        if supported_services is not None:
            return supported_services
        else:
            results = sepy.get_sites()
            supported_services = utils.get_supported_services(results['api_sites'])
            memcache.add("supported_services", supported_services, 7200) #Recheck at least every two hours
            return supported_services
        
class DeliciousDownloader():  
    def get_favorites_questions(self, username):
        result = [] 
        dapi = deliciousapi.DeliciousAPI()
        meta = dapi.get_user(username, max_bookmarks = 100)
        bookmarks = meta.bookmarks
        for bookmark in bookmarks:
            match = re.search('http://(%s)\.com/questions/(\d+)/' % ("|".join(StackAuthDownloader.get_supported_services().keys).replace(".","\.")), bookmark[0])
            if match:
                result.append(Question(match.group(2), bookmark[0], bookmark[2], bookmark[1], bookmark[4], match.group(1)))
        return result