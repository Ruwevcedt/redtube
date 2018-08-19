from gevent import pywsgi
from drawer import app


http_server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()
