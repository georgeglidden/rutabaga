import os
from os import path
from csv import reader
from itertools import chain
from skimage.io import imread
from Tile import Tile
from json import dump as json_dump
from glob import glob
from PointSource import * 

def flatten(nested_list):
    return list(chain.from_iterable(nested_list))

def quarter(points, rect):
    l,r,t,b = rect
    mid_x, mid_y = ((l+r)/2,(t+b)/2)
    if len(points) > 0:
        points_by_x = sorted(points, key=lambda p: p[0])
        nearest_x = min(points_by_x, key=lambda p: abs(mid_x - p[0]))
        mid_x_i = points_by_x.index(nearest_x)

        points_left_by_y = sorted(points_by_x[:mid_x_i], key=lambda p: p[1])
        if len(points_left_by_y) > 0:
            nearest_left_y = min(points_left_by_y, key=lambda p: abs(mid_y - p[1]))
            mid_left_y_i = points_left_by_y.index(nearest_left_y)
            points_left_top = points_left_by_y[:mid_left_y_i]
            points_left_bottom = points_left_by_y[mid_left_y_i:]
        else:
            points_left_top = []
            points_left_bottom = []

        points_right_by_y = sorted(points_by_x[mid_x_i:], key=lambda p: p[1])
        if len(points_right_by_y) > 0:
            nearest_right_y = min(points_right_by_y, key=lambda p: abs(mid_y - p[1]))
            mid_right_y_i = points_right_by_y.index(nearest_right_y)
            points_right_top = points_right_by_y[:mid_right_y_i]
            points_right_bottom = points_right_by_y[mid_right_y_i:]
        else:
            points_right_top = []
            points_right_bottom = []
    else:
        points_left_top = []
        points_left_bottom = []
        points_right_top = []
        points_right_bottom = []

    return [(points_left_top, [l, mid_x, t, mid_y]),
    (points_right_top, [mid_x, r, t, mid_y]),
    (points_right_bottom, [mid_x, r, mid_y, b]),
    (points_left_bottom, [l, mid_x, mid_y, b])]

class Pyramid:
    def __init__(self, pyr_dir, point_set, bounds, depth, resolution = 100):
        self.pyr_dir = pyr_dir
        self.resolution = resolution
        self.point_set = point_set
        self.subsets = [[(point_set,bounds)]]
        self.bounds = bounds
        self.depth = depth
        for i in range(1,depth):
            layer = flatten([quarter(points,rect) for points,rect in self.subsets[i-1]])
            layer.sort(key=lambda x: (x[1][0],x[1][2]))
            self.subsets.append(layer)

    def generate_tiles(self):
        if not path.isdir(self.pyr_dir):
            os.mkdir(self.pyr_dir)
        layer_count = []
        for l in range(self.depth):
            layer_path = path.join(self.pyr_dir, f'z{l}')
            if not path.isdir(layer_path):
                os.mkdir(layer_path)
            for q in range(4**l):
                points, rect = self.subsets[l][q]
                i = q % (2**l)
                j = q // (2**l)
                tile = Tile(sum([2**m for m in range(l+1)])+q, (l,i,j), points, rect, width=self.resolution)
                tile.save(self.pyr_dir)
            layer_tiles = glob(path.join(layer_path,'*.tile'))
            layer_count.append(len(layer_tiles))
        summary = {
            'pyr_dir': self.pyr_dir,
            'depth': self.depth,
            'resolution': self.resolution,
            'nb_points': len(self.point_set),
            'layers': {
                f'z{l}': {
                    'expected_tiles': len(self.subsets[l]),
                    'generated_tiles': layer_count[l],
                    'nb_points': sum([len(s[0]) for s in self.subsets[l]])
                } for l in range(self.depth)
            }
        }
        json_dump(summary, open(path.join(self.pyr_dir, f'{self.pyr_dir}.pyr'), 'w'))

# a simple CLI for generating pyramids from a variety of point set sources
def main():
    import sys
    point_set_source = sys.argv[1]
    pyr_dir = sys.argv[2]
    if point_set_source[-4:] == '.csv':
        if '-b' in sys.argv:
            i = sys.argv.index('-b') + 1
            x0,x1,y0,y1 = sys.argv[i:i+4]
            bounds = x0,x1,y0,y1 = int(x0),int(x1),int(y0),int(y1)
        else:
            bounds = x0,x1,y0,y1 = [-1, 1, -1, 1]
        point_set = load_from_csv(point_set_source, x_bounds=(x0,x1), y_bounds=(y0,y1))
    else:
        try:
            thr = sys.argv[sys.argv.index('-t')+1]
            thr = float(thr)
            point_set = load_from_img(point_set_source, thr)
        except Exception as e:
            print(e)
            print(f'failed to load point set source {point_set_source}')
            return -1
    depth = sys.argv[sys.argv.index('-d')+1]
    depth = int(depth)
    resolution = sys.argv[sys.argv.index('-r')+1]
    resolution = int(depth)
    pyramid = Pyramid(pyr_dir, point_set, bounds, depth, resolution)
    pyramid.generate_tiles()

if __name__ == '__main__':
    main()
