import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
from datetime import datetime


class FileHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.files_dir = os.environ.get('FILES_DIRECTORY', '/app/files')
        self.windows_mode = os.environ.get('WINDOWS_MODE', 'false').lower() == 'true'
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path.startswith('/file/'):
            filename = unquote(path[6:])
            self.serve_file(filename)
        elif path == '/health':
            self.health_check()
        else:
            self.error_response("Invalid endpoint", 404)
    
    def serve_file(self, filename):
        try:
            file_path = os.path.join(self.files_dir, os.path.basename(filename))
            
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
                self.json_response({
                    "status": "success",
                    "data": content,
                    "msg": "data returned"
                })
            else:
                self.error_response(f"there was an error retrieving {filename}")
        except Exception:
            self.error_response(f"there was an error retrieving {filename}")
    
    def health_check(self):
        self.json_response({
            "status": "healthy",
            "service": "remote-server-2",
            "timestamp": datetime.now().isoformat(),
            "mode": "Windows" if self.windows_mode else "Unix"
        })
    
    def json_response(self, data, status=200):
        # Format JSON based on mode
        if self.windows_mode:
            json_data = json.dumps(data, separators=(',', ':'))
            json_data = json_data.replace('\n', '\r\n')
            server_header = 'Microsoft-IIS/10.0'
        else:
            json_data = json.dumps(data, indent=2)
            server_header = 'Python/HTTP-Server'
        
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Server', server_header)
        self.send_header('Content-Length', str(len(json_data.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def error_response(self, message, status=200):
        self.json_response({
            "status": "error",
            "data": "",
            "msg": message
        }, status)


def main():
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    files_dir = os.environ.get('FILES_DIRECTORY', '/app/files')
    
    os.makedirs(files_dir, exist_ok=True)
    
    server = HTTPServer((host, port), FileHandler)
    print(f"Server starting on {host}:{port}")
    print(f"Serving files from: {files_dir}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == '__main__':
    main()