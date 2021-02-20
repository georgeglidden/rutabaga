from http.server import HTTPServer, BaseHTTPRequestHandler
from skimage.io import imsave
import numpy as np
from os import path as os_path
from json import load
from Tile import Tile, TileQuery

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            request = self.path.split('/')
            print(self.path)
            print(request)
            if len(request) == 4 and request[1] == 'psq':
                    pyr_dir = request[2]
                    z,x,y,w = request[3].split('_')
                    z,x,y,w = int(z),int(x),int(y),int(w)
                    query = TileQuery((z,x,y),w)
                    tile = Tile.from_query(pyr_dir,query)
                    imsave('.dmap.png', tile.density_map())
                    self.send_response(200)
                    self.send_header('Content-type', 'image/png')
                    self.end_headers()
                    self.wfile.write(open('.dmap.png', 'rb').read())
            else:
                file_to_open = open(self.path[1:]).read()
                print(file_to_open)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(file_to_open, 'utf-8'))
# print(self.path[-4:])
# if self.path[-4:] == '.png':
#     file_to_open = open(self.path[1:], 'rb').read()
#     self.send_response(200)
#     print('serving an image!')
#     self.send_header('Content-type', 'image/png')
#     self.end_headers()
#     self.wfile.write(file_to_open)
# elif self.path[-4:] == '.rut':
#     ll = self.path.index('_l')
#     yl = self.path.index('_y')
#     xl = self.path.index('_x')
#     lstr = self.path[ll+2:yl]
#     ystr = self.path[yl+2:xl]
#     xstr = self.path[xl+2:-4]
#     l = int(lstr)
#     y = int(ystr)
#     x = int(xstr)
#     print(lstr,ystr,xstr)
#     imsave('temp.png', np.load(f'../data/roots_130_pyramid/_l{l}_y{y}_x{x}.npz')['arr_0'])
#     self.send_response(200)
#     self.send_header('Content-type', 'image/png')
#     self.end_headers()
#     self.wfile.write(open('temp.png', 'rb').read())
# else:
#     file_to_open = open(self.path[1:]).read()
#     self.send_response(200)
#     self.end_headers()
#     self.wfile.write(bytes(file_to_open, 'utf-8'))
        except Exception as e:
            file_to_open = "File not found\n" + str(e)
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            raise e

httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()
