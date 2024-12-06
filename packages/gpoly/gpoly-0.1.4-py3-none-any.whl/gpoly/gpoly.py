import sys, json, click, importlib.metadata
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patheffects as pe
import numpy as np
from skimage import measure
from scipy import interpolate

#  ──────────────────────────────────────────────────────────────────────────
# global variables

gpoly_version = importlib.metadata.version('gpoly')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

#  ──────────────────────────────────────────────────────────────────────────
# global options

grid_json_option = click.option('-g', '--grid', 'grid_json', type=click.Path(exists=True), help='Path to gpoly-ready grid.JSON file', required=True)

# resolutions

res_option = click.option('-r', '--res', type=click.Choice(['110m', '50m', '10m']), default='110m', show_default=True, help='Resolution of the coastline; lower resolution is faster.')

grid_res_option = click.option('-gr', '--grid-res', 'grid_res', type=float, default=10, show_default=True, help='Resolution of the gridlines in degrees. Default is 10 deg.')

snap_grid_res_option = click.option('-sgr', '--snap-grid-res', 'snap_grid_res', type=str, default='1', show_default=True, help='Resolution of the snapping gridlines in degrees. Default is 1 deg.')

center_lon_option = click.option('-cl', '-center-longitude', 'center_lon', nargs=1, type=float, default=0, help='Set center view of the map (-cl lon./east); e.g. -cl -178 for the northern Pacific Ocean.')

extent_option = click.option('-e', '-ext', '--extent', nargs=4, type=click.Tuple([float, float, float, float]), default=(-180, 180, -90, 90), help='Set the extent of the map (-e lon./west lon./east lat./south lat./north); e.g. -e -7 37 29 47 for the Med. Sea.')

polygon_points_option = click.option('--polygon_points/--no-polygon-points', '-PP/-NPP', 'polygon_points_flag', show_default=True, default=True, help='Show polygon points (points will only be shown if polygons are also shown).')

labels_option = click.option('--labels/--no-labels', '-L/-NL', 'labels_flag', show_default=True, default=True, help='Show polygon/mask labels.')

#  ──────────────────────────────────────────────────────────────────────────
# global functions

def adjust_for_center_longitude(x):
    x = np.array(x)
    x = np.where(x < -180, x + 360, x)
    x = np.where(x > 180, x - 360, x)
    return x


def snap_grid(snap_grid_res, center_lon):

    # handling moving center longitude
    tmp_lon = np.arange(center_lon - 180, center_lon + 180, snap_grid_res)
    tmp_lon = adjust_for_center_longitude(tmp_lon)

    snap_lon, snap_lat = np.meshgrid(tmp_lon, np.arange(-90, 90 + snap_grid_res, snap_grid_res))
    return snap_lon.flatten(order='C'), snap_lat.flatten(order='C')


def snapping(x, y, snap_x, snap_y, center_lon):

    # adjusting for moving x axis center longitude
    x += center_lon
    x = adjust_for_center_longitude(x)

    dist = ( (snap_x - x)**2 + (snap_y - y)**2 )**.5
    return np.argmin(dist)


def plot_polygons(ax, polygons, center_lon, points=True, labels=True):
    """
    zorder for polygons are in the 40's and up range
    """

    colors = plt.get_cmap('rainbow', len(polygons))

    lons, lats = [], []
    for i, polygon in enumerate(polygons):
        lons.append(np.array(polygon['points'])[:,0])
        lats.append(np.array(polygon['points'])[:,1])

    for i, _ in enumerate(lons):
        ax.fill(adjust_for_center_longitude(lons[i] - center_lon), lats[i], transform=ccrs.PlateCarree(center_lon), color=colors(i), alpha=0.7, zorder=30+i/len(lons)) # fourth layer

        # adding polygon points
        if points:
            ax.scatter(adjust_for_center_longitude(lons[i] - center_lon), lats[i], transform=ccrs.PlateCarree(center_lon), color=colors(i), edgecolor='k', zorder=30+i/len(lons)) # fourth layer

        # adding polygon label
        if labels:
            center = (np.mean(adjust_for_center_longitude(lons[i] - center_lon)), np.mean(lats[i]))
            ax.text(center[0], center[1], s=str(i), color=colors(i), transform=ccrs.PlateCarree(center_lon), path_effects=[pe.withStroke(linewidth=4, foreground='k')], zorder=100) # always on top layer

    return ax


def plot_earth(res, grid_res, extent, center_lon):

    colors = {'land': (27/255, 255/255, 0, 0.7),
              'ocean': (0, 122/255, 255/255, 0.7),
              'point': (245/255, 40/255, 145/255, 1),
              'polygon': (245/255, 40/255, 145/255, 0.75),
              }

    coast = cfeature.NaturalEarthFeature('physical', 'land', res, edgecolor=None, facecolor=colors['land'])
    ocean = cfeature.NaturalEarthFeature('physical', 'ocean', res, edgecolor=None, facecolor=colors['ocean']) 

    # make world plot
    proj = ccrs.PlateCarree(central_longitude=center_lon)
    fig, ax = plt.subplots(1, 1, subplot_kw={'projection': proj})

    # setting up gridlines for lat. long.
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=.75, color='black', alpha=0.1, linestyle='--', zorder=2)

    # removing upper and right lat. long. labels
    gl.top_labels = False
    gl.right_labels = False

    # fixing lat long. locations
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, grid_res)) # longitude
    gl.ylocator = mticker.FixedLocator(np.arange(-90, 90 + grid_res, grid_res))  # latitude
    gl.xformatter = LONGITUDE_FORMATTER  # formatter needed to get proper labels
    gl.yformatter = LATITUDE_FORMATTER

    gl.xlabel_style = {'rotation': 90}

    # add coast and ocean
    ax.add_feature(coast, zorder=1)
    ax.add_feature(ocean, zorder=1)

    # extent
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    fig.tight_layout()
    fig.canvas.draw()

    ax.autoscale(False)

    return fig, ax, colors

#  ──────────────────────────────────────────────────────────────────────────
# global classes

class SnappingCursor:
    """
    A cross-hair cursor that snaps to the data point of a line, which is
    closest to the *x* position of the cursor.

    For simplicity, this assumes that *x* values of the data are sorted.
    """
    def __init__(self, ax, snap_grid_res, center_lon):
        self.ax = ax
        self.res = snap_grid_res
        self.center_lon = center_lon
        self.get_decimals()
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--', zorder=100) # always on top layer
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--', zorder=100) # always on top layer
        self.x, self.y = snap_grid(self.res, self.center_lon)
        self._last_index = None
        self.text = ax.text(0.725, 0.925, '', transform=ax.transAxes, weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground='white')], zorder=100) # text location in axes coords; always on top layer


    def get_decimals(self):
        if '.' in self.res:
            self.decimals = len(self.res.split('.')[-1])
        else:
            self.decimals = 0
        self.res = float(self.res)


    def plot_polygons(self, lon, lat, colors):

        if len(lon) > 0:
            points = self.ax.scatter(adjust_for_center_longitude(np.array(lon) - self.center_lon), lat, transform=ccrs.PlateCarree(self.center_lon), color=colors['point'], edgecolor='k', zorder=40)
            polygon = self.ax.fill(adjust_for_center_longitude(np.array(lon) - self.center_lon), lat, transform=ccrs.PlateCarree(self.center_lon), color=colors['polygon'], zorder=40)

        self.ax.figure.canvas.draw()

        if len(lon) > 0:
            points.remove()
            polygon[0].remove()


    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw


    def on_mouse_move(self, event, lon, lat, colors):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)

            # drawing polygons
            if need_redraw:
                self.plot_polygons(lon, lat, colors)

        else:
            self.set_cross_hair_visible(True)
            index = snapping(event.xdata, event.ydata, self.x, self.y, self.center_lon)

            if index == self._last_index:
                return  # still on the same data point. Nothing to do.

            self._last_index = index
            x = self.x[index]
            y = self.y[index]

            # update the line positions; relative to plotted axes
            self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata([adjust_for_center_longitude(x - self.center_lon)]) # adjusting for moving center longitude
            self.text.set_text(f'Lon.={x:1.{self.decimals}f}, Lat.={y:1.{self.decimals}f}')

            # drawing polygons
            self.plot_polygons(lon, lat, colors)

#  ──────────────────────────────────────────────────────────────────────────
# base command, center_lon

@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(gpoly_version)
@click.pass_context
def gpoly(ctx):
    pass

#  ──────────────────────────────────────────────────────────────────────────
# mapping command to draw a polygon

@gpoly.command('map', short_help='Polygon creation tool.')
@res_option
@grid_res_option
@snap_grid_res_option
@center_lon_option
@extent_option
@polygon_points_option
@labels_option
@click.option('-p', '--polygons', 'polygon_jsons', type=click.Path(exists=True), multiple=True, help='')
@click.pass_context
def map(ctx, res, grid_res, snap_grid_res, center_lon, extent, polygon_points_flag, labels_flag, polygon_jsons):
    """
    Create a polygon on the world map. Outputs a JSON object with the polygon vertices.
    """

    def onclick(event, ax, colors, lon, lat, snap_lon, snap_lat, center_lon):

        if event.button == 3: # only works with right click to avoid clicking interference while zooming

            index = snapping(event.xdata, event.ydata, snap_lon, snap_lat, center_lon)

            lon.append(snap_lon[index])
            lat.append(snap_lat[index])

            points = ax.scatter(adjust_for_center_longitude(np.array(lon) - center_lon), lat, transform=ccrs.PlateCarree(center_lon), color=colors['point'], edgecolor='k', zorder=40)
            polygon = ax.fill(adjust_for_center_longitude(np.array(lon) - center_lon), lat, transform=ccrs.PlateCarree(center_lon), color=colors['polygon'], zorder=40)

            fig.canvas.draw()

            points.remove()
            polygon[0].remove()


    fig, ax, colors = plot_earth(res, grid_res, extent, center_lon)

    # initiating map with points
    lon, lat = [], []

    snap_lon, snap_lat = snap_grid(float(snap_grid_res), center_lon)
    fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, ax, colors, lon, lat, snap_lon, snap_lat, center_lon))

    # adding polygons
    polygons = []
    for polygon_json in polygon_jsons:
        with open(polygon_json, 'r') as file:
            polygons.append(json.load(file))

    ax = plot_polygons(ax, polygons, center_lon, points=polygon_points_flag, labels=labels_flag)

    # snapping
    snap_cursor = SnappingCursor(ax, snap_grid_res, center_lon)
    fig.canvas.mpl_connect('motion_notify_event', lambda event: snap_cursor.on_mouse_move(event, lon, lat, colors))

    plt.show()

    data = {'gpoly': gpoly_version,
            'description': 'Geopoly JSON containing the vertices of the polygon. Stored in a list of (longitude, latitude) tuples.',
            'points': [],
            }

    for i, loni in enumerate(lon):
        data['points'].append((loni, lat[i]))

    click.echo(json.dumps(data))

#  ──────────────────────────────────────────────────────────────────────────
# make grid masks with polygons

@gpoly.command('mask', short_help='Create a polygon(s) mask(s) for a grid.')
@grid_json_option
@click.argument('polygon_jsons', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def mask(ctx, grid_json, polygon_jsons):
    """
    Create a mask of the given grid in the grid.JSON file marking the points within the polygons given in the POLYGON_JSONS files. Outputs a JSON object containing the grid, masks, and polygons.

    The grid.JSON file needs to have 2D grids for both the 'lon' and 'lat' keys.

    When giving multiple POLYGON_JSONS files, if they overlap, the polygons supplied first maintain their boundaries and overlaps in the proceeding masks are removed (first listed, first prioritized).
    """

    with open(grid_json, 'r') as file:
        grid = json.load(file)

    # adding polygons
    polygons = []
    for polygon_json in polygon_jsons:
        with open(polygon_json, 'r') as file:
            polygons.append(json.load(file))

    # masking
    grid_points = np.array([np.array(grid['lon']).flatten(order='C'), np.array(grid['lat']).flatten(order='C')]).transpose()

    # making neutral grid to overcome masks that cross the international dateline
    neutral_lon, _ = np.meshgrid(np.arange(np.array(grid['lon']).shape[1]), np.arange(np.array(grid['lat']).shape[0]))
    neutral_grid_points = np.array([neutral_lon.flatten(order='C'), np.array(grid['lat']).flatten(order='C')]).transpose()

    masks = []
    for i, polygon in enumerate(polygons):
        polygon_points = polygon['points']
        polygon_points = np.array(polygon_points)

        neutral_polygon_points = interpolate.griddata(grid_points, neutral_lon.flatten('C'), polygon_points)
        neutral_polygon_points = np.stack((neutral_polygon_points, polygon_points[:,1]), axis=1)

        masks.append(measure.points_in_poly(neutral_grid_points, neutral_polygon_points).reshape(np.array(grid['lon']).shape, order='C').astype(int))

    # capturing overlapping
    overlaps = []
    for i, maski in enumerate(masks):
        for j, maskj in enumerate(masks):
            if not maski.astype(bool) is maskj.astype(bool):
                if j > i: # order matters; precedence equals priority
                    overlap = maski.astype(bool) & maskj.astype(bool)
                    if overlap.any():
                        overlaps.append((i, j, overlap))

    for overlap in overlaps:
        masks[overlap[1]][overlap[-1]] = 0

    # preparing data
    for i, mask in enumerate(masks):
        masks[i] = mask.tolist()

    data = {'gpoly': gpoly_version,
            'description': 'Mask JSON file for grid points inside the given polygon (provided in the "polygon" key: 1 for within polygon, 0 for outside.',
            'grid': grid,
            'masks': masks,
            'polygons': polygons,
            }

    click.echo(json.dumps(data))

#  ──────────────────────────────────────────────────────────────────────────
# make grid mask with polygon

@gpoly.command('show', short_help='Show grid/masks/polygons.')
@res_option
@grid_res_option
@snap_grid_res_option
@extent_option
@click.option('--grid/--no-grid', '-G/-NG', 'grid_flag', show_default=True, default=True, help='Show grid.')
@click.option('--masks/--no-masks', '-M/-NM', 'masks_flag', show_default=True, default=True, help='Show masks.')
@click.option('--polygons/--no-polygons', '-P/-NP', 'polygons_flag', show_default=True, default=True, help='Show polygons.')
@polygon_points_option
@labels_option
@click.argument('masks_json', type=click.Path(exists=True))
@click.pass_context
def show(ctx, res, grid_res, snap_grid_res, extent, grid_flag, masks_flag, polygons_flag, polygon_points_flag, labels_flag, masks_json):
    """
    Show polygon masks and polygons from the MASKS_JSON.
    """

    with open(masks_json, 'r') as file:
        tmp = json.load(file)
        grid = tmp['grid']
        masks = tmp['masks']
        polygons = tmp['polygons']

    grid_points = np.array([np.array(grid['lon']).flatten(order='C'), np.array(grid['lat']).flatten(order='C')]).transpose()

    # grid center longitude; for proper polygon plotting
    tmp_averaged_lon = np.nanmean(np.array(grid['lon']), axis=0)
    center_grid_lon = tmp_averaged_lon[int(len(tmp_averaged_lon)//2)]

    # global plot and colors
    fig, ax, _ = plot_earth(res, grid_res, extent, center_grid_lon) # first layer
    colors = plt.get_cmap('rainbow', len(masks))

    # adding grid points
    if grid_flag:
        ax.scatter(adjust_for_center_longitude(grid_points[:,0] - center_grid_lon), grid_points[:,1], transform=ccrs.PlateCarree(center_grid_lon), color='k', marker='+', zorder=10) # second layer

    # adding masks
    if masks_flag:
        for i, _ in enumerate(masks):
            mask = np.array(masks[i]).flatten(order='C').astype(bool)
            ax.scatter(adjust_for_center_longitude(grid_points[mask,0] - center_grid_lon), grid_points[mask,1], transform=ccrs.PlateCarree(center_grid_lon), color=colors(i), zorder=20) # third layer

    # adding polygons
    if polygons_flag:
        ax = plot_polygons(ax, polygons, center_grid_lon, points=polygon_points_flag, labels=labels_flag) # fourth layer

    # snapping
    snap_cursor = SnappingCursor(ax, snap_grid_res, center_grid_lon)
    fig.canvas.mpl_connect('motion_notify_event', lambda event: snap_cursor.on_mouse_move(event, [], [], []))

    plt.show()
