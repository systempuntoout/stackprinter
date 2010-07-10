import app.lib.sopy as sopy
from app.models.question import Question
import app.lib.deliciousapi as deliciousapi 
import app.utility.utils as utils
import web
import re

class StackExchangeDownloader():
    def __init__(self, service):
        self.service = service
        
    def get_question(self, question_id):  
        return sopy.get_question(int(question_id), self.service, body = True, comments = True, pagesize = 1)
    
    def get_question_title(self, question_id):  
        return sopy.get_question(int(question_id), self.service, pagesize = 1)['title']
    
    def get_question_quicklook(self, question_id):
        return sopy.get_question(int(question_id), self.service, body = True, comments = False, pagesize = 1)
        
    def get_answers(self, question_id):  
        return sopy.get_answers(int(question_id), self.service, body = True, comments = True, pagesize = 50, sort = 'votes')
        
    def get_users_by_id(self, user_id):   
        return sopy.get_users_by_id(int(user_id), self.service, page = 1, pagesize = 1)
        
    def get_users(self, username_filter):    
        return sopy.get_users(web.net.urlquote(username_filter), self.service, pagesize = 50)
    
    def get_favorites_questions(self, user_id, page): 
        result = []   
        favorite_questions = sopy.get_favorites_questions(user_id, self.service, page, pagesize= 30)
        questions = favorite_questions[0]
        pagination = favorite_questions[1]
        for question in questions:
            result.append(Question(question['question_id'],
                                   "http://%s.com/questions/%d" % (self.service, question['question_id']),
                                   question['title'],
                                   question['tags'], 
                                   utils.date_from(question['creation_date']),
                                   self.service,
                                   question['up_vote_count'],
                                   question['down_vote_count'],
                                   question['answer_count']
                                   ))
        return (result, pagination)
        
    def get_tags(self, tag_filter):
        return "\n".join([tag['name'] for tag in sopy.get_tags(tag_filter, self.service, page = 1, pagesize = 10)])
   
    def get_questions_by_tags(self, tagged, page):
        result = []
        top_voted_questions = sopy.get_questions_by_tags(";".join([web.net.urlquote(tag) for tag in tagged.strip().split()]), self.service, page, pagesize = 30)
        questions = top_voted_questions[0]
        pagination = top_voted_questions[1]
        for question in questions:
            result.append(Question(question['question_id'],
                                   "http://%s.com/questions/%d" % (self.service, question['question_id']),
                                   question['title'],
                                   question['tags'],
                                   utils.date_from(question['creation_date']),
                                   self.service,
                                   question['up_vote_count'],
                                   question['down_vote_count'],
                                   question['answer_count']
                                   ))
        return (result, pagination)
        
    def get_questions(self, page):
        result = []
        top_voted_questions = sopy.get_questions(self.service, page, pagesize = 30)
        questions = top_voted_questions[0]
        pagination = top_voted_questions[1]
        for question in questions:
            result.append(Question(question['question_id'],
                                   "http://%s.com/questions/%d" % (self.service, question['question_id']),
                                   question['title'],
                                   question['tags'],
                                   utils.date_from(question['creation_date']),
                                   self.service,
                                   question['up_vote_count'],
                                   question['down_vote_count'],
                                   question['answer_count']
                                   ))
        return (result, pagination)
        
        
class DeliciousDownloader():
    
    def get_favorites_questions(self, username):
        result = [] 
        dapi = deliciousapi.DeliciousAPI()
        meta = dapi.get_user(username, max_bookmarks = 100)
        bookmarks = meta.bookmarks
        for bookmark in bookmarks:
            match = re.search('http://(%s)\.com/questions/(\d+)/' % ("|".join(sopy.supported_services).replace(".","\.")), bookmark[0])
            if match:
                result.append(Question(match.group(2), bookmark[0], bookmark[2], bookmark[1], bookmark[4], match.group(1)))
        return result