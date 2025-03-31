import http.server
import socketserver
import json
import logging 
base = "/tolan_bio_site"
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        log.info(f"received request for path: {self.path}")
        match self.path:
            case '/image_gallery':
                self.path = f'{base}/image_gallery.html'
                super().do_GET()
            case '/contact':
                self.path = '/contact.html'
                super().do_GET()
            case '/index':
                self.path = '/index.html'
                super().do_GET()
            case '/hobbies':
                self.path = '/hobbies.html'
                super().do_GET()
            case '/api/info':
                data = {
                    'name': "Chris Tolan",
                    'bio': 'sound engineer/musician turned software developer',
                    'hobbies': ['music', 'coding', 'video games', 'cooking', 'etc...']
                }
                self.handleHeaders(data, True)
            case '/api/contact':
                contact_info = {
                    'name': "Chris Tolan",
                    'phone': "813-410-2858",
                    'email': "christolansf@icloud.com"
                }
                self.handleHeaders(contact_info, True)
            case '/favicon.ico':
                  self.path = '/favicon.svg'
                  super().do_GET()
            case '/api/gallery':
                image_object = [
                    {
                        "src": "https://scontent-sjc3-1.xx.fbcdn.net/v/t1.6435-9/185321622_10218046087574035_3186882831171380852_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=sZkhaIpYDp4Q7kNvgGpegUt&_nc_oc=Adnrp7_pOufvUHfdS8PzeZeZ10JfZ4ZzRWEaZhUeAu78XvOYumQhXSK4wN06qmCUabFl74HXnou-8VFGGwNFFAK4&_nc_zt=23&_nc_ht=scontent-sjc3-1.xx&_nc_gid=42Bjr9DQBNu4vVv0Ij9v3w&oh=00_AYHpoxnSbvlLCZ4p6QCGqcgeE5HfPDgm0pjttw-5kobXhQ&oe=6806A0FF",
                        "alt": "chris tolan"
                    }
                ]

                self.handleHeaders(image_object, True)
            case _:
                super().do_GET()

    def do_POST(self):
        match self.path:
            case '/api/submit-contact':
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




            #         # self.send_response(400)
            #         # self.send_header("Content-Type", "application/json")
            #         # self.end_headers()
            #         # self.wfile.write(json.dumps({"status": "failure", "message": "Invalid JSON"}).encode('utf-8'))
            #         return


            #     # respons_data = json.dumps(response).encode('utf-8')
            #     # self.send_response(200)
            #     # self.send_header("Content-Type", "application/json")
            #     # self.send_header("Content-Length", str(len(respons_data)))
            #     # self.end_headers()
            #     # self.wfile.write(respons_data)



# class MyHandler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/api/info':
#             data = {
#                 'name': "Chris Tolan",
#                 'bio': 'sound engineer/musician turned software developer',
#                 'hobbies': ['music', 'coding', 'video games', 'cooking', 'etc...']
#             }
#             json_data = json.dumps(data).encode('utf-8')
#             #send http header
#             self.send_response(200)
#             self.send_header("Content-Type", "application/json")
#             self.send_header("Content-Length", str(len(json_data)))
#             self.end_headers()
#             # write JSON to response
#             self.wfile.write(json_data)
#         else:
#             super().do_GET()
        
# PORT = 8000
# with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
#     log.info(f"Serving at port {PORT}")
#     httpd.serve_forever()







#simple HTTP server that listens on port 8000
# httpd = http.server.HTTPServer(('', 8000), http.server.SimpleHTTPRequestHandler)
# print("Serving HTTP on port 8000...")
# httpd.serve_forever()
