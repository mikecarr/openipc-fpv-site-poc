#!/usr/bin/env python3
"""
Lightweight API server for OpenIPC
This minimal server provides API endpoints for the web UI to interact with the system
"""

import os
import json
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Configuration
PORT = 8000
HOST = '0.0.0.0'

class OpenIPCHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/system-info':
            self._handle_system_info()
        elif path == '/api/wireless-settings':
            self._handle_get_wireless_settings()
        elif path == '/api/uptime':
            self._handle_uptime()
        elif path == '/api/resources':
            self._handle_resources()
        elif path.startswith('/'):
            # Serve static files
            self._serve_static_file(path)
        else:
            self._handle_not_found()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/wireless-settings':
            self._handle_update_wireless_settings(post_data)
        elif path == '/api/execute':
            self._handle_execute_command(post_data)
        else:
            self._handle_not_found()

    def _serve_static_file(self, path):
        # Security check to prevent directory traversal
        if '..' in path:
            self._handle_not_found()
            return

        # Default to index.html for root
        if path == '/':
            path = '/index.html'

        # Map to the actual file path
        file_path = os.path.join('/usr/share/www', path.lstrip('/'))
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                
            # Set content type based on file extension
            content_type = 'text/html'
            if file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.json'):
                content_type = 'application/json'
            elif file_path.endswith('.png'):
                content_type = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self._handle_not_found()

    def _handle_system_info(self):
        # Get system information using shell commands
        try:
            # Get device type
            device_info = subprocess.check_output(['cat', '/proc/cmdline']).decode('utf-8')
            
            # Get firmware version
            version_info = subprocess.check_output(['cat', '/etc/os-release']).decode('utf-8')
            
            response = {
                'device': device_info.strip(),
                'version': version_info.strip()
            }
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self._handle_error(str(e))

    def _handle_get_wireless_settings(self):
        try:
            # Read wireless settings from config file
            config = subprocess.check_output(['cat', '/etc/wfb.conf']).decode('utf-8')
            
            # Parse basic settings (very simplified parsing)
            settings = {
                'channel': '100',
                'power': '30',
                'stbc': True,
                'ldpc': True
            }
            
            for line in config.splitlines():
                line = line.strip()
                if line.startswith('channel='):
                    settings['channel'] = line.split('=')[1]
                elif line.startswith('driver_txpower_override='):
                    settings['power'] = line.split('=')[1]
                elif line.startswith('stbc='):
                    settings['stbc'] = line.split('=')[1] == '1'
                elif line.startswith('ldpc='):
                    settings['ldpc'] = line.split('=')[1] == '1'
            
            self._set_headers()
            self.wfile.write(json.dumps(settings).encode())
        except Exception as e:
            self._handle_error(str(e))

    def _handle_update_wireless_settings(self, post_data):
        try:
            settings = json.loads(post_data.decode('utf-8'))
            
            # In a real implementation, you would:
            # 1. Validate the settings
            # 2. Update the config file
            # 3. Restart the wireless service if needed
            
            # This is a simplified example
            response = {
                'success': True,
                'message': 'Settings updated successfully',
                'settings': settings
            }
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self._handle_error(str(e))

    def _handle_execute_command(self, post_data):
        try:
            data = json.loads(post_data.decode('utf-8'))
            command = data.get('command', '')
            
            # IMPORTANT: In a real implementation, you would need to:
            # 1. Validate the command for security
            # 2. Only allow specific whitelisted commands
            # 3. Handle errors properly
            
            # This is a simplified and UNSAFE example
            output = subprocess.check_output(command, shell=True).decode('utf-8')
            
            response = {
                'success': True,
                'output': output
            }
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self._handle_error(str(e))

    def _handle_uptime(self):
        try:
            uptime = subprocess.check_output(['uptime']).decode('utf-8').strip()
            
            response = {
                'uptime': uptime
            }
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self._handle_error(str(e))

    def _handle_resources(self):
        try:
            # Get memory usage
            memory = subprocess.check_output(['free', '-k']).decode('utf-8')
            
            # Get CPU usage
            cpu = subprocess.check_output(['top', '-bn1']).decode('utf-8')
            
            response = {
                'memory': memory.strip(),
                'cpu': cpu.strip()
            }
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self._handle_error(str(e))

    def _handle_not_found(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def _handle_error(self, error_message):
        self.send_response(500)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': error_message}).encode())

def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, OpenIPCHandler)
    print(f'Starting server on {HOST}:{PORT}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
