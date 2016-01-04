import re


def regexValidate(regeXpression, string):
    return regeXpression.match(string)

def validate_username(string):
    ''' will return None if the username is invalid '''
    username_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return regexValidate(username_re, string)

def validate_password(string):
    password_re = re.compile(r"^.{3,20}$")
    return regexValidate(password_re, string)
    
def validate_email(string):
    email_re = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    return regexValidate(email_re, string)
