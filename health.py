import http.server, os
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200); s.end_headers(); s.wfile.write(b"ok")
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), H).serve_forever()
