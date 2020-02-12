from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty()
    pageId = ndb.IntegerProperty()
    time = ndb.StringProperty()
    message = ndb.StringProperty()

