import logging, web, re
from google.appengine.api import urlfetch
from app.lib.key import api_key
from google.appengine.api import memcache

render = web.render 

class Admin:
    """
    Admin homepage
    """
    def GET(self):
        result = {}
        action = web.input(action = None)['action']
        
        if action=='quota':
            
            result = (urlfetch.fetch('http://api.stackoverflow.com/1.0/questions/9?pagesize=0&key=%s' % api_key, headers = {'User-Agent': 'StackPrinter','Accept-encoding': 'gzip, deflate'}, deadline = 10)).headers
        
        elif action =='memcachestats':
            result = memcache.get_stats()
        
        elif action =='memcacheflush':
            result['result'] = memcache.flush_all()
        
        return render.admin(result)

