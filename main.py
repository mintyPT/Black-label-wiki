#!/usr/bin/env python

import os
import webapp2
import logging

from lib.handlers import Login
from lib.handlers import Logout
from lib.handlers import Signup
from lib.handlers import EditPage
from lib.handlers import WikiPage
from lib.handlers import HistoryPage


PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'


app = webapp2.WSGIApplication([
    ('/signup', Signup),
    ('/login', Login),
    ('/logout', Logout),
    ('/_history' + PAGE_RE, HistoryPage),
    ('/_edit' + PAGE_RE, EditPage),
    (PAGE_RE, WikiPage)
], debug=True)

