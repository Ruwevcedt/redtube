from gevent import pywsgi
from drawer import app


http_server = pywsgi.WSGIServer(('0.0.0.0', 19283), app)
http_server.serve_forever()
