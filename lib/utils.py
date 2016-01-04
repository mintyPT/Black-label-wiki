import hmac
import unittest
from random import choice
from string import letters
import hashlib


# 
# Cookie hashing functions
# 

SECRET = 'I am the snowman!'
SEPARATOR = '|'

def make_secure_val(s):
    return "%s%s%s" % (s, SEPARATOR, hmac.new(SECRET, s).hexdigest())

def check_secure_val(h):
    part = h.split(SEPARATOR)[0]
    if h == make_secure_val(part):
        return part 


# 
# Password hashing functions
# 

def make_salt(length=10):
    return ''.join((choice(letters) for x in range(length)))

def make_pw_hash(pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(pw, h):
    salt = h.split(',')[-1]
    return make_pw_hash(pw, salt) == h




def test_pw_hashing():
    print "test_pw_hashing"
    # salt = make_salt()
    salt = "MNcAaZhYvN"
    pw_hash = make_pw_hash("mauro", salt)
    assert pw_hash == "1f23b10502b5b110243097b109ed4258559197e2e5ffb7e91b08a1a47df2dd85,MNcAaZhYvN"
    assert pw_hash != "1f213b10502b5b110243097b109ed4258559197e2e5ffb7e91b08a1a47df2dd85,MNcAaZhYvN"
    assert valid_pw("mauro", pw_hash) == True
    assert valid_pw("mauro1", pw_hash) == False

def test_cookie_hashing():
    print "test_cookie_hashing"
    mauro_hash = make_secure_val('mauro')
    assert mauro_hash == 'mauro|fc002faccc463ba85ddffa955a86f39f'
    assert check_secure_val(mauro_hash) == 'mauro'

if __name__ == '__main__':
    test_cookie_hashing()
    test_pw_hashing()


