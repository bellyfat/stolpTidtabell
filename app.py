import tornado.ioloop
import tornado.web
import dep

application = tornado.web.Application([
    (r"/favicon.ico", tornado.web.StaticFileHandler,dict(url='favicon.ico',permanent=False)),
    (r"/dep/([^/]+)", dep.getdep),
])

def main():
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    print "run"
    main()
