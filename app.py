import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.options import define, options
from db_access import *
from settings import SERVER_PORT, API_PASSWD, API_USERNAME
import json
define("port", default=SERVER_PORT, help="run on the given port", type=int)
define("debug", default=True, type=bool)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, Welcome to Miku')
        self.finish()


class AllProxyHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_argument('user', '')
        password = self.get_argument('password', '')
        if user == API_USERNAME and password == API_PASSWD:
            res = get_ip()
            self.finish(res)
        else:
            self.write('Error in Account or Password')


class GetProxyHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_argument('user', '')
        password = self.get_argument('password', '')
        if user == API_USERNAME and password == API_PASSWD:
            res = random_ip()
            self.finish(res)
        else:
            self.write('Error in Account or Password')


class DelProxyHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_argument('user', '')
        password = self.get_argument('password', '')
        ip = self.get_argument('proxy').split(':')[0]
        if user == API_USERNAME and password == API_PASSWD:
            del_ip(ip)
        else:
            self.write('Error in Account or Password')


class OverseasProxyHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_argument('user', '')
        password = self.get_argument('password', '')
        if user == API_USERNAME and password == API_PASSWD:
            res = random_overseas_ip()
            self.finish(res)
        else:
            self.write('Error in Account or Password')


settings = {
        "debug": False,
}


application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/get_all', AllProxyHandler),  # 获取所有代理
    (r'/get', GetProxyHandler),  # 随机获取一个代理
    (r'/delete', DelProxyHandler),  # 删除代理
    (r'/overseas', OverseasProxyHandler),  # 随机获取一个海外代理

], **settings)


def run():
    application.listen(options.port)
    print("App Start running at: http://127.0.0.1:{port}".format(port=options.port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
