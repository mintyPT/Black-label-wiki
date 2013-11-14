import os
import webapp2
import jinja2
from models import User

base = '/'.join(os.path.dirname(__file__).split('/')[:-1])
templates_dir = os.path.join(base, "templates")
jinja_env = jinja2.Environment( loader = jinja2.FileSystemLoader(templates_dir),
                                autoescape = True)



from utils import make_secure_val
from utils import check_secure_val


class Base(webapp2.RequestHandler):
    
    # 
    # Helpers and others
    # 

    def info(self):
        ''' prints the information of the request '''
        self.response.headers['Content-Type'] = "text/plain"
        self.write(self.request)

    def done(self, *a, **kw):
        raise NotImplementedError

    def notfound(self):
        self.error(404)
        self.write("<h1>404: Not found!</h1> Sorry my friend, you hit a dead end.")

    def get(self):
        self.info()
        
    def post(self):
        self.info()
        
    #
    # rendering functions and helping functions
    #
    
    def write(self, *args, **kwargs):
        self.response.write(*args, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **params):
        self.write(self.render_str(template, user=self.user, **params))

    # 
    # Cookie related functions
    # 

    def set_cookie(self, cookie):
        self.add_header("Set-Cookie", cookie)

    def get_cookie(self, cookie_name, default=None):
        return self.request.cookies.get(cookie_name, default)

    def set_secure_cookie(self, name, val):
        self.set_cookie('%s=%s; Path=/' % (name, make_secure_val(val)))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    # 
    # Auth functions
    # 

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.set_secure_cookie('user_id', '')


    # 
    # header functions
    # 

    def add_header(self, *args, **kwargs):
        self.response.headers.add_header(*args, **kwargs)

    def set_content_to_text(self):
        self.response.headers['Content-Type'] = "text/plain"

    def set_content_type_to_json(self):
        self.response.headers['Content-Type'] = "application/json"


    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
