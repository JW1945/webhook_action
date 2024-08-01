import http.server
import subprocess
import hmac
import hashlib
import json
import os

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Verify GitHub signature
        signature = self.headers.get('X-Hub-Signature-256')
        secret = os.environ.get('WEBHOOK_SECRET').encode()
        hash_object = hmac.new(secret, msg=post_data, digestmod=hashlib.sha256)
        expected_signature = f"sha256={hash_object.hexdigest()}"
        
        if not hmac.compare_digest(signature, expected_signature):
            self.send_response(403)
            self.end_headers()
            return

        # Process the webhook
        event = json.loads(post_data.decode())
        if event['ref'] == 'refs/heads/main':  # Adjust branch name as needed
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Received')
            
            # Run your deployment script
            subprocess.Popen(['/path/to/your/deployment_script.sh'])
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Ignored')

if __name__ == '__main__':
    server_address = ('', 8000)  # Change port if needed
    httpd = http.server.HTTPServer(server_address, WebhookHandler)
    print('Webhook server running...')
    httpd.serve_forever()