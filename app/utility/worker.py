from app.db.question import CachedQuestionModel, CachedAnswersModel
import logging
import app.db.counter as dbcounter
import app.db.question as dbquestion

CHUNK_SIZE = 150


def deferred_store_question_to_cache(question_id, service, question_data):
    try:
        CachedQuestionModel(key_name = '%s_%s' % (question_id, service ), data = question_data).put()
    except Exception, ex:
        logging.info("%s - db error trying to store question_id : %s" % (service, question_id))

def deferred_store_answers_to_cache(question_id, service, answers_data):   
    id_service = '%s_%s' % (question_id, service)
    try:
        chunk_index = 0
        chunk_id = 1
        for chunk_index in range(CHUNK_SIZE, len(answers_data),  CHUNK_SIZE):
            CachedAnswersModel(key_name = '%s_%s' % (id_service, chunk_id), 
                               id_service = id_service,
                               chunk_id = chunk_id,
                               data = answers_data[chunk_index-CHUNK_SIZE:chunk_index]).put()  
            chunk_id += 1
        else:
             CachedAnswersModel(key_name = '%s_%s' % (id_service, chunk_id), 
                                id_service = id_service,
                                chunk_id = chunk_id,
                                data = answers_data[chunk_index:chunk_index + CHUNK_SIZE]).put()
    except Exception, ex:
        logging.info("%s - db error trying to store answers of question_id : %s" % (service, question_id))

def deferred_store_print_statistics(question_id, service, title, tags, deleted):
    try:
        dbcounter.increment()
        dbquestion.store_printed_question(question_id, service, title, tags, deleted)
    except Exception, exception:
        logging.exception("db error trying to store stats") 

def deferred_static_counters(question_id, service):
    try:
        dbcounter.increment()
        dbquestion.increment_printed_question_counter(question_id, service)
    except Exception, exception:
        logging.exception("db error trying to store stats")
      
def deferred_delete_question_and_answers(question_id, service):
    try:
        dbquestion.delete_question(question_id, service)
        dbquestion.delete_answers(question_id, service)
        dbquestion.delete_printed_question(question_id, service)
    except Exception, exception:
        logging.exception("db error deleting question and answers")
