from numpy import histogram2d as hist2d
import numpy as np
from os import path
from csv import reader

#### CHANGE ME #########################
path_to_data = '../data/roots_130.csv'
########################################

def get_points(path_to_data):
    points = []
    with open(path_to_data, newline='') as data_file:
        data = reader(data_file)
        i = 0
        for line in data:
            l,r,i,q,e = line
            if l == '':
                continue
            else:
                r,i,q,e = float(r),float(i),int(q),float(e)
                points.append((r,i))
    return points

def format_names(path_to, e, r, t):
    return [path.join(path_to,f'_l{e+1}_y{2*r+v}_x{2*t+b}') for v in range(2) for b in range(2)]

def recursive_quad(width, path, max_depth, points, layer, i, j, x_l, x_r, y_l, y_r):
    x_m = (x_l + x_r) / 2
    y_m = (y_l + y_r) / 2
    #print(x_m, y_m)
    if len(points) > 0:
        points_xsort = sorted(points, key=lambda x:x[0])
        x_midean = min(points_xsort, key=lambda x: abs(x[0] - x_m))
        x_mid = points_xsort.index(x_midean)
        points_left = sorted(points_xsort[x_mid:], key=lambda x:x[1])
        if len(points_left) > 0:
            y_midean_l = min(points_left, key=lambda x: abs(x[1] - y_m))
            y_mid_l = points_left.index(y_midean_l)
            q1 = points_left[y_mid_l:]
            q4 = points_left[:y_mid_l]
        else:
            q1 = []
            q4 = []

        points_right = sorted(points_xsort[:x_mid], key=lambda x:x[1])
        if len(points_right) > 0:
            y_midean_r = min(points_right, key=lambda x: abs(x[1] - y_m))
            y_mid_r = points_right.index(y_midean_r)
            q2 = points_right[y_mid_r:]
            q3 = points_right[:y_mid_r]
        else:
            q2 = []
            q3 = []
        print(len(points_left),len(points_right))
        quads = [q1,q2,q3,q4]
    else:
        quads = [[],[],[],[]]
    #print((i,j))
    files = format_names(path, layer, i, j)
    for w in range(4):
        q = quads[w]
        f = files[w]
        hist, _, _ = hist2d([x[0] for x in q],[x[1] for x in q],width)
        np.savez_compressed(f,hist)

    if layer < max_depth-1:
        recursive_quad(width, path, max_depth, quads[0], layer+1, 2*i, 2*j, x_l, x_m, y_l, y_m)
        recursive_quad(width, path, max_depth, quads[1], layer+1, 2*i, 2*j+1, x_m, x_r, y_l, y_m)
        recursive_quad(width, path, max_depth, quads[2], layer+1, 2*i+1,2*j+1, x_m, x_r, y_m, y_r)
        recursive_quad(width, path, max_depth, quads[3], layer+1, 2*i+1, 2*j, x_l, x_m, y_m, y_r)

def main():
    import sys
    path_data = sys.argv[1]     # /data/roots_130.csv
    path_store = sys.argv[2]    # /data/roots_130_pyramid/
    l = int(sys.argv[3])        # 9
    d = int(sys.argv[4])        # 4
    width = int(sys.argv[5])    # 512

    points = get_points(path_data)
    print(f'loaded {len(points)} points')
    xmin = -1700/(2**(l))
    xmax = 1700/(2**(l))
    ymin = -550/(2**(l))
    ymax = 550/(2**(l))
    restr_points = [p for p in points if xmin < p[0] < xmax and ymin < p[1] < ymax]
    print(f'using {len(restr_points)} to construct pyramid')
    hist, _, _ = hist2d([x[0] for x in restr_points],[x[1] for x in restr_points],width)
    np.savez_compressed(path.join(path_store,'_l0_y0_x0'),hist)
    recursive_quad(width, path_store, d, restr_points, 0, 0, 0, xmin, xmax, ymin, ymax)

if __name__ == '__main__':
    main()
