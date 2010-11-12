from datetime import datetime
from app.lib import BeautifulSoup as Bs
from app.db.token import Token
from google.appengine.api import memcache
import re


def date_from(timestamp):
    """Format the given timestamp""" 
    return datetime.fromtimestamp(timestamp)

def get_inner_node_value(node):
    if node.string is None:        
        return get_inner_node_value(node.next)    
    else:        
        return node.string

def suppify_body(body):
    """Return supped body with sups and links"""
    count = 1
    links_dict = {}
    soup = Bs.BeautifulSoup(body)
    for link_tag in soup.findAll('a'):
        inner_node_value = get_inner_node_value(link_tag)    
        if link_tag.has_key('href') and len(link_tag['href']) > 0 and inner_node_value.strip()!= '' and link_tag['href'].upper() != inner_node_value.upper():
                links_dict[count]  = link_tag['href']          
                link_tag.replaceWith( link_tag.prettify() + '<sup style="font-size:9px">[%d]</sup>' % count )          
                count += 1
    return (soup,links_dict)

class SupportedServices():
    """Stackauth sites representation"""
    def __init__(self):
        self.keys = []
        self.info = {}
    
def get_supported_services(sites):
    """Return a SupportedServices object parsing /sites returned from Stackauth""" 
    services_key_mapping_list = []
    supported_services = SupportedServices()
    for site in sites:
        key = re.match('^http://(.*).com$',site['site_url']).group(1)
        supported_services.keys.append(key)
        services_key_mapping_list.append((key, site))
    supported_services.info = dict(services_key_mapping_list)
    'need to order keys'
    supported_services.keys = order_supported_services_keys(supported_services.keys)
    return supported_services
    
    
def order_supported_services_keys(keys):
    """Return an ordered list of supported services keys returned from Stackauth""" 
    ordered_keys = []
    keys.remove('stackoverflow')
    keys.remove('meta.stackoverflow')
    keys.remove('serverfault')
    keys.remove('meta.serverfault')
    keys.remove('superuser')
    keys.remove('meta.superuser')
    keys.remove('stackapps')
    keys_stripped_meta = [key for key in keys if not key.startswith('meta.')]
    keys_stripped_meta.sort()
    keys_added_meta = [prefix+key for key in keys_stripped_meta for prefix in ('','meta.')]
    ordered_keys.append('stackoverflow')
    ordered_keys.append('superuser')
    ordered_keys.append('serverfault')
    ordered_keys.append('stackapps') 
    ordered_keys.append('meta.stackoverflow')
    ordered_keys.append('meta.serverfault')
    ordered_keys.append('meta.superuser')  
    ordered_keys = ordered_keys + keys_added_meta
    return ordered_keys    

class Pagination(object):
    def __init__(self, results):
        self.total = results.get('total',0)
        self.page = results.get('page',0)
        self.pagesize = results.get('pagesize',0)
        self.total_pages = 0 if self.total==0 else 1 if (self.total / self.pagesize == 0) else (self.total / self.pagesize) \
                             if (self.total % self.pagesize == 0) else (self.total / self.pagesize) + 1
        self.separator = "..."

    def has_more_entries(self):
        return (self.page < self.total_pages)
    def has_previous_entries(self):
        return (self.page > 1)
    def get_pretty_pagination(self):
        """
            Return a list of int representing page index like:
            [1, -1 , 6 ,  7 , 8 , -1 , 20]
            -1 is where separator will be placed
        """
        pagination = []
        if self.total_pages == 1:
            return pagination
        pagination.append(1)
        if self.page > 2:
            if ( self.total_pages > 3 and self.page > 3 ):
                pagination.append(-1)
            if self.page == self.total_pages and self.total_pages > 3 :
                pagination.append(self.page - 2)
            pagination.append(self.page - 1)
        if self.page != 1 and self.page != self.total_pages :
            pagination.append(self.page)
        if self.page < self.total_pages - 1 :
            pagination.append(self.page + 1)
            if  self.page == 1 and self.total_pages > 3:
                pagination.append(self.page + 2)
            if ( self.total_pages > 3 and self.page < self.total_pages - 2 ):
                pagination.append(-1)
        pagination.append(self.total_pages)
        return pagination

class TokenManager():
    @staticmethod
    def store_auth_token(auth_token_value):
        """Save the passed token to datastore and to memcache"""
        if Token(key_name = 'authtoken', value = auth_token_value).put():
            memcache.set('authtoken', auth_token_value)
            return True
        else:
            return False
    @staticmethod
    def get_auth_token():
        """Get the auth token from memcache and from datastore if necessary saving again to memcache """
        auth_token_value = memcache.get('authtoken')
        if not auth_token_value:
            entity = Token.get_by_key_name(key_names = 'authtoken')
            if entity:
                auth_token_value= entity.value
                memcache.set('authtoken', auth_token_value)
            else:
                auth_token_value = None
        return auth_token_value
