from Tile import *
from Pyramid import load_from_csv, load_from_img
from bisect import bisect_left, bisect_right

class ImplicitPyramid:

    def __init__(self, point_set, bounds):
        self.bounds = bounds
        self.left = self.bounds[0]
        self.top = self.bounds[2]
        self.width = self.bounds[1] - self.bounds[0]
        self.height = self.bounds[3] - self.bounds[2]
        self.point_set = sorted(point_set, key=lambda x:x[0])
        self.n = len(point_set)
        self.x_set = [p[0] for p in self.point_set]
        print(f'initialized ImplicitPyramid with {self.n} points\n\tbounded by ({self.width},{self.height})')

    def psq_to_rect(self, query):
        l,j,i = query.coordinates
        x = self.left + i*(2**(-l)) * self.width
        y = self.top + j*(2**(-l)) * self.height
        return [x, x + (2**(-l)) * self.width, y, y + (2**(-l)) * self.height]

    def points_in_rect(self, rect):
        x0,x1,y0,y1 = rect
        i1 = bisect_left(self.x_set, x0)
        i2 = bisect_right(self.x_set, x1)
        print('QUERY X POSITIONS', (x0,x1))
        print('QUERY X INDICES', (i1/self.n,i2/self.n))
        candidate_points = sorted(self.point_set[i1:i2], key=lambda x:x[1])
        y_set = [p[1] for p in candidate_points]
        j1 = bisect_left(y_set, y0)
        j2 = bisect_right(y_set, y1)
        m = len(candidate_points)
        print('QUERY Y POSITIONS', (y0,y1))
        print('QUERY Y INDICES', (j1/m,j2/m))
        return candidate_points[j1:j2]

    def query(self, query):
        q_rect = self.psq_to_rect(query)
        q_points = self.points_in_rect(q_rect)
        print('QUERY RECT',q_rect)
        print('QUERY N',len(q_points))
        return Tile(-1, query.coordinates, q_points, q_rect, width = query.resolution)

pyramids = dict()
initialized = False
def init_point_sources(source_paths, source_labels, bounds=None):
    global pyramids, initialized
    if bounds == None:
        bounds = [0,1,0,1]
    x0,x1,y0,y1 = bounds
    for i in range(len(source_paths)):
        source = source_paths[i]
        point_set = load_from_csv(source, x_bounds=(x0,x1), y_bounds=(y0,y1))
        label = source_labels[i]
        pyramids[label] = ImplicitPyramid(point_set, bounds)
    initialized = True

def do_query(label, psq):
    global pyramids, initialized
    if initialized:
        return pyramids[label].query(psq)
    else:
        print('the ImplicitPyramid is not initialized')
        return -1
