from app.core.stackprinterdownloader import StackExchangeDownloader
from app.core.stackprinterdownloader import StackAuthDownloader
from app.core.stackprinterdownloader import UnsupportedServiceError
from app.core.stackprinterdownloader import DeliciousDownloader
from app.config.constant import NOT_FOUND_ERROR, GENERIC_ERROR, UNSUPPORTED_SERVICE_ERROR
import app.lib.sepy as sepy
import app.db.counter as dbcounter
import app.db.question as dbquestion
import app.utility.utils as utils
from app.utility.utils import cachepage
import logging, web, re
from google.appengine.ext import ereporter
import os

ereporter.register_logger()

render = web.render 

class Index:
    """
    Homepage
    """
    @cachepage()
    def GET(self):
        questions_printed = web.utils.commify(dbcounter.get_count())
        return render.index(questions_printed)

class Export:
    """
    Export question to a printer friendly view
    """
    def POST(self):
        question_id = web.input(question = None)['question']
        service = web.input(service = None)['service']
        return web.redirect('/export?question=%s&service=%s' % (question_id, service))
   
    def GET(self):
        try:
            
            question_id = web.input(question = None)['question']
            service = web.input(service = None)['service']
            pretty_links =  web.input(prettylinks = 'true')['prettylinks']
            printer =  web.input(printer = 'true')['printer']
            link_to_home = web.input(linktohome = 'true')['linktohome']
            format = web.input(format = 'HTML')['format'] #For future implementations
            
            #Check for malformed request
            if not service or not question_id or not question_id.isdigit():
                return Index().GET()
            
            se_downloader = StackExchangeDownloader(service)
            
            #Everything that comes outside the stackprinter homepage, stackoverflow and stackexchange is now heavily cached
            
            bypass_cache = False
            referrer = os.environ.get("HTTP_REFERER")
            if referrer:
                try:
                    referrer_key = re.match('^http://(.*).com',referrer).group(1)
                    if referrer_key in StackAuthDownloader.get_supported_services().keys or referrer in ('http://www.stackprinter.com/','http://stackprinter.appspot.com/'):
                        bypass_cache = True
                except:
                    pass

            post = se_downloader.get_post(question_id, bypass_cache)
            
            if post is None:
                return render.oops(NOT_FOUND_ERROR)
                
            return render.export(service, post, pretty_links == 'true', printer == 'true', link_to_home == 'true' )
        except (sepy.ApiRequestError, UnsupportedServiceError), exception:
            logging.error(exception)
            return render.oops(exception.message)
        except Exception, exception:
            logging.error("%s - Generic exception on question_id: %s" % (service, question_id))
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
    @cachepage()
    def GET(self):
        try:
            result = []
            page = web.input(page = 1)['page']
            result = dbquestion.get_top_printed_questions(page)
            count = dbquestion.get_top_printed_count()
            return render.topprinted(result, int(page), dbquestion.TOP_PRINTED_PAGINATION_SIZE, count)  
        except Exception, exception:
            logging.exception("Generic exception")
            return render.oops(GENERIC_ERROR)

class Deleted:
    """
    Show a list of deleted questions 
    """
    @cachepage()
    def GET(self):
        try:
            result = []
            result = dbquestion.get_deleted_questions()
            return render.deleted(result)  
        except Exception, exception:
            logging.exception("Generic exception")
            return render.oops(GENERIC_ERROR)

class About:
    """
    About StackPrinter
    """
    @cachepage()
    def GET(self):
        return render.about()