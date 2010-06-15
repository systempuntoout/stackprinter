from models.question import Question
from config.constant import *
import lib.sopy as sopy
import lib.deliciousapi as deliciousapi 
import db.counter as counter
import utility.utils as utils
import urllib
import logging
import web
import re

render = web.render 

class Index:
    """
    Homepage
    """
    def GET(self):
        questions_printed = web.utils.commify(counter.get_count())
        return render.index(questions_printed)

class Export:
    """
    Export question to a printer friendly view
    """
    def POST(self):
        return self.GET()
    def GET(self):
        try:
            question_id = web.input()['question']
            service = web.input()['service']
            pretty_links =  web.input(prettylinks = 'true')['prettylinks']
            printer =  web.input(printer = 'true')['printer']
            
            question = sopy.get_question(int(question_id), service, body = True, comments = True, pagesize = 1)
            if not question:
                return render.oops(NOT_FOUND_ERROR)
            else:
                answers = sopy.get_answers(int(question_id), service, body = True, comments = True, pagesize = 50, sort = 'votes')
            
            counter.increment()
            return render.export(service, question, answers, pretty_links == 'true', printer == 'true' )
        except (sopy.ApiRequestError, sopy.UnsupportedServiceError), exception:
            logging.error(exception)
            return render.oops(exception.message)
        except Exception, exception:
            logging.error(exception)
            return render.oops(GENERIC_ERROR)
      
class Favorites:
    """
    Show a lists of favorites questions from different supported services
    """
    def POST(self):
        return self.GET()
    def GET(self):
        try:
            service = web.input(service = None)['service']
            if not service:
                return render.favorites()
                
            username = web.input(username = None)['username']
            page = web.input(page = 1)['page']
            user_id = web.input(userid = None)['userid']
            
            result = []
            if service in sopy.supported_services:
                if username:
                    match = re.search('.+\|(\d+)', username)
                    if match:
                        user_id = match.group(1)
                if user_id:
                    users = sopy.get_users_by_id(int(user_id), service, page = 1, pagesize = 1)
                else:
                    users = sopy.get_users(urllib.quote(username.encode('utf-8')), service, pagesize = 50)
                    
                if len(users) > 1:
                    return render.favorites_user_selection(users, service)
                elif len(users) == 1:
                    user_id = users[0]['user_id'] 
                    favorite_questions = sopy.get_favorites_questions(user_id, service, page, pagesize= 30)
                    questions = favorite_questions[0]
                    pagination = favorite_questions[1]
                    for question in questions:
                        result.append(Question(question['question_id'],
                                               "http://%s.com/questions/%d" % (service, question['question_id']),
                                               question['title'],
                                               question['tags'], 
                                               utils.date_from(question['creation_date']),
                                               service,
                                               question['up_vote_count'],
                                               question['down_vote_count'],
                                               question['answer_count']
                                               ))
                    return render.favorites_trilogy(users[0]['display_name'], user_id, result, service, pagination)
                else:
                    render.favorites(message = NOT_FOUND_ERROR)    
            elif service == "delicious":
                    dapi = deliciousapi.DeliciousAPI()
                    meta = dapi.get_user(username, max_bookmarks = 100)
                    bookmarks = meta.bookmarks
                    for bookmark in bookmarks:
                        match = re.search('http://(%s)\.com/questions/(\d+)/' % ("|".join(sopy.supported_services).replace(".","\.")), bookmark[0])
                        if match:
                            result.append(Question(match.group(2), bookmark[0], bookmark[2], bookmark[1], bookmark[4], match.group(1)))
                    return render.favorites_delicious(username, result)
            else:
                raise sopy.UnsupportedServiceError( service, UNSUPPORTED_SERVICE_ERROR)
        except (sopy.ApiRequestError, sopy.UnsupportedServiceError), exception:
            logging.error(exception)
            return render.oops(exception.message)
        except Exception, exception:
                logging.error(exception)
                return render.oops(GENERIC_ERROR)

class TopVoted:
    """
    Show a lists of questions filtered by tags
    """
    def POST(self):
        return self.GET()
    def GET(self):
        try:
            result = []
            service = web.input(service = None)['service']
            tagged = web.input(tagged = None)['tagged']
            page = web.input(page = 1)['page']
            if not service or not tagged:
                return render.topvoted()
            
            top_voted_questions = sopy.get_questions_by_tags(";".join([urllib.quote(tag.encode('utf-8')) for tag in tagged.split()]), service, page, pagesize = 30)
            questions = top_voted_questions[0]
            pagination = top_voted_questions[1]
            for question in questions:
                result.append(Question(question['question_id'],
                                       "http://%s.com/questions/%d" % (service, question['question_id']),
                                       question['title'],
                                       question['tags'],
                                       utils.date_from(question['creation_date']),
                                       service,
                                       question['up_vote_count'],
                                       question['down_vote_count'],
                                       question['answer_count']
                                       ))
            return render.topvoted_tagged(tagged, result, service, pagination)  
        except (sopy.ApiRequestError, sopy.UnsupportedServiceError), exception:
            logging.error(exception)
            return render.oops(exception.message)
        except Exception, exception:
                logging.error(exception)
                return render.oops(GENERIC_ERROR)

class About:
    """
    About StackPrinter
    """
    def GET(self):
        return render.about()