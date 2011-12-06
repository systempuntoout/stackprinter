import logging
import pickle

from google.appengine.ext import db
from google.appengine.ext.db import stats
from google.appengine.api import memcache

from app.utility.utils import memcached
import app.db.sitemap as dbsitemap

TOP_PRINTED_PAGINATION_SIZE = 50
DELETED_PAGINATION_SIZE = 1000

class PickleProperty(db.Property):
     data_type = db.Blob
     def get_value_for_datastore(self, model_instance):
       value = self.__get__(model_instance, model_instance.__class__)
       if value is not None:
         return db.Blob(pickle.dumps(value))
     def make_value_from_datastore(self, value):
       if value is not None:
         return pickle.loads(str(value))
     def default_value(self):
       return copy.copy(self.default)

class PrintedQuestionModel(db.Model):
    question_id = db.IntegerProperty()
    service = db.StringProperty()
    title = db.StringProperty()
    tags = db.ListProperty(str)
    counter = db.IntegerProperty()
    deleted = db.BooleanProperty()
    
    def get_url(self):
        return "http://%s.com/questions/%d" % (self.service, self.question_id)

class CachedAnswersModel(db.Model):
    id_service = db.StringProperty()
    chunk_id = db.IntegerProperty()
    data = PickleProperty()  
    last_modified = db.DateTimeProperty(auto_now = True)
    
class CachedQuestionModel(db.Model):
    data = PickleProperty()
    last_modified = db.DateTimeProperty(auto_now = True)

def increment_printed_question_counter(question_id, service):
    entity = PrintedQuestionModel.get_by_key_name(key_names = '%s_%s' % (question_id, service ) )
    if entity:
        entity.counter += 1
        entity.put()


def store_printed_question(question_id, service, title, tags, deleted):
        entity = PrintedQuestionModel.get_by_key_name(key_names = '%s_%s' % (question_id, service ) )
        if entity:
            entity.counter += 1
            if entity.deleted and not deleted:
                #don't exhume ghosts
                pass
            else:
                entity.deleted = deleted
            entity.put()
        else:
            PrintedQuestionModel(key_name = '%s_%s' % (question_id, service ), question_id = question_id,\
                                 service = service, title = title, tags = tags, counter = 1, deleted = deleted).put()
            dbsitemap.Sitemap.update_last_sitemap( '%s_%s' % (question_id, service ))

def delete_printed_question(question_id, service):
    question_to_delete = PrintedQuestionModel.all().filter('question_id = ',int(question_id)).filter('service =',service).get()
    if question_to_delete:
        question_to_delete.delete()    
        return True
    else:
        return "None"
    
def get_top_printed_questions(page):
    fetched_questions = memcache.get('get_top_printed_questions')
    bookmark = memcache.get("%s:%s" % ('get_top_printed_questions_cursor', int(page)))
    if not fetched_questions and not bookmark:
        query = PrintedQuestionModel.all().order('-counter')
        bookmark = memcache.get("%s:%s" % ('get_top_printed_questions_cursor', int(page)-1))
        if bookmark:
            query.with_cursor(start_cursor = bookmark)
            fetched_questions = query.fetch(TOP_PRINTED_PAGINATION_SIZE)
            memcache.set("%s:%s" % ('get_top_printed_questions_cursor', page), query.cursor())
        else:
            if page == 1:
                fetched_questions = query.fetch(TOP_PRINTED_PAGINATION_SIZE)
                memcache.set("%s:%s" % ('get_top_printed_questions_cursor', page), query.cursor())
            else:
                #Without cursors return nothing, offset consumes too much Datastore reads
                fetched_questions = []
        if fetched_questions:
            memcache.set('get_top_printed_questions',fetched_questions)
    return fetched_questions

@memcached('get_top_printed_count', 3600*24*10)
def get_top_printed_count():
    try:
        kind_stats = stats.KindStat().all().filter("kind_name =", "PrintedQuestionModel").get()
        count = kind_stats.count
    except Exception, ex:
        logging.error(ex)
        count = PrintedQuestionModel.all().count()
    return count

@memcached('get_deleted_questions', 3600*24*10) 
def get_deleted_questions():
    query = PrintedQuestionModel.all().filter('deleted =', True).order('-counter')
    return query.fetch(DELETED_PAGINATION_SIZE)

def get_question(question_id, service):
    entity = CachedQuestionModel.get_by_key_name(key_names = '%s_%s' % (question_id, service ))
    if entity:
        return entity.data
    else:
        return None

def get_answers(question_id, service):
    answers = []
    entry_found = False
    answers_chunks = CachedAnswersModel.all().filter('id_service =', '%s_%s' % (question_id, service )).order('chunk_id').fetch(100)
    for answers_chunk in answers_chunks:
        answers = answers + answers_chunk.data
        entry_found = True
    else:
        if entry_found:
            return answers
        else:
            return None

def delete_question(question_id, service):
    entity = CachedQuestionModel.get_by_key_name(key_names = '%s_%s' % (question_id, service ))
    if entity:
        entity.delete()
        return True
    else:
        return None

def delete_answers(question_id, service):
    answers = []
    entry_found = False
    answers_chunks = CachedAnswersModel.all().filter('id_service =', '%s_%s' % (question_id, service )).order('chunk_id')
    for answers_chunk in answers_chunks:
        answers_chunk.delete()
        entry_found = True
    else:
        if entry_found:
            return True
        else:
            return None