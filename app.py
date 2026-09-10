import http.server
import os
import socketserver

PORT = int(os.environ.get("PORT", 10000))


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/home.html"
        return super().do_GET()


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as server:
        print(f"Sito attivo sulla porta {PORT}")
        server.serve_forever()