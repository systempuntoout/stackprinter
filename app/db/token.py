from google.appengine.ext import db

class Token(db.Model):
    value = db.StringProperty(required = True)
    last_modified = db.DateTimeProperty(required = True, auto_now = True)
