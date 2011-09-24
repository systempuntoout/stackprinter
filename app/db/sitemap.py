import logging

from google.appengine.ext import db
from google.appengine.api import memcache
from app.utility.utils import memcached

import app.utility.utils as utils
import app.db.counter as counter

import web

QUESTIONS_PER_SITEMAP = 500


class Sitemap(db.Model):
    question_count = db.IntegerProperty(default = 0)
    question_keys = db.StringListProperty(default = [])    
    content = db.TextProperty(default ='')
    archived = db.BooleanProperty(default = False)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    @staticmethod
    def get_last_sitemap():
        entity = Sitemap.all().order('-created').get()
        if entity:
            if entity.question_count >= QUESTIONS_PER_SITEMAP:
                entity.content = unicode(web.render.sitemap_questions(entity.question_keys))
                entity.archived = True
                entity.put()
                entity = Sitemap()
                entity.put()
        else:
            entity = Sitemap()
            entity.put()
        return entity
        
    @staticmethod
    def update_last_sitemap(key):
        last_sitemap = Sitemap.get_last_sitemap()
        last_sitemap.question_count += 1
        last_sitemap.question_keys.insert(0, str(key))
        last_sitemap.put()
    
    
    @staticmethod
    def get_sitemaps():
        sitemaps = Sitemap.all().order('-created').fetch(500)
        return sitemaps
        
    @staticmethod
    @memcached('get_sitemap_by_id', 3600*24, lambda id : int(id) )
    def get_sitemap_by_id(id):
        entity = Sitemap.get_by_id(id)
        if entity:
            if entity.content:
                return entity.content
            else:
                return unicode(web.render.sitemap_questions(entity.question_keys))
        else:
            raise web.notfound()