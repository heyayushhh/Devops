import http.server
import socketserver
import os
import sys

PORT = 8080

class Lab2AppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        response_msg = (
            "===================================================\n"
            "   LAB 2 — DOCKER APPLICATION CONTAINERIZATION    \n"
            "===================================================\n"
            f"Container Status : ACTIVE\n"
            f"Runtime Engine   : Python {sys.version.split()[0]}\n"
            f"Listening Port   : {PORT}\n"
            f"Host Process PID : {os.getpid()}\n"
            f"Working Dir      : {os.getcwd()}\n"
            "Response         : Containerization Q1 Verification Successful!\n"
        )
        self.wfile.write(response_msg.encode('utf-8'))

if __name__ == '__main__':
    print(f"[*] Lab 2 Q1 Server starting on port {PORT}...")
    with socketserver.TCPServer(("", PORT), Lab2AppHandler) as httpd:
        print(f"[+] Server listening on 0.0.0.0:{PORT}")
        httpd.serve_forever()
