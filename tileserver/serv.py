from http.server import HTTPServer, BaseHTTPRequestHandler
from skimage.io import imsave
import numpy as np
class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.path = '/index.html'
        try:
            print(self.path[-4:])
            if self.path[-4:] == '.png':
                file_to_open = open(self.path[1:], 'rb').read()
                self.send_response(200)
                print('serving an image!')
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(file_to_open)
            elif self.path[-4:] == '.rut':
                ll = self.path.index('_l')
                yl = self.path.index('_y')
                xl = self.path.index('_x')
                lstr = self.path[ll+2:yl]
                ystr = self.path[yl+2:xl]
                xstr = self.path[xl+2:-4]
                l = int(lstr)
                y = int(ystr)
                x = int(xstr)
                print(lstr,ystr,xstr)
                imsave('temp.png', np.load(f'../data/roots_130_pyramid/_l{l}_y{y}_x{x}.npz')['arr_0'])
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(open('temp.png', 'rb').read())
            else:
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(file_to_open, 'utf-8'))
        except Exception as e:
            print(e)
            file_to_open = "File not found" + str(e)
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))

httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()
