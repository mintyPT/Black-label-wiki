import logging

from models import User
from models import Page

from basehandler import Base

from validators import validate_email
from validators import validate_password
from validators import validate_username




class WikiPage(Base):
    def get(self, title):
        version = self.request.get('v')
        if version:
            version = int(version)
            page = Page.by_id(version)
        else:
            page = Page.by_title(title)

        if page:
            self.render('wiki_page.html', title=title[1:], content=page.content)
        else:
            self.redirect("/_edit"+title)


class EditPage(Base):
    def get(self, title):
        if self.user:
            content = ''
            version = self.request.get('v')
            
            if version:
                version = int(version)
                page = Page.by_id(version)
            else:
                page = Page.by_title(title)
            
            if page:
                content = page.content

            self.render('wiki_page_edit.html', title=title[1:], content=content, view=True)
        else:
            self.redirect('/login')
    
    def post(self, title):
        page = Page.by_title(title)
        content = self.request.get("content")
        
        if page:
            page = Page(title=title, content=content)
            page.put()
        else:
            page = Page(title=title, content=content)
            page.put()
        
        self.redirect(title)
            

class Login(Base):
    def get(self):
        if self.user:
            self.redirect('/')
        else:
            self.render('login.html', title="Login")

    def post(self):
        errors = []

        username = self.request.get('username')
        valid_username = validate_username(username)
        if not valid_username:
            errors.append("Invalid username")
        
        password = self.request.get('password')
        valid_password = validate_password(password)
        if not valid_password:
            errors.append("Invalid password")

        user = User.login(username, password)
        if not user:
            errors.append("Invalid login details")


        if not errors:
            self.login(user)
            self.redirect('/')
        else:          
            self.render('login.html', title="Login", errors=errors, username=username)


class Logout(Base):
    def get(self):
        self.logout()
        self.redirect('/')


class Signup(Base):
    def get(self):    
        self.render('signup.html', title="Sign up")
        
    def post(self):
        errors = []
        
        username = self.request.get('username')
        valid_username = validate_username(username)
        if not valid_username:
            errors.append("Invalid username")


        email = self.request.get('email')
        valid_email = validate_email(email)
        if not valid_email and email != "":
            errors.append("Invalid email")


        password = self.request.get('password')
        valid_password = validate_password(password)
        if not valid_password:
            errors.append("Invalid password")

        verify = self.request.get('verify')
        valid_verify = validate_password(verify)
        if not valid_verify:
            errors.append("Invalid password verification")

        valid_password_match = password == verify
        if not valid_password_match:
            errors.append("Passwords do not match")
        
        logging.error("DB QUERY")
        # check if username is unique
        u = User.by_username(username)
        logging.error(repr(u))
        if u:
            errors.append("Username is not unique")

        if not errors:
            user = User.register(username, password, email)
            user.put()
            self.login(user)
            self.redirect('/')
        else:          
            self.render('signup.html', title="Sign up", errors=errors, username=username, email=email)



class HistoryPage(Base):
    def get(self, title):
        if self.user:
            pages = Page.all_by_title(title)
            self.render('history.html', pages=pages, title=title[1:])
        else:
            self.redirect('/login')

