import numpy as np
import json
from skimage import measure
from scipy import interpolate

def adjust_for_center_longitude(x):
    x = np.array(x)
    x = np.where(x < -180, x + 360, x)
    x = np.where(x > 180, x - 360, x)
    return x

cl = 150
N = 10

lon = np.arange(cl-180, cl+180+N, N)
lon = adjust_for_center_longitude(lon)
lon, lat = np.meshgrid(lon, np.arange(-90, 90+N, N))

print(np.array2string(lon, max_line_width=300))

lon = lon.tolist()
lat = lat.tolist()

grid = {'lon': lon, 'lat': lat}
with open('off_center_grid.json', 'w') as file:
    json.dump(grid, file)

#  ──────────────────────────────────────────────────────────────────────────

polygon_points = [(135, 0), (-143.5, 50), (-169.8, -50)]
polygon = {'points': polygon_points}

with open('off_center_polygon.json', 'w') as file:
    json.dump(polygon, file)

#  ──────────────────────────────────────────────────────────────────────────

neutral_lon, _ = np.meshgrid(np.arange(np.array(grid['lon']).shape[1]), np.arange(np.array(grid['lat']).shape[0]))
print(np.array2string(neutral_lon, max_line_width=300))

grid_points = np.array([np.array(grid['lon']).flatten('C'), np.array(grid['lat']).flatten('C')]).transpose()
mask = measure.points_in_poly(grid_points, polygon_points).reshape(np.array(grid['lon']).shape, order='C').astype(int)

print(polygon_points)
print(np.array2string(mask, max_line_width=300))

polygon_points = np.array(polygon_points)

neutral_grid_points = np.array([neutral_lon.flatten('C'), np.array(grid['lat']).flatten('C')]).transpose()

neutral_polygon_points = interpolate.griddata(grid_points, neutral_lon.flatten('C'), polygon_points)
neutral_polygon_points = np.stack((neutral_polygon_points, polygon_points[:,1]), axis=1)

print(neutral_polygon_points)

mask = measure.points_in_poly(neutral_grid_points, neutral_polygon_points).reshape(np.array(grid['lon']).shape, order='C').astype(int)
print(np.array2string(mask, max_line_width=300))
