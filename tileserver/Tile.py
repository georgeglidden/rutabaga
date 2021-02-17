# generate tiles from pyramid
from numpy import histogram2d
from json import dump,load
from os import path

class TileQuery:
    def __init__(self, coordinates, resolution):
        self.coordinates = coordinates
        self.resolution = resolution

class Tile:
# the Tile class holds all the information necessary to
# 1. save and restore pointsets to and from a pyramid file structure;
#    enable the TileServer to respond to PointSetQuery GET requests
# 2. provide a TileClient with everything it needs to quickly render the pointset
    def __init__(self, tile_id, pos, pointset, rect, fitted_rect = None, width=100):
        self.id = tile_id
        self.pos = (int(pos[0]),int(pos[1]),int(pos[2]))
        self.width = width
        self.rect = [self.l, self.r, self.t, self.b] = rect
        rect_bounds = [(self.l,self.t),(self.r,self.t),(self.r,self.b),(self.l,self.b)]

        if len(pointset) == 0:
            self.points = rect_bounds
        else:
            self.points = pointset
        self.xvals,self.yvals = list(zip(*self.points)) # unzip pointset
        if fitted_rect == None:
            fitted_rect = [min(xvals),max(xvals),min(yvals),max(yvals)]
        self.fitted_rect = fitted_rect
        self.xbounds,self.ybounds = list(zip(*rect_bounds)) # unzip bound set
        self._density_map = None

    def density_map(self):
        if self._density_map == None:
            self._density_map, _, __ = histogram2d(self.xvals+self.xbounds,self.yvals+self.ybounds,self.width)
        return self._density_map

    # the pointset is saved rather than the density map to prevent a storage req. explosion:
    # if the density maps are stored, a pyramid occupies O(\sum{(width^2)*4^i)}) for i in [0,depth]
    # if the point sets are stored, a pyramid occupies O(d * width^2)
    def save(self, pyramid_directory, path_to_tile=None):
        if path_to_tile == None:
            l,i,j = self.pos
            path_to_tile = path.join(pyramid_directory, f'tile_z{l}_x{i}_y{j}.json')
        tile_dict = dict()
        tile_dict['id'] = self.id
        tile_dict['pos'] = self.pos
        tile_dict['rect'] = self.rect
        tile_dict['fitted_rect'] = self.fitted_rect
        tile_dict['points'] = self.points
        dump(tile_dict, open(path_to_tile, 'w'))

    @classmethod
    def load(cls, path_to_tile, width=100):
        tile_dict = load(open(path_to_tile, 'r'))
        return cls(tile_dict['id'], tile_dict['pos'], tile_dict['points'], tile_dict['rect'],
                   fitted_rect=tile_dict['fitted_rect'], width=width)

    @classmethod
    def from_query(cls, pyramid_directory, query):
        l,i,j = query.coordinates
        width = query.resolution
        path_to_file = path.join(pyramid_directory, f'tile_z{l}_x{i}_y{j}.json')
        return cls.load(path_to_file, width=width)
