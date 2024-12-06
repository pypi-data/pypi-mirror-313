import numpy as np
import json
from skimage import measure

N = 2
lon, lat = np.meshgrid(np.arange(-180, 180+N, N), np.arange(-90, 90+N, N))

lon = lon.tolist()
lat = lat.tolist()

grid = {'lon': lon, 'lat': lat}
with open('grid.json', 'w') as file:
    json.dump(grid, file)

#  ──────────────────────────────────────────────────────────────────────────

polygon_points = [(10, 0), (10, 10), (0, 0)]
polygon = {'points': polygon_points}

with open('polygon0.json', 'w') as file:
    json.dump(polygon, file)

polygon_points = [(16, 0), (4, 10), (16, 16)]
polygon = {'points': polygon_points}

with open('polygon1.json', 'w') as file:
    json.dump(polygon, file)

#  ──────────────────────────────────────────────────────────────────────────

polygon_points = [(30, 10), (40, 40), (0, 30)]
polygon = {'points': polygon_points}

with open('polygon2.json', 'w') as file:
    json.dump(polygon, file)

polygon_points = [(-100, -50), (-110, -10), (-50, -20), (-50, -50)]
polygon = {'points': polygon_points}

with open('polygon3.json', 'w') as file:
    json.dump(polygon, file)

#  ──────────────────────────────────────────────────────────────────────────

grid_points = np.array([np.array(grid['lon']).flatten('C'), np.array(grid['lat']).flatten('C')]).transpose()
mask = measure.points_in_poly(grid_points, polygon_points).reshape(np.array(grid['lon']).shape, order='C').astype(int)
print(np.array2string(mask, max_line_width=300))
