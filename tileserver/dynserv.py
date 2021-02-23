from http.server import HTTPServer, BaseHTTPRequestHandler
from skimage.io import imsave
import numpy as np
from os import path as os_path
from json import load
from Tile import TileQuery
import ImplicitPyramid as impyr

class DynamicTileserver(BaseHTTPRequestHandler):

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
                    tq = TileQuery((z,x,y),w)
                    tile = impyr.do_query(pyr_dir, tq)
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
        except Exception as e:
            file_to_open = "File not found\n" + str(e)
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            raise e

impyr.init_point_sources(['../data/roots_100.csv'],['zoomed_pyramid'],(-1,1,-1,1))
httpd = HTTPServer(('localhost', 8080), DynamicTileserver)
httpd.serve_forever()
