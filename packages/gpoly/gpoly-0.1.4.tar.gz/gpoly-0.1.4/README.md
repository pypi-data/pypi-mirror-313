# geopoly

Simple "CLI" tool to mark polygons on a global map (with zooming) and then produce masks with said polygons with a given grid.

## Install

Install with:

```
pipx install gpoly
```

Or with the following for Apple Silicon:

```
pipx install gpoly --pip-args='--no-binary :all:'
```

## Example grid.JSON

Example python script to make the `grid.json`:

```
import numpy as np
import json

# resolution of 2 degree grid
N = 2
lon, lat = np.meshgrid(np.arange(-180, 180+N, N), np.arange(-90, 90+N, N))

lon = lon.tolist()
lat = lat.tolist()

# saving as a json file with the 'lat' and 'lon' keywords
grid = {'lon': lon, 'lat': lat}
with open('grid.json', 'w') as file:
    json.dump(grid, file)
```
