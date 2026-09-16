import http.server
import socketserver
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

PORT = 8080

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        log_entry = f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}\n"
        try:
            with open("server_access.log", "a", encoding="utf-8") as f:
                f.write(log_entry)
        except:
            pass

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    with ReusableTCPServer(("", PORT), QuietHandler) as httpd:
        with open("server_access.log", "a", encoding="utf-8") as f:
            f.write(f"=== Server started on port {PORT} ===\n")
        httpd.serve_forever()

