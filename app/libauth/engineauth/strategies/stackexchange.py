from __future__ import absolute_import
import json
from engineauth.models import User
from engineauth.strategies.oauth2 import OAuth2Strategy
import re
import app.lib.key as key

class StackExchangeUser():

    """Associated user sites"""
    def __init__(self):
        self.main_site_key = ''
        self.associated_sites = {}
        self.associated_sites_keys = []

def order_supported_services_keys(keys):
    """Return an ordered list of supported services keys""" 
    ordered_keys = []
    so_removed = True
    sf_removed = True
    su_removed = True
    sa_removed = True
    
    try:
        keys.remove('stackoverflow')
    except:
        so_removed = False
    try:
        keys.remove('serverfault')
    except:
        sf_removed = False
    try:
        keys.remove('superuser')
    except:
        su_removed = False
    try:
        keys.remove('stackapps')
    except:
        sa_removed = False
    keys_stripped_meta = [key for key in keys if not key.startswith('meta.')] 
    keys_stripped_meta.sort()
    keys_added_meta = [prefix+key for key in keys_stripped_meta for prefix in ('','meta.')]
    
    if so_removed:
        ordered_keys.append('stackoverflow')
    if su_removed:
        ordered_keys.append('superuser')
    if sf_removed:
        ordered_keys.append('serverfault')
    if sa_removed:
        ordered_keys.append('stackapps')
    if so_removed:
        ordered_keys.append('meta.superuser')
    if su_removed:
        ordered_keys.append('meta.serverfault')
    if sf_removed:
        ordered_keys.append('meta.stackoverflow')
    ordered_keys = ordered_keys + keys_added_meta
    return ordered_keys
    
def get_stackexchange_user(sites):

    """Return a SupportedServices object parsing /sites returned from Stackauth"""
    services_key_mapping_list = []
    stackexchange_user = StackExchangeUser()
    for i, site in enumerate(sites):

        key = re.match('^http://(.*).com$',site['site_url']).group(1)
        stackexchange_user.associated_sites_keys.append(key)
        services_key_mapping_list.append((key, site))
        if i == 0 or (site['creation_date'] <= site_creation_date ):            
            site_creation_date = site['creation_date']
            stackexchange_user.main_site_key = key
        if key not in ('stackapps','stackoverflow','meta.stackoverflow'):
            services_key_mapping_list.append(('meta.'+key, site))
            stackexchange_user.associated_sites_keys.append('meta.'+key)
            
    stackexchange_user.associated_sites = dict(services_key_mapping_list)  
    stackexchange_user.associated_sites_keys = order_supported_services_keys(stackexchange_user.associated_sites_keys) 

    return stackexchange_user


class StackExchangeStrategy(OAuth2Strategy):

    @property
    def options(self):
        return {
            'provider': 'stackexchange',
            'site_uri': 'https://stackexchange.com',
            'auth_uri': 'https://stackexchange.com/oauth',
            'token_uri': 'https://stackexchange.com/oauth/access_token',
            }

    def user_info(self, req):
        url = "https://api.stackexchange.com/2.0/me/associated?pagesize=100&key=%s&access_token=%s" % (key.api_key, req.credentials.access_token)
        res, results = self.http(req).request(url)
        if res.status is not 200:
            return self.raise_error('There was an error contacting StackExchange. '
                                    'Please try again.')
        se_user = get_stackexchange_user(json.loads(results)['items'])
        
        url = "https://api.stackexchange.com/2.0/me?site=%s&key=%s&access_token=%s" % (se_user.main_site_key, key.api_key, req.credentials.access_token)
        res, results = self.http(req).request(url)
        if res.status is not 200:
            return self.raise_error('There was an error contacting StackExchange. '
                                    'Please try again.')

        main_user = json.loads(results)['items'][0]
        auth_id = User.generate_auth_id(req.provider, main_user['user_id'])
        return {
            'auth_id': auth_id,
            'info': {
                'id': main_user['user_id'],
                'displayName': main_user.get('display_name'),
            },
            'extra': {
                    'raw_info': main_user,
                    'associated_sites': se_user.associated_sites,
                    'associated_sites_keys': se_user.associated_sites_keys
                }
        }


