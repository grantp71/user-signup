import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

### ROT13 IS HERE IN THE SOLUTION FILE












USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")      #a username a through z zero through nine with a length between three to twenty characters
def valid_username(username):
    return username and USER_RE.match(username)     #return if a match

PASS_RE = re.compile(r"^.{3,20}$")                  #any characters with a length between three and twenty characters
def valid_password(password):
    return password and PASS_RE.match(password)     #return if a match

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)       #return if a match

class Signup(BaseHandler):

    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "The username entered is not valid.."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "The password entered is not valid.."
            have_error = True
        elif password != verify:
            params['error_verify'] = "The passwords entered do not match.."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "The email entered is not valid.."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.redirect("/welcome?username=" + username)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        self.render('welcome.html', username = username)


app = webapp2.WSGIApplication([('/', Signup),
                               ('/welcome', Welcome)],
                              debug = True)
