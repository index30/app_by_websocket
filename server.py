import os, sys, random, json, path
import sqlite3
#from pykakasi import kakasi
from auto_response import DefaultResponse

from pypugjs.ext.tornado import patch_tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
from tornado.web import url

patch_tornado()
db_name = 'appdatabase.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()
#kakasi = kakasi()
#kakasi.setMode('J', 'H')
#conv = kakasi.getConverter()

class BaseHandler(tornado.web.RequestHandler):
    cookie_username = "username"
    def get_current_user(self):
        username = self.get_secure_cookie(self.cookie_username)
        if not username: return None
        return tornado.escape.utf8(username)

    def set_current_user(self, username):
        self.set_secure_cookie(self.cookie_username, tornado.escape.utf8(username))

    def clear_current_user(self):
        self.clear_cookie(self.cookie_username)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    users = set()
    messages = []

    def open(self):
        self.users.add(self)
        print("Session open")

    def on_message(self, message):
        message = json.loads(message)
        if message["text"]:
            self.messages.append(message)
            for user in self.users:
                #kakasi_mes = conv.do(message["text"])
                kakasi_mes = message["text"]
                DR = DefaultResponse()
                response = DR.parse_response(message["text"])
                user.write_message({'kakasi_mes': kakasi_mes, 'response': response})

    def on_close(self):
        self.users.remove(self)
        print("Session close")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('main.pug')


class SigninHandler(BaseHandler):
    def get(self):
        self.render("signin.pug")

    def post(self):
        #self.check_xsrf_cookie()
        username = self.get_argument("username")
        password = self.get_argument("password")

        pass_sql = 'select user_pass from user where user_name=?'
        c.execute(pass_sql, (username, ))
        pass_list = c.fetchall()
        if password == pass_list[0][0]:
            self.set_current_user(username)
            self.redirect("/")
        else:
            self.write_error(403)


class SignoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_current_user()
        self.redirect('/')


class SignupHandler(BaseHandler):
    def get(self):
        self.render("signup.pug")

    def post(self):
        #self.check_xsrf_cookie()
        username = self.get_argument("username")
        password = self.get_argument("password")
        confirmpass = self.get_argument("confirm")

        pass_sql = 'select user_pass from user where user_name=?'
        c.execute(pass_sql, (username, ))
        pass_list = c.fetchone()
        if pass_list is None and password == confirmpass:
            c.execute('insert into user (user_name, user_pass) values (?,?)', (username, password))
            conn.commit()
            self.set_current_user(username)
            self.redirect("/")
        else:
            self.redirect("/signup")


class Application(tornado.web.Application):
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        handlers = [
            (r"/", MainHandler),
            (r"/signup", SignupHandler),
            (r"/signin", SigninHandler),
            (r"/signout", SignoutHandler),
            (r"/websocket", WebSocketHandler),
        ]
        settings = dict(
            login_url="/signin",
            cookie_secret=path.cookie_path,
            template_path=os.path.join(BASE_DIR, 'templates'),
            static_path=os.path.join(BASE_DIR, 'static'),
        )

        conn.execute("create table if not exists user(id INTEGER PRIMARY KEY, user_name TEXT, user_pass TEXT)")
        c.execute("select * from user where user_name='admin'")
        entry = c.fetchone()
        if entry is None:
            c.execute('insert into user (user_name, user_pass) values (?,?)', ('admin', 'adminpass'))
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
