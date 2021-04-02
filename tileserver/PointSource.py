from csv import reader

def load_riley_roots(path_to_csv, x_bounds=(-1.0, 1.0), y_bounds=(-1.0, 1.0)):
    points = []
    with open(path_to_csv, newline='') as data_file:
        data = reader(data_file)
        for line in data:
            if line == '':
                continue
            l,x,y,p,q = line[:5]
            if l == '':
                continue
            else:
                x,y = float(x),float(y)
                p,q = int(p),int(q)
                if x_bounds[0] < x < x_bounds[1] and y_bounds[0] < y < y_bounds[1]:
                    points.append((x,y,p,q))
    print(f'loaded {len(points)} roots from {path_to_csv} bounded by x {x_bounds} y {y_bounds}')
    return points

def load_from_csv_2d(path_to_data, x_bounds=(-1.0, 1.0), y_bounds=(-1.0, 1.0)):
    points = []
    with open(path_to_data, newline='') as data_file:
        data = reader(data_file)
        for line in data:
            if line == '':
                continue
            l,x,y = line[:3]
            if l == '':
                continue
            else:
                x,y = float(x),float(y)
                if x_bounds[0] < x < x_bounds[1] and y_bounds[0] < y < y_bounds[1]:
                    points.append((x,y))
    print(f'loaded {len(points)} points from {path_to_data}')
    return points

def load_from_img_2d(impath,threshold):
    image = imread(impath,as_gray=True)
    rows,cols = image.shape
    points = []
    for i in range(rows):
        for j in range(cols):
            if image[i,j] < threshold:
                points.append((i,j))
    print(rows*cols)
    return points
