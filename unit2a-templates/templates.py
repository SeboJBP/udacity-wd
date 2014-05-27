"""Learning templates"""

import os

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        "Loads file, creates jinja template and renders"
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        "Wraps around the rendered template and sends it to the client"
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        items = self.request.get_all("food")
        self.render("shopping_list.html", items = items)


class FizzBuzzHandler(Handler):
    def get(self):
        n = self.request.get('n', 0)  # defaulting to 0
        n = n and int(n)  # this is nice syntactic sugar
        self.render('fizzbuzz.html', n = n)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fizzbuzz', FizzBuzzHandler)], 
    debug=True)
