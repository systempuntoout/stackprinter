#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Python Stack Overflow library customized for Google App Engine
"""
from django.utils import simplejson 
from google.appengine.api import urlfetch
from app.models.pagination import Pagination
from app.config.constant import *
import logging
try:
    from key import api_key
except ImportError: 
    logging.error(KEY_TEMPLATE_ERROR)

__api_version = '1.0'
__default_page_size = 100
__default_page = 1
#This should be updated when Stackauth will provide png with trasparent background 
supported_services_keys = ["stackoverflow","meta.stackoverflow","serverfault","superuser","stackapps","webapps.stackexchange", "meta.webapps.stackexchange",\
                            "gaming.stackexchange","meta.gaming.stackexchange","webmasters.stackexchange","meta.webmasters.stackexchange"]
supported_services = {"stackoverflow":"Stack Overflow", 
                      "meta.stackoverflow": "Meta Stack Overflow",
                      "serverfault" : "Server Fault", 
                      "superuser" : "Super User", 
                      "stackapps" : "Stack Apps",
                      "webapps.stackexchange" : "Web Apps",
                      "meta.webapps.stackexchange" : "Meta Web Apps",
                      "gaming.stackexchange" : "Gaming",
                      "meta.gaming.stackexchange" : "Meta Gaming",
                      "webmasters.stackexchange" : "Pro Webmasters",
                      "meta.webmasters.stackexchange" : "Meta Pro Webmasters"}

class ApiRequestError(Exception):
    def __init__(self, url, code, message):
        self.args = (url, code, message)
        self.url = url
        self.code = code
        self.message = message

class UnsupportedServiceError(Exception):
    def __init__(self, service, message):
        self.args = (service, message)
        self.service = service
        self.message = message

def get_question(question_id, service, body = False, comments = False, pagesize = 1):
    """
    Get the question of a given question_id 
    """
    path = "questions/%d" % question_id
    results = __fetch_results(path, service, body = body, comments = comments, pagesize = pagesize)
    question = results["questions"]
    if len(question) > 0:
        return question[0]
    else:
        return None
        
def get_answers(question_id, service, page = 1, body = False, comments = False, pagesize = 100, sort = 'votes'):
    """
    Get the answers list of a given question_id 
    """
    answers = []
    path = "questions/%d/answers" % question_id
    while True:
        results = __fetch_results(path, service, body = body, page = page, comments = comments, pagesize = pagesize, sort = sort)
        answers_chunk = results["answers"] 
        answers = answers + answers_chunk
        if len(answers) == int(results["total"]):
            break
        else:
            page = page +1 
    return answers

def get_favorites_questions(user_id, service, page = 1, body = False, comments = False, pagesize = 100, sort = 'added'):
    """
    Get the favorites questions list of a given user_id
    """
    path = "users/%d/favorites" % user_id
    results = __fetch_results(path, service, body = body, page = page, comments = comments, pagesize = pagesize, sort = sort)
    questions = results["questions"]
    return questions, Pagination(results)

def get_questions_by_tags(tagged, service, page = 1, pagesize = 30, sort = 'votes'):
    """
    Get questions list filtered by tags
    """
    path = "questions" 
    results = __fetch_results(path, service, tagged = tagged, page = page, pagesize = pagesize, sort = sort)
    questions = results["questions"]
    return questions, Pagination(results)

def get_users(filter, service, page = 1, pagesize = 30, sort = 'reputation'):
    """
    Get a list of users filtered by display name
    """
    path = "users"
    results = __fetch_results(path, service, filter= filter, page = page, pagesize = pagesize, sort = sort)
    users = results['users']
    return users

def get_tags(filter, service, page = 1, pagesize = 10, sort = 'popular'):
    """
    Get a list of tags filtered by text
    """
    path = "tags"
    results = __fetch_results(path, service, filter= filter, page = page, pagesize = pagesize, sort = sort)
    tags = results['tags']
    return tags

def get_users_by_id(user_id, service, page = 1, pagesize = 30, sort = 'reputation'):
    """
    Get a users of a given user_id
    """
    path = "users/%d" % user_id
    results = __fetch_results(path, service, id = user_id, page = page, pagesize = pagesize, sort = sort)
    users = results['users']
    return users

def __fetch_results(path, service, **url_params):
    """
    Fetch results
    """
    params = {
        "key": api_key,
        "pagesize": __default_page_size,
        "page": __default_page
        }

    params.update(url_params)

    url = __build_url(path, service, **params)
    
    if service not in supported_services.keys():
        raise UnsupportedServiceError(service, UNSUPPORTED_SERVICE_ERROR)
    
    result = urlfetch.fetch(url, headers = {'User-Agent': 'StackPrinter','Accept-encoding': 'gzip, deflate'}, deadline = 10)
    response = simplejson.loads(result.content)
    if "error" in response:
        error = response["error"]
        code = error["code"]
        message = error["message"]
        raise ApiRequestError(url, code, message)
    return response

def __build_url(path, service, **params):
    """
    Builds the API URL for fetching results.
    """
    query = ["%s=%s" % (key, params[key]) for key in params if params[key]]
    query_string = "&".join(query)
    url = "http://api.%s.com/%s/%s?" % (service, __api_version, path)
    url += query_string
    return url