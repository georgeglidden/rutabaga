from numpy import histogram2d, max as np_max, min as np_min
from json import dump as json_dump, load as json_load
from os import path
from bisect import bisect_left, bisect_right

class TileQuery:
    def __init__(self, coordinates, resolution, options = {'pq':False, 'threshold_pq':False, 'bright':False}):
        self.coordinates = coordinates
        self.resolution = resolution
        self.options = options

class Tile:
# the Tile class holds all the information necessary to
# 1. save and restore pointsets to and from a pyramid file structure;
#    enable the TileServer to respond to PointSetQuery GET requests
# 2. provide a TileClient with everything it needs to quickly render the pointset
    def __init__(self, tile_id, pos, pointset, rect, fitted_rect = None, width=100, options = {'pq':False, 'threshold_pq':False, 'bright':True}):
        self.id = tile_id
        self.pos = (int(pos[0]),int(pos[1]),int(pos[2]))
        self.width = width
        self.rect = [self.l, self.r, self.t, self.b] = rect
        rect_bounds = [(self.l,self.t),(self.r,self.t),(self.r,self.b),(self.l,self.b)]

        if len(pointset) == 0:
            self.points = rect_bounds
        else:
            self.points = pointset
        self.n = len(self.points)
        if options['pq'] == True:
            if len(self.points[0]) == 4:
                self.points.sort(key=lambda x:x[2]/x[3])
            else:
                print('no pq values found for tile', tile_id)
        self.vals = list(zip(*self.points)) # unzip pointset
        assert all([len(v) == self.n for v in self.vals])
        self.xvals, self.yvals = self.vals[:2]
        if fitted_rect == None:
            fitted_rect = [min(self.xvals),max(self.xvals),min(self.yvals),max(self.yvals)]
        self.fitted_rect = fitted_rect
        self.xbounds,self.ybounds = list(zip(*rect_bounds)) # unzip bound set
        self._density_map = None
        self._max_density = None
        self._options = options

    def render(self, options=None):
        if options == None:
            options = self._options
        if type(self._density_map) == type(None):
            self._density_map, _, __ = histogram2d(self.xvals+self.xbounds,self.yvals+self.ybounds,self.width+1)
            # remove corner marker
            self._density_map[0,0] -= 1
            # remove redundant columns and rows
            self._density_map = self._density_map[:self.width,:self.width]
            # scale to [0,1]
            self._max_density = np_max(self._density_map)
            if self._max_density > 0:
                self._density_map /= self._max_density
        print(options['threshold_pq'])
        if options['threshold_pq']:
            thr = options['threshold_pq']
            try:
                max_pq = bisect_left([self.vals[2][i]/self.vals[3][i] for i in range(self.n)], thr)
                #print('THRESHOLDING INDEX / TOTAL POINTS', max_pq/self.n)
            except:
                print('cannot perform pq thresholding on points without p and q values. restart the server with the option -r to load riley roots from your csv.')
                max_pq = -1
            self._density_map, _, __ = histogram2d(self.xvals[:max_pq]+self.xbounds,self.yvals[:max_pq]+self.ybounds,self.width+1)
            # remove corner marker
            self._density_map[0,0] -= 1
            # remove redundant columns and rows
            self._density_map = self._density_map[:self.width,:self.width]
            # scale to [0,1]
            self._max_density = np_max(self._density_map)
            if self._max_density > 0:
                self._density_map /= self._max_density
        tile_img = self._density_map
        if options['bright'] == True:
            tile_img = tile_img > 0
        return tile_img

    def max_density(self):
        if self._max_density == None:
            self.density_map()
        return self._max_density

    def metadata(self):
        tile_data = dict()
        tile_data['id'] = self.id
        tile_data['pos'] = self.pos
        tile_data['rect'] = self.rect
        tile_data['n'] = self.n
        tile_data['fitted_rect'] = self.fitted_rect
        tile_data['initialization'] = {
            'resolution':self.width,
            'max_density':self.max_density()
        }
        return tile_data

    # the pointset is saved rather than the density map to prevent a storage
    # req. explosion: for n points,
    # if the density maps are stored, a pyramid occupies
    # O(\sum{(width^2)*4^i)} * n) for i in [0,depth]
    # if the point sets are stored, a pyramid occupies O(d * width^2 * n)
    def save(self, pyramid_directory, path_to_tile=None):
        if path_to_tile == None:
            l,i,j = self.pos
            path_to_tile = path.join(pyramid_directory, f'z{l}', f'x{i}_y{j}.tile')
        tile_data = self.metadata()
        tile_data['points'] = self.points
        json_dump(tile_dict, open(path_to_tile, 'w'))

    @classmethod
    def load(cls, path_to_tile, width=100):
        tile_dict = json_load(open(path_to_tile, 'r'))
        return cls(tile_dict['id'], tile_dict['pos'], tile_dict['points'], tile_dict['rect'],
                   fitted_rect=tile_dict['fitted_rect'], width=width)

    @classmethod
    def from_query(cls, pyramid_directory, query):
        l,i,j = query.coordinates
        width = query.resolution
        path_to_file = path.join(pyramid_directory, f'z{l}', f'x{i}_y{j}.tile')
        return cls.load(path_to_file, width=width)
