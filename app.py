import http.server
import socketserver

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/home.html"
        return super().do_GET()
    pass

with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as server:
    print(f"Sito attivo su http://localhost:{PORT}")
    server.serve_forever()
