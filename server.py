import os, sys, random, json
import sqlite3

from pypugjs.ext.tornado import patch_tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
from tornado.web import url

import path

patch_tornado()
db_name = 'appdatabase.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()

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
                user.write_message(message["text"])

    def on_close(self):
        self.users.remove(self)
        print("Session close")


class MainHandler(BaseHandler):
    def get(self):
        self.render('main.pug')


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.pug")

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


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_current_user()
        self.redirect('/')


class Application(tornado.web.Application):
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        handlers = [
            (r"/", MainHandler),
            (r"/auth/login", LoginHandler),
            (r"/auth/logout", LogoutHandler),
            (r"/websocket", WebSocketHandler),
        ]
        settings = dict(
            login_url="/auth/login",
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
