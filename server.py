import http.server
import socketserver
import json
import logging
from urllib.parse import urlparse, parse_qs
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        log.info(f"received request for path: {self.path}")
        match self.path:
            case '/tolan_bio_site/image_gallery':
                self.path = '/tolan_bio_site/image_gallery.html'
                super().do_GET()
            case '/tolan_bio_site/contact':
                self.path = '/tolan_bio_site/contact.html'
                super().do_GET()
            case '/tolan_bio_site/index':
                self.path = '/tolan_bio_site/index.html'
                super().do_GET()
            case '/tolan_bio_site/hobbies':
                self.path = '/tolan_bio_site/hobbies.html'
                super().do_GET()
            case '/tolan_bio_site/api/info':
                data = {
                    'name': "Chris Tolan",
                    'bio': 'sound engineer/musician turned software developer',
                    'hobbies': ['music', 'coding', 'video games', 'cooking', 'etc...']
                }
                self.handleHeaders(data, True)
            case '/api/contact':
                contact_info = {
                    'name': "Chris Tolan",
                    'phone': "415-867-5309",
                    'email': "christolan@tolbot.com"
                }
                self.handleHeaders(contact_info, True)
            case '/favicon.ico':
                  self.path = '/favicon.svg'
                  super().do_GET()
            case '/api/gallery':
                parsed = urlparse(self.path)
                query_params = parse_qs(parsed.query)
                category = query_params.get("category", [None])[0]
                
                image_object = [
                    {
                        "src": "https://live.staticflickr.com/65535/54416799767_c306eb47fa_5k.jpg",
                        "alt": "chris tolan",
                        "category": "city"
                    },
                    {
                        "src": "https://live.staticflickr.com/65535/54417378698_ca8486adee_6k.jpg",
                        "alt": "chris tolan",
                        "category": "city"
                    },
                    {
                        "src": "https://live.staticflickr.com/65535/54416579489_3b162debdb_6k.jpg",
                        "alt": "chris tolan",
                        "catagory": "city"
                    },
                    {
                        "src": "https://live.staticflickr.com/65535/54416374516_834ef30396_5k.jpg",
                        "alt": "chris tolan",
                        "category": "nature"
                    },
                    {
                        "src": "https://live.staticflickr.com/65535/54416971824_9c78cd0d5d_5k.jpg",
                        "alt": "chris tolan",
                        "category": "nature"
                    },
                    {
                        "src": "https://live.staticflickr.com/65535/54416568400_5abf15cdcf_5k.jpg",
                        "alt": "chris tolan",
                        "category": "nature"
                    },
                    {
                        "src": "https://live.staticflickr.com/65535/54414994482_35e7451ce3_3k.jpg",
                        "alt": "chris tolan",
                        "category": "technology"
                    },
                    {
                        "src": "https://live.staticflickr.com/65535/54415763513_021bc2b91f_k.jpg",
                        "alt": "chris tolan",
                        "category": "technology"
                    },
                    {
                        "src": "https://live.staticflickr.com/65535/54414807236_cfa476240f_k.jpg",
                        "alt": "chris tolan",
                        "category": "technology"
                    },
                ]
                if category:
                    image_object = [img for img in image_object if img["category"] == category]
                self.handleHeaders(image_object, True)
            case _:
                super().do_GET()

    def do_POST(self):
        match self.path:
            case 'api/submit-contact':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                except Exception as e:
                    log.error(f'Error decoding JSON: {e}')
                    success = False
                    self.handleHeaders(data, success)
                    return
                #log the received form data
                log.info(f'Received contact submission: {data}')
                response = {"status": "success", "message": "Contact submission recieved", "data": str(data)}
                success = True
                self.handleHeaders(response, success)
            case _:
                self.send_response(404)
                self.end_headers()

    def handleHeaders(self, data, success):
            json_data = json.dumps(data).encode('utf-8')
            self.send_response(200) if success else self.send_response(400)
            #send http header
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(json_data)))
            self.end_headers()
            # write JSON to response
            self.wfile.write(json_data) if success else self.wfile.write(json.dumps({"status": "failure", "message": "Invalid JSON"}).encode('utf-8'))
        
PORT = 8000
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    log.info(f"Serving at port {PORT}")
    httpd.serve_forever()
