import xarray as xr
import json
import numpy as np
from skimage import measure

data = xr.open_dataset('./NEMO_1993-2013_D.nc')

lon = data.nav_lon_grid_T.values
lat = data.nav_lat_grid_T.values

grid = {'lon': lon.tolist(), 'lat': lat.tolist()}
with open('nemo_grid.json', 'w') as file:
    json.dump(grid, file)

#  ──────────────────────────────────────────────────────────────────────────

polygon_points = [(4.0, 39.0), (7.0, 42.0), (11.0, 42.0), (11.0, 38.0)]

polygon = {'points': polygon_points}

with open('nemo_polygon.json', 'w') as file:
    json.dump(polygon, file)

#  ──────────────────────────────────────────────────────────────────────────

grid_points = np.array([np.array(grid['lon']).flatten('C'), np.array(grid['lat']).flatten('C')]).transpose()
mask = measure.points_in_poly(grid_points, polygon_points).reshape(np.array(grid['lon']).shape, order='C').astype(int)
