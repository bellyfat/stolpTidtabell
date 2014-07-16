import tornado.ioloop
import tornado.web
import dep

application = tornado.web.Application([
    (r"/favicon.ico", tornado.web.StaticFileHandler,dict(url='favicon.ico',permanent=False)),
    (r"/dep/([^/]+)", dep.getdep),
])

def main(address):
    application.listen(8080, address)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    address = "87.237.214.63"
    main(address)
