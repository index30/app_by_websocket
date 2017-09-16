import os, sys, random, json

from pypugjs.ext.tornado import patch_tornado

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.web import url

patch_tornado()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    users = set()

    def open(self):
        self.users.add(self)
        print("Session open")

    def on_message(self, message):
        message = json.loads(message)
        if message["text"]:
            for user in self.users:
                user.write_message(message["text"])

    def on_close(self):
        self.users.remove(self)
        print("Session close")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('main.pug')


class Application(tornado.web.Application):
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler),
        ]
        settings = dict(
            template_path=os.path.join(BASE_DIR, 'templates'),
            static_path=os.path.join(BASE_DIR, 'static'),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
