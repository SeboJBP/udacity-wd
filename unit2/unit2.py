"""A simple webapp2 server."""


import webapp2
import cgi      # for escape_html
import re       # reg exps to validate inputs


# Validation functions
def escape_html(s):
    return cgi.escape(s, quote = True)

# Rot 13 functions
def rot13(s):
    kAlpha = "abcdefghijklmnopqrstuvwxyz"
    rot_s = ""
    for l in s:
        if l.isalpha():
            r = kAlpha[(kAlpha.index(l.lower()) + 13) % 26]
            if l.isupper():
                r = r.upper()
        else:
            r = l
        rot_s += r
    return rot_s

# Signup validation
USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile("^.{3,20}$" )
EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")
def valid_username(username):
    if USER_RE.match(username):
        return True, ""
    else:
        return None, "That's not a valid username."

def valid_password(password):
    if PASSWORD_RE.match(password):
        return True, ""
    else:
        return None, "That wasn't a valid password."

def is_verified(password, verify):
    if password == verify:
        return True, ""
    else:
        return None, "Your passwords didn't match"

def valid_email(email):
    if email:
        if EMAIL_RE.match(email):
            return True, ""
        else:
            return None, "That is not a valid email"
    else:
        return True, ""


# RequestHandlers
class MainPage(webapp2.RequestHandler):
    def write_main_html(self):
        with open("./main.html") as myfile:
            main_html = myfile.read()
        self.response.out.write(main_html)

    def get(self):
        self.write_main_form()

class Rot13(webapp2.RequestHandler):
    def write_rot13_html(self, text=""):
        with open("./rot13.html") as myfile:
            rot13_html = myfile.read()
        self.response.out.write(rot13_html % {'text' : text})

    def get(self):
        self.write_rot13_html()

    def post(self):
        user_text = self.request.get('text')
        # text = valid_text(user_text)  # Is there invalid input? (if so, replace user_text with text below)
        rot13_text = rot13(user_text)
        self.write_rot13_html(escape_html(rot13_text))

class Signup(webapp2.RequestHandler):
    def write_signup_html(self,
                          username="",
                          email="",
                          error_un="",
                          error_pw="",
                          error_verify="",
                          error_email=""):
        with open("./signup.html") as myfile:
            signup_html = myfile.read()
        self.response.out.write(
            signup_html % {'username' : username,
                           'email' : email,
                           'error_un' : error_un,
                           'error_pw' : error_pw,
                           'error_verify' : error_verify,
                           'error_email' : error_email})

    def get(self):
        self.write_signup_html()

    def post(self):
        user_un = self.request.get('username')
        user_pw = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        username_f, error_un = valid_username(user_un)
        password_f, error_pw = valid_password(user_pw)
        verified_f, error_verify = is_verified(user_verify, user_pw)
        email_f, error_email = valid_email(user_email)

        if not (username_f and password_f and verified_f and email_f):
            self.write_signup_html(user_un, user_email,
                                   error_un, error_pw,
                                   error_verify, error_email)
        else:
            # self.redirect('/signup_welcome')
            self.redirect('/signup_welcome?username=' + user_un)

class SignupWelcome(webapp2.RequestHandler):

    def write_welcome_html(self, username=""):
        with open("./signup-welcome.html") as myfile:
            welcome_html = myfile.read()
        self.response.out.write(welcome_html % {'username' : username})

    def get(self):
        username = self.request.get('username')
        self.write_welcome_html(username)


# Application
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13', Rot13),
    ('/signup', Signup),
    ('/signup_welcome', SignupWelcome)],
     debug=True)

