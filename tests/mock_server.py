"""
A tiny local HTTP server used ONLY to test Scraper's behavior
without needing external network access. Not part of the
project itself — this stays out of /mnt/user-data/outputs.
"""

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Toggle this between test runs to simulate different server behaviors.
MODE = "fail_twice_then_ok" # "ok", "fail_twice_then_ok", "always_500", "always_404"

_attempt_counts = {}      # need this for fail_twice_then_ok 



class MockHandler(BaseHTTPRequestHandler):
    def log_message(Self, format, *args):
        pass  # silence default request logging, we have our own logger 


    def do_GET(self):
        path = self.path
        _attempt_counts[path] = _attempt_counts.get(path,0) + 1
        count = _attempt_counts[path]


        if MODE == "ok":
            self._respond(200, "<html><body>Mock OK page</body></html>")
        
        elif MODE == "fail_twice_then_ok":
            if count <= 2:
                self._respond(503, "Service Unavailable")
            else :
                self._respond(200, "<html><body>Recovered after retries</body></html>")

        elif MODE == "always_500":
            self._respond(500, "Internal Server Error")

        elif MODE == "always_404":
            self._respond(404, "Not Found")




    def _respond(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))



def run_server(port=8765):
    server = HTTPServer(("localhost", port), MockHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server




if __name__ == "__main__":
    run_server()
    input("Server running on http://localhost:8765 — press Enter to stop\n")

