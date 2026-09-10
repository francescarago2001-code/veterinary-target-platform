import http.server
import os
import socketserver

PORT = int(os.environ.get("PORT", 10000))


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.path = "/home.html"
        return super().do_GET()

    def do_HEAD(self):
        if self.path in ("/", "/index.html"):
            self.path = "/home.html"
        return super().do_HEAD()

    def guess_type(self, path):
        if path.endswith(".html"):
            return "text/html; charset=utf-8"
        return super().guess_type(path)


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as server:
        print(f"Sito attivo sulla porta {PORT}")
        server.serve_forever()