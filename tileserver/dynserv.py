import sys
import io
from json import load, dumps
from os import path as os_path
from http.server import HTTPServer, BaseHTTPRequestHandler

import numpy as np
from skimage.io import imsave
from skimage.util import img_as_ubyte

from Tile import TileQuery
import ImplicitPyramid as impyr
from PointSource import *

def get_png_bytes(arr):
    byte_io = io.BytesIO()
    imsave(byte_io, img_as_ubyte(arr), format='PNG')
    return byte_io.getvalue()

class DynamicTileserver(BaseHTTPRequestHandler):

    def respond(self, byte_data, code=200, headers=None):
        self.send_response(code)
        if headers:
            self.send_header(*headers)
        self.end_headers()
        self.wfile.write(byte_data)

    def do_GET(self):
        if self.path == '/':
            self.path = '/demoClient.html'
        try:
            request = self.path.split('/')
            print(self.path)
            print(request)
            if request[1] == 'psq':
                pyr_label = request[2]
                z,x,y,w = request[3].split('_')
                z,x,y,w = int(z),int(x),int(y),int(w)
                tq = TileQuery((z,x,y),w)
                opt = {'bright':True,'pq':riley,'threshold_pq':None}
                print(opt)
                tile = impyr.do_tile_query(pyr_label, tq, options=opt)
                #timg = tile.render()
                #imsave('.tile_render.png', timg)
                #im_bytes = open('.tile_render.png', 'rb').read()
                im_bytes = get_png_bytes(tile.render())
                self.respond(im_bytes, headers=['Content-type', 'image/png'])
            elif request[1] == 'psq_meta':
                pyr_label = request[2]
                query = request[3]
                if query == 'pyramid':
                    pointset_data = dumps(impyr.do_meta_query(pyr_label))
                    self.respond(bytes(pointset_data, 'utf-8'))
                elif query == 'tile':
                    z,x,y,w = request[4].split('_')
                    z,x,y,w = int(z),int(x),int(y),int(w)
                    tq = TileQuery((z,x,y),w)
                    tile = impyr.do_tile_query(pyr_label, tq)
                    tile_data = dumps(tile.metadata())
                    self.respond(bytes(tile_data, 'utf-8'))
            else:
                requested_file = open(self.path[1:]).read()
                print(self.path[1:],len(requested_file),requested_file[:50])
                self.respond(bytes(requested_file, 'utf-8'))
        except Exception as e:
            generic_response = "File not found\n" + str(e)
            self.respond(bytes(generic_response, 'utf-8'),code=404)
            raise e
pyramid_points = []
pyramid_labels = []
pyramid_sources = []
i = 1
while '-p' in sys.argv[i:]:
    pyramid_sources.append(sys.argv[i+1])
    pyramid_labels.append(sys.argv[i+2])
    i += 3
render_options = sys.argv[i:]
riley = '-r' in render_options
for point_file in pyramid_sources:
    if riley:
        pyramid_points.append(load_riley_roots(point_file, (-1000,1000,),(-1000,1000)))
    else:
        pyramid_points.append(load_from_csv(point_file, (-1000,1000,),(-1000,1000)))
print(len(pyramid_points))
impyr.init_pyramids(pyramid_points,pyramid_labels,pyramid_sources,(-1000,1000,-1000,1000))
httpd = HTTPServer(('localhost', 8080), DynamicTileserver)
httpd.serve_forever()
