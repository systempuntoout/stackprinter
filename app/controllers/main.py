from app.core.stackprinterdownloader import StackExchangeDownloader
from app.core.stackprinterdownloader import StackAuthDownloader
from app.core.stackprinterdownloader import UnsupportedServiceError
from app.core.stackprinterdownloader import DeliciousDownloader
from app.config.constant import NOT_FOUND_ERROR, GENERIC_ERROR, UNSUPPORTED_SERVICE_ERROR
import app.lib.sepy as sepy
import app.db.counter as dbcounter
import app.db.question as dbquestion
import app.utility.utils as utils
import logging, web, re
from google.appengine.ext import ereporter

ereporter.register_logger()

render = web.render 

class Index:
    """
    Homepage
    """
    def GET(self):
        questions_printed = web.utils.commify(dbcounter.get_count())
        return render.index(questions_printed)

class Export:
    """
    Export question to a printer friendly view
    """
    def POST(self):
        return self.GET()
    def GET(self):
        try:
            question_id = web.input(question = None)['question']
            service = web.input(service = None)['service']
            pretty_links =  web.input(prettylinks = 'true')['prettylinks']
            printer =  web.input(printer = 'true')['printer']
            link_to_home = web.input(linktohome = 'true')['linktohome']
            format = web.input(format = 'HTML')['format'] #For future implementations
            
            #Check for malformed request
            if not service or not question_id:
                return Index().GET()
            
            se_downloader = StackExchangeDownloader(service)
            question = se_downloader.get_question(question_id)
            
            if not question:
                return render.oops(NOT_FOUND_ERROR)
            else:
                answers = se_downloader.get_answers(question_id)

            try:
                #Stats
                dbcounter.increment()
                dbquestion.store_printed_question(question['question_id'], service, question['title'], question['tags'])
            except Exception, exception:
                logging.error(exception) #Just log and go ahead
                
            return render.export(service, question, answers, pretty_links == 'true', printer == 'true', link_to_home == 'true' )
        except (sepy.ApiRequestError, UnsupportedServiceError), exception:
            logging.error(exception)
            return render.oops(exception.message)
        except Exception, exception:
            logging.exception("Generic exception")
            return render.oops(GENERIC_ERROR)
      
class Favorites:
    """
    Show a list of favorites questions from different supported services
    """
    def POST(self):
        return self.GET()
    def GET(self):
        try:
            service = web.input(service = None)['service']     
            username = web.input(username = None)['username']
            page = web.input(page = 1)['page']
            user_id = web.input(userid = None)['userid']
            
            if not service:
                return render.favorites()
            
            if service in StackAuthDownloader.get_supported_services().keys:
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
                raise UnsupportedServiceError( service, UNSUPPORTED_SERVICE_ERROR)
        except (sepy.ApiRequestError, UnsupportedServiceError), exception:
            logging.error(exception)
            return render.oops(exception.message)
        except Exception, exception:
            logging.exception("Generic exception")
            return render.oops(GENERIC_ERROR)

class TopVoted:
    """
    Show a list of questions filtered by tags
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
                result, pagination = se_downloader.get_questions_by_votes(page)
                
            return render.topvoted_tagged(tagged.strip(), result, service, pagination)  
        except (sepy.ApiRequestError, UnsupportedServiceError), exception:
            logging.error(exception)
            return render.oops(exception.message)
        except Exception, exception:
            logging.exception("Generic exception")
            return render.oops(GENERIC_ERROR)

class TopPrinted:
    """
    Show a list of top printed questions 
    """
    def GET(self):
        try:
            result = []
            result = dbquestion.get_top_printed_question()
            return render.topprinted(result)  
        except Exception, exception:
            logging.exception("Generic exception")
            return render.oops(GENERIC_ERROR)

class About:
    """
    About StackPrinter
    """
    def GET(self):
        return render.about()