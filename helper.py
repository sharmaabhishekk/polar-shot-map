import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.projections import get_projection_class
from scipy.interpolate import interp1d
from matplotlib.projections import PolarAxes
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def setup_axes1(fig, rect):
    """
    Get a simple floating cartesian axis rotated at 25 degrees
    """
    tr = Affine2D().scale(1, 1).rotate_deg(25)

    grid_helper = floating_axes.GridHelperCurveLinear(
        tr, extremes=(0, 4, 0, 4))

    ax1 = floating_axes.FloatingSubplot(fig, rect, grid_helper=grid_helper)
    fig.add_subplot(ax1)

    aux_ax = ax1.get_aux_axes(tr)

    grid_helper.grid_finder.grid_locator1._nbins = 4
    grid_helper.grid_finder.grid_locator2._nbins = 4

    return ax1, aux_ax

def custom_axes():

    """ Get all our figure and axis instances
    """


    fig = plt.figure(figsize=(10,12))

    gs = fig.add_gridspec(nrows=14, ncols=12, wspace=0, hspace=0)
    ax = fig.add_subplot(gs[:, :], projection="polar")
    ax.grid(True, linestyle="-.", alpha=0.2, linewidth=0.7, color="k")
    ax.set_thetamin(25)
    ax.set_thetamax(295)

    ax1, aux_ax1 = setup_axes1(fig, 111)

    ax1_bbox = ax1.get_position()
    ax1_bbox.bounds = (0.53, 0.152, 0.53, 0.53)
    ax1.set_position(ax1_bbox)

    return fig, ax, ax1, aux_ax1

def ax_points(N, mean, step):
    '''
    Calculates N equidistant points on both sides of a number for one of the axes
        N: number of points,
        mean: the middlemost value,
        step: the spacing between points
    '''
    if N%2 == 1:
        return np.linspace(start = mean - round(N/2)*step,
                               stop = mean + round(N/2)*step + step,
                               num=N)
    elif N%2 == 0:
        return np.linspace( start = mean - ( (N/2 - 1)*step + step/2),
                             stop = mean + ( (N/2 - 1)*step + step/2),
                              num=N)

def plot_inset(x,y, axis_main, width, color="k" ):
    
    """ Inset a polar axis in the cartesian axis for the legend/key """
    
    ax_sub= inset_axes(axis_main, width=width, height=width, loc=10, 
                       bbox_to_anchor=(x,y),
                       bbox_transform=axis_main.transData, 
                       borderpad=0.0, axes_class=get_projection_class("polar"))
    
    ax_sub.set_theta_direction(-1)
    ax_sub.set_theta_offset(np.pi/2)
    ax_sub.set_rmax(30)
    ax_sub.set_rmin(0)

    ax_sub.set_thetagrids(angles=np.linspace(0,360, 11))
    ax_sub.grid(True, linestyle="-.", alpha=0.2, linewidth=0.7, color="k")
    ax_sub.set_xticklabels(" ")
    ax_sub.set_yticklabels(["", "5m", "", "15m", "", "25m", ""], size=7)
    ax_sub.set_rlabel_position(120)
    ax_sub.yaxis.set_tick_params(labelsize=5)
    ax_sub.spines["polar"].set_visible(False)

    for i in range(5):    
        c1, c2 = np.deg2rad([120,240])
        x = np.linspace(c1, c2, 500)
        y = interp1d( [c1, c2], [i,i])( x)
        ax_sub.plot(x, y, color=color)
        
    ax_sub.scatter(x=np.radians(270), y=3, marker="x", color=color)
    ax_sub.text(x=np.radians(280), y=3, s="Freekick", size=5)
    
    ax_sub.scatter(x=np.radians(76), y=3, marker="s", color=color)
    ax_sub.text(x=np.radians(86), y=3.5, s="Penalty", size=5)
    
    ax_sub.scatter(x=np.radians(360), y=2, marker="o", color=color)    
    ax_sub.text(x=np.radians(360), y=2.5, s="Open Play", size=5)


    return ax_sub

def imscatter(x, y, image_path, ax, zoom=1):

    """ function to plot an image at a point (x, y) on axis"""

    image = plt.imread(image_path)

    im = OffsetImage(image, zoom=zoom)
    im.set_zorder(10)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    return artists
    




