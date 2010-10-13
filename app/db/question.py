from google.appengine.ext import db

RANKING_SIZE = 100

class PrintedQuestionModel(db.Model):
    question_id = db.IntegerProperty()
    service = db.StringProperty()
    title = db.StringProperty()
    tags = db.ListProperty(str)
    counter = db.IntegerProperty()
    
    def get_url(self):
        return "http://%s.com/questions/%d" % (self.service, self.question_id)

def store(question_id, service, title, tags):
    #Transaction would be an overkill
    entity = PrintedQuestionModel.get_by_key_name(key_names = '%s_%s' % (question_id, service ) )
    if entity:
        entity.counter = entity.counter + 1
        entity.put()
    else:
        PrintedQuestionModel(key_name = '%s_%s' % (question_id, service ), question_id = question_id,\
                             service = service, title = title, tags = tags, counter = 1).put()

def get_top_printed():
    query = PrintedQuestionModel.all().order('-counter')
    return query.fetch(RANKING_SIZE)