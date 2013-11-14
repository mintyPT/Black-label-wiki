from utils import make_pw_hash
from utils import valid_pw


from google.appengine.ext import db


class User(db.Model):
    username = db.StringProperty(required=True)
    email = db.StringProperty()
    password_hash = db.StringProperty(required=True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)
    
    @classmethod
    def by_username(cls, username):
        # users = db.GqlQuery("select * from User where username='%s'" % username)
        user = cls.all().filter('username =', username).get()
        return user

    @classmethod
    def register(cls, username, password, email=None):
        password_hash = make_pw_hash(password)
        return cls(username = username, 
                    password_hash = password_hash, 
                    email = email)

    @classmethod
    def login(cls, username, pw):
        u = cls.by_username(username)
        if u and valid_pw(pw, u.password_hash):
            return u


class Page(db.Model):
    title = db.StringProperty(required=True)
    # author = db.ReferenceProperty(User, required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def by_title(cls, title):
        return cls.all().filter('title =', title).order('-created').get()
        
    @classmethod
    def all_by_title(cls, title):
        return cls.all().filter('title =', title).order('-created').fetch(None)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)
