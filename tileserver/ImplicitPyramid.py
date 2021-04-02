from Tile import *
from bisect import bisect_left, bisect_right
from collections import deque

class ImplicitPyramid:

    def __init__(self, point_set, bounds, source, label, memory=128, options = {'pq':False, 'threshold_pq':False, 'bright':True}):
        self.label = label
        self.source = source
        self.bounds = self.left, self.right, self.top, self.bottom = bounds
        self.width = self.bounds[1] - self.bounds[0]
        self.height = self.bounds[3] - self.bounds[2]
        self.point_set = sorted(point_set, key=lambda x:x[0])
        self.n = len(point_set)
        self.x_set = [p[0] for p in self.point_set]
        self._options = options
        self.memory = memory
        self._active_tiles = deque([])

    def metadata(self):
        pyr_data = dict()
        pyr_data['label'] = self.label
        pyr_data['source'] = self.source
        pointset_data = dict()
        pointset_data['cardinality'] = self.n
        pointset_data['left'] = self.left
        pointset_data['right'] = self.right
        pointset_data['top'] = self.top
        pointset_data['bottom'] = self.bottom
        pyr_data['pointset'] = pointset_data
        return pyr_data

    def psq_to_rect(self, query):
        l,j,i = query.coordinates
        x = self.left + i*(2**(-l)) * self.width
        y = self.top + j*(2**(-l)) * self.height
        return [x, x + (2**(-l)) * self.width, y, y + (2**(-l)) * self.height]

    def points_in_rect(self, rect, verbose=False):
        x0,x1,y0,y1 = rect
        i1 = bisect_left(self.x_set, x0)
        i2 = bisect_right(self.x_set, x1)
        candidate_points = sorted(self.point_set[i1:i2], key=lambda x:x[1])
        y_set = [p[1] for p in candidate_points]
        j1 = bisect_left(y_set, y0)
        j2 = bisect_right(y_set, y1)
        m = len(candidate_points)
        if verbose:
            print('QUERY X POSITIONS', (x0,x1))
            print('QUERY X INDICES', (i1/self.n,i2/self.n))
            print('QUERY Y POSITIONS', (y0,y1))
            print('QUERY Y INDICES', (j1/m,j2/m))
        return candidate_points[j1:j2]

    def query(self, tile_query, verbose=True, options=None):
        q_rect = self.psq_to_rect(tile_query)
        q_points = self.points_in_rect(q_rect)
        if options == None:
            options = self._options
        in_memory = tile_query.coordinates[:3] in [tile.pos[:3] for tile in self._active_tiles]
        if in_memory:
            i = [tile.pos[:3] for tile in self._active_tiles].index(tile_query.coordinates[:3])
            response = self._active_tiles[i]
        else:
            response = Tile(-1, tile_query.coordinates, q_points, q_rect, width=tile_query.resolution, options=options)
            self._active_tiles.append(response)
            print(len(self._active_tiles))
            if len(self._active_tiles) > self.memory:
                self._active_tiles.popleft()
        if verbose:
            print('QUERY RECT',q_rect)
            print('QUERY N',len(q_points))
            print('QUERY FROM MEM',in_memory)
            print(options)
        return response

pyramids = dict()
initialized = False
def init_pyramids(source_points, source_labels, source_paths, bounds=None):
    global pyramids, initialized
    if bounds == None:
        bounds = [0,1,0,1]
    x0,x1,y0,y1 = bounds
    for i in range(len(source_points)):
        point_set = source_points[i]
        label = source_labels[i]
        source = source_paths[i]
        pyramids[label] = ImplicitPyramid(point_set, bounds, source, label)
    initialized = True

def do_tile_query(label, psq, options=None):
    global pyramids, initialized
    if initialized:
        return pyramids[label].query(psq,options=options)
    else:
        print('the ImplicitPyramid is not initialized')
        return -1

def do_meta_query(label):
    global pyramids, initialized
    if initialized:
        return pyramids[label].metadata()
    else:
        print('the ImplicitPyramid is not initialized')
        return -1
