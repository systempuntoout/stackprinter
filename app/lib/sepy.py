#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Python Stack Exchange library customized for Google App Engine
"""
import app.lib.simplejson as simplejson 
from google.appengine.api import urlfetch
from google.appengine.api.taskqueue import taskqueue
from google.appengine.api import memcache
from app.config.constant import KEY_TEMPLATE_ERROR
from app.config.constant import API_ERROR_AUTH_TOKEN_NOT_AUTHORIZED
from app.config.constant import API_ERROR_THROTTLING
from app.config.constant import CODE_API_ERROR_THROTTLING
from app.utility.utils import TokenManager
from datetime import datetime
import urllib
import logging
import os

try:
    from key import api_key, client_id, client_secret, code
except ImportError: 
    logging.error(KEY_TEMPLATE_ERROR)

__api_endpoint = 'https://api.stackexchange.com'
__api_version = '2.0'
__default_page_size = 100
__default_page = 1
__headers = {'User-Agent': 'StackPrinter'}
__debug = os.environ['SERVER_SOFTWARE'].startswith('Dev')

class ApiRequestError(Exception):
    def __init__(self, url, code, message):
        self.args = (url, code, message)
        self.url = url
        self.code = code
        self.message = message
            
def get_question(question_id, api_site_parameter, body = False, comments = False, pagesize = 1):
    """
    Get the question of a given question_id 
    """

    path = "questions/%d" % question_id
    
    query_filter = 'I9hR'
    
    if body:
        query_filter = '-m8CVE-h20D'
    if comments:
        query_filter = ')(Ybxr-pC9'
    if body and comments:
        query_filter = ')(YbxrpMgi'
    
    results = __fetch_results(path, api_site_parameter, filter = query_filter, pagesize = pagesize)
    return results

def get_questions_by_ids(question_ids, api_site_parameter, body = False, comments = False, pagesize = 1):
    """
    Get the question list of a given question_ids list
    """

    path = "questions/%s" % question_ids

    query_filter = 'I9hR'

    if body:
        query_filter = '-m8CVE-h20D'
    if comments:
        query_filter = ')(Ybxr-pC9'
    if body and comments:
        query_filter = ')(YbxrpMgi'

    results = __fetch_results(path, api_site_parameter, filter = query_filter, pagesize = pagesize)
    return results

def get_answer(answer_id, api_site_parameter, body = False, comments = False, pagesize = 1):
    """
    Get the answer of a given answer_id 
    """
    path = "answers/%d" % answer_id
    
    query_filter = ')(Y_v2R5Tz'
    
    if body:
        query_filter = '-m84pZ4-YWK'
    if comments:
        query_filter = ')(Ybxr-pC9'
    if body and comments:
        query_filter = 'D9kY06hX'
    
    results = __fetch_results(path, api_site_parameter, filter = query_filter, pagesize = pagesize)
    return results   
        
def get_answers(question_id, api_site_parameter, rpc = None, page = 1, body = False, comments = False, pagesize = 100, sort = 'votes'):
    """
    Get the answers list of a given question_id 
    """
    path = "questions/%d/answers" % question_id
    
    query_filter = '.p-I38n'
    
    if body:
        query_filter = '-m8C*uMP-q0'
    if comments:
        query_filter = ')(Ybp0wdAN'
    if body and comments:
        query_filter = 'D9l0ZsiD'
    if pagesize == 0:
        query_filter = '!-q2Rj6nE'
        
    results = __fetch_results(path, api_site_parameter, rpc = rpc, page = page, filter = query_filter, pagesize = pagesize, sort = sort)
    return results

def get_favorites_questions(user_id, api_site_parameter, page = 1, body = False, comments = False, pagesize = 100, sort = 'added'):
    """
    Get the favorites questions list of a given user_id
    """
    path = "users/%d/favorites" % user_id
    
    query_filter = ')(Ybxw_gbz'
    
    if body:
        query_filter = '9F)u(CSWCtKt'
    if comments:
        query_filter = ')(YbxuzQQ.'
    if body and comments:
        query_filter = ')(YbxuzQTp'
    
    results = __fetch_results(path, api_site_parameter, page = page, filter = query_filter, pagesize = pagesize, sort = sort)
    return results

def get_asked_questions(user_id, api_site_parameter, page = 1, body = False, comments = False, pagesize = 100, sort = 'creation'):
    """
    Get the asked questions list of a given user_id
    """
    path = "users/%d/questions" % user_id

    query_filter = ')(Ybxw_gbz'

    if body:
        query_filter = '9F)u(CSWCtKt'
    if comments:
        query_filter = ')(YbxuzQQ.'
    if body and comments:
        query_filter = ')(YbxuzQTp'

    results = __fetch_results(path, api_site_parameter, page = page, filter = query_filter, pagesize = pagesize, sort = sort)
    return results

def get_user_anwers(user_id, api_site_parameter, page = 1, pagesize = 100, sort = 'creation'):
    """
    Get the answers list of a given user_id
    """
    path = "users/%d/answers" % user_id
    
    query_filter = "!9hS0OLcgC"

    results = __fetch_results(path, api_site_parameter, page = page, filter = query_filter, pagesize = pagesize, sort = sort)
    return results


def get_questions_by_tags(tagged, api_site_parameter, page = 1, pagesize = 30, sort = 'votes'):
    """
    Get questions list filtered by tags
    """
    path = "questions" 
    
    query_filter = ')(Ybxw_gbz'
    
    results = __fetch_results(path, api_site_parameter, tagged = tagged, page = page, pagesize = pagesize, filter = query_filter, sort = sort)
    return results

def get_questions(api_site_parameter, page = 1, pagesize = 30, sort = 'votes'):
    """
    Get questions list sorted by votes
    """
    path = "questions"
    
    query_filter = ')(Ybxw_gbz'
     
    results = __fetch_results(path, api_site_parameter, page = page, pagesize = pagesize, filter = query_filter, sort = sort)
    return results

def get_users(filter, api_site_parameter, page = 1, pagesize = 30, sort = 'reputation'):
    """
    Get a list of users filtered by display name
    """
    path = "users"
    results = __fetch_results(path, api_site_parameter, inname= filter, page = page, pagesize = pagesize, sort = sort)
    return results

def get_tags(filter, api_site_parameter, page = 1, pagesize = 10, sort = 'popular'):
    """
    Get a list of tags filtered by text
    """
    path = "tags"
    
    query_filter = ')(Yb(vlSfU'
    
    results = __fetch_results(path, api_site_parameter, inname= filter, page = page, pagesize = pagesize, filter = query_filter, sort = sort)
    return results

def get_users_by_id(user_id, api_site_parameter, page = 1, pagesize = 30, sort = 'reputation'):
    """
    Get a users of a given user_id
    """
    path = "users/%d" % user_id
    results = __fetch_results(path, api_site_parameter, id = user_id, page = page, pagesize = pagesize, sort = sort)
    return results

def get_sites():
    """
    Get a list of Stack Exchange sites using Stackauth service
    """
    results = __gae_fetch('https://api.stackexchange.com/%s/sites?pagesize=999&key=%s' % (__api_version, api_key))
    response = simplejson.loads(results.content)
    return response

def get_auth_token():
    """
    Get the auth Token for authentication using Stackauth service
    """
    
    form_fields = {
      "client_id": client_id,
      "client_secret":client_secret,
      "code": code,
      "redirect_uri": "http://www.stackprinter.com"
    }
    form_data = urllib.urlencode(form_fields)
    results = __gae_fetch(url = 'https://stackexchange.com/oauth/access_token',
                          method = urlfetch.POST, 
                          payload = form_data,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
    response = results.content
    return response


def invalidate_auth_token(auth_token):
    """
    Invalidate the given auth_token
    """

    results = __gae_fetch('https://api.stackexchange.com/%s/access-tokens/%s/invalidate' % (__api_version, auth_token))
    response = simplejson.loads(results.content)
    return response

def __fetch_results(path, api_site_parameter, rpc = None, **url_params ):
    """
    Fetch results
    """
    
    #Backoff and respect the API
    if memcache.get('backoff') is not None:
        raise ApiRequestError(None, CODE_API_ERROR_THROTTLING, API_ERROR_THROTTLING)
    
    params = {
        "site": api_site_parameter,
        "key": api_key,
        "pagesize": __default_page_size,
        "page": __default_page
        }
    
    #Inject the auth token if valorized 
    if not __debug:
        auth_token = TokenManager.get_auth_token()
        if auth_token:
            params['access_token'] = auth_token
    
    params.update(url_params)

    url = __build_url(path, api_site_parameter, **params)
    
    results = __gae_fetch(url, rpc = rpc)
    if rpc:
        pass
    else:
        return handle_response(results, url)

def __build_url(path, api_site_parameter, **params):
    """
    Builds the API URL for fetching results.
    """
    
    query = ["%s=%s" % (key, params[key]) for key in params if (params[key] or key == 'pagesize') ]
    query_string = "&".join(query)
    url = "%s/%s/%s?" % (__api_endpoint, __api_version, path)
    url += query_string
    return url
    
def __gae_fetch(url, rpc = None, payload = None, method = urlfetch.GET, headers = None):
    if headers:
        custom_headers = dict(__headers.items() + headers.items()) 
    else:
        custom_headers = __headers
    if rpc:
        return urlfetch.make_fetch_call(rpc, url, headers = custom_headers, payload = payload, method = method)
    else:
        return urlfetch.fetch(url,  headers = custom_headers, deadline = 10, payload = payload, method = method)


def handle_response(results, url = None):
    """
    Load results in JSON
    """
    #When request is throttled, API simply closes the door without any response

    try:
        response = simplejson.loads(results.content)
    except:
        raise ApiRequestError(url, CODE_API_ERROR_THROTTLING, API_ERROR_THROTTLING) 
    if "backoff" in response:
        logging.info('Backoff warning found! Value: %s Url: %s' % (response["backoff"], url))
        memcache.set('backoff', response["backoff"],response["backoff"])
 
    if "error_id" in response:
        error = response["error_name"]
        code = response["error_id"]
        message = response["error_message"]
        raise ApiRequestError(url, code, message)
    return response    