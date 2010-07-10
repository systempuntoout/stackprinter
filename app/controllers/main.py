from app.core.APIdownloader import StackExchangeDownloader
from app.core.APIdownloader import DeliciousDownloader
from app.config.constant import *
import app.lib.sopy as sopy
import app.db.counter as counter
import app.utility.utils as utils
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
            format = web.input(format = 'HTML')['format'] #For future implementations
            
            se_downloader = StackExchangeDownloader(service)
            question = se_downloader.get_question(question_id)
            
            if not question:
                return render.oops(NOT_FOUND_ERROR)
            else:
                answers = se_downloader.get_answers(question_id)
            
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
            
            if service in sopy.supported_services:
                if username:
                    match = re.search('.+\|(\d+)', username)
                    if match:
                        user_id = match.group(1)
                se_downloader = StackExchangeDownloader(service)
                if user_id:
                    users = se_downloader.get_users_by_id(user_id)
                else:
                    users = se_downloader.get_users(username)
                    
                if len(users) > 1:
                    return render.favorites_user_selection(users, service)
                elif len(users) == 1:
                    user_id = users[0]['user_id']
                    result, pagination = se_downloader.get_favorites_questions(user_id, page)
                    return render.favorites_stackexchange(users[0]['display_name'], user_id, result, service, pagination)
                else:
                    return render.favorites(message = NOT_FOUND_ERROR)    
            elif service == "delicious":
                    try:
                        delicious_downloader = DeliciousDownloader()
                        result = delicious_downloader.get_favorites_questions(username)
                        return render.favorites_delicious(username, result)
                    except:
                        return render.favorites(message = NOT_FOUND_ERROR)  
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
            if not service:
                return render.topvoted()
                
            se_downloader = StackExchangeDownloader(service)
            if tagged:
                result, pagination = se_downloader.get_questions_by_tags(tagged, page)
            else:
                result, pagination = se_downloader.get_questions(page)
            return render.topvoted_tagged(tagged.strip(), result, service, pagination)  
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