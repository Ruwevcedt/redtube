from gevent import pywsgi
from drawer import app
import sys

keyfile = ""
certfile = ""

if sys.platform == "darwin":
    http_server = pywsgi.WSGIServer(('0.0.0.0', 19283), app)
else:
    http_server = pywsgi.WSGIServer(('0.0.0.0', 19283), app, keyfile=keyfile, certfile=certfile)

http_server.serve_forever()
