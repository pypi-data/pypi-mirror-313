# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:18:24 2024

@author: jablonski
"""

import logging
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as path_effects
import matplotlib.patches as mpatches

logger = logging.getLogger('PT3S')

def pNcd_pipes(ax=None, gdf=None, attribute=None, colors=['darkgreen', 'magenta'], legend_fmt=None, legend_values=None, norm_min=None, norm_max=None, query=None, line_width_factor=10, zorder=None):
    """
    pNcd_pipes: Plots pipes on axis with customization options.

    :param ax: Matplotlib axis object. If None, a new axis is created.
    :type ax: matplotlib.axes.Axes, optional
    :param gdf: Geospatial DataFrame containing the data to plot.
    :type gdf: geopandas.GeoDataFrame
    :param attribute: Column name in gdf of the data that should be plotted.
    :type attribute: str
    :param colors: List of colors to use for the colormap. Default is ['darkgreen', 'magenta'].
    :type colors: list, optional
    :param legend_fmt: Legend text for attribute. Default is attribute + '{:.4f}'.
    :type legend_fmt: str, optional
    :param legend_values: Specific values to use for value steps in legend. Default is None.
    :type legend_values: list, optional
    :param norm_min: Minimum value for normalization. Default is None.
    :type norm_min: float, optional
    :param norm_max: Maximum value for normalization. Default is None.
    :type norm_max: float, optional
    :param query: Query string to filter the data. Default is None.
    :type query: str, optional
    :param line_width_factor: Factor to influence width of the lines in the plot. Default is 10.
    :type line_width_factor: float, optional
    :param zorder: Determines order of plotting when calling the function multilpe times. Default is None.
    :type zorder: float, optional
    
    :return: patches.
    :rtype: matplotlib.patches.Patch
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

    try:
        if ax is None:
            fig, ax = plt.subplots(figsize=(11.7, 8.3))  # A3 size
            logger.debug("{0:s}{1:s}".format(logStr, 'Created new axis.'))

        if gdf is None or gdf.empty:
            logger.debug("{0:s}{1:s}".format(logStr, 'No plot data provided.'))
            return

        # Set default legend_fmt if not provided
        if legend_fmt is None:
            legend_fmt = attribute + ' {:4.0f}'

        # Create Colormap
        cmap = mcolors.LinearSegmentedColormap.from_list('cmap', colors, N=256)
        norm_min = norm_min if norm_min is not None else gdf[attribute].min()
        norm_max = norm_max if norm_max is not None else gdf[attribute].max()
        norm = plt.Normalize(vmin=norm_min, vmax=norm_max)
        logger.debug("{0:s}norm_min: {1:10.2f} norm_max: {2:10.2f}".format(logStr, norm_min, norm_max))

        # Filter and Sort Data if Query is Provided
        df = gdf.query(query) if query else gdf
        df = df.sort_values(by=[attribute], ascending=True)

        # Plotting Data with Lines
        sizes = norm(df[attribute].astype(float)) * line_width_factor  # Scale sizes appropriately
        df.plot(ax=ax,
                linewidth=sizes,
                color=cmap(norm(df[attribute].astype(float))),
                path_effects=[path_effects.Stroke(capstyle="round")],
                label=attribute,
                zorder=zorder)  # Add label for legend
        logger.debug("{0:s}{1:s}".format(logStr, f'Plotted {attribute} data.'))

        plt.axis('off')

        # Create Legend Patches
        legend_values = legend_values if legend_values is not None else np.linspace(norm_min, norm_max, num=5)
        logger.debug("{0:s}legend_values: {1}".format(logStr, legend_values))
        patches = [mpatches.Patch(color=cmap(norm(value)), label=legend_fmt.format(value)) for value in legend_values]

        return patches

    except Exception as e:
        logger.error("{0:s}{1:s} - {2}".format(logStr, 'Error.', str(e)))

    logger.debug("{0:s}{1:s}".format(logStr, 'End.'))

def pNcd_nodes(ax=None, gdf=None, attribute=None, colors=['darkgreen', 'magenta'], legend_fmt=None, legend_values=None, norm_min=None, norm_max=None, query=None, marker_style='o', marker_size_factor=1000.0, zorder=None):
    """
    pNcd_nodes: Plots nodes on axis with customization options.

    :param ax: Matplotlib axis object. If None, a new axis is created.
    :type ax: matplotlib.axes.Axes, optional
    :param gdf: Geospatial DataFrame containing the data to plot.
    :type gdf: geopandas.GeoDataFrame
    :param attribute: Column name in gdf of the data that should be plotted.
    :type attribute: str
    :param colors: List of colors to use for the colormap. Default is ['darkgreen', 'magenta'].
    :type colors: list, optional
    :param legend_fmt: Legend text for attribute. Default is attribute + '{:.4f}'.
    :type legend_fmt: str, optional
    :param legend_values: Specific values to use for value steps in legend. Default is None.
    :type legend_values: list, optional
    :param norm_min: Minimum value for normalization. Default is None.
    :type norm_min: float, optional
    :param norm_max: Maximum value for normalization. Default is None.
    :type norm_max: float, optional
    :param query: Query string to filter the data. Default is None.
    :type query: str, optional
    :param marker_style: Style of the markers in the plot. Default is 'o'.
    :type marker_style: str, optional
    :param marker_size_factor: Factor to influence size of the markers in the plot. Default is 1000.0.
    :type marker_size_factor: float, optional
    :param zorder: Determines order of plotting when calling the function multilpe times. Default is None.
    :type zorder: float, optional
    
    :return: patches.
    :rtype: matplotlib.patches.Patch
    """
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

    try:
        if ax is None:
            fig, ax = plt.subplots(figsize=(11.7, 8.3))  # A3 size
            logger.debug("{0:s}{1:s}".format(logStr, 'Created new axis.'))

        if gdf is None or gdf.empty:
            logger.debug("{0:s}{1:s}".format(logStr, 'No plot data provided.'))
            return

        # Set default legend_fmt if not provided
        if legend_fmt is None:
            legend_fmt = attribute + ' {:4.0f}'

        # Create Colormap
        cmap = mcolors.LinearSegmentedColormap.from_list('cmap', colors, N=256)
        norm_min = norm_min if norm_min is not None else gdf[attribute].min()
        norm_max = norm_max if norm_max is not None else gdf[attribute].max()
        norm = plt.Normalize(vmin=norm_min, vmax=norm_max)
        logger.debug("{0:s}norm_min: {1:10.2f} norm_max: {2:10.2f}".format(logStr, norm_min, norm_max))

        # Filter and Sort Data if Query is Provided
        df = gdf.query(query) if query else gdf
        df = df.sort_values(by=[attribute], ascending=True)

        # Plotting Data with Markers
        sizes = norm(df[attribute].astype(float)) * marker_size_factor  # Scale sizes appropriately
        df.plot(ax=ax,
                marker=marker_style,
                markersize=sizes,
                linestyle='None',  # No lines, only markers
                color=cmap(norm(df[attribute].astype(float))),
                path_effects=[path_effects.Stroke(capstyle="round")],
                zorder=zorder)
        logger.debug("{0:s}{1:s}".format(logStr, f'Plotted {attribute} data.'))

        plt.axis('off')

        # Create Legend Patches
        legend_values = legend_values if legend_values is not None else np.linspace(norm_min, norm_max, num=5)
        logger.debug("{0:s}legend_values: {1}".format(logStr, legend_values))
        patches = [mpatches.Patch(color=cmap(norm(value)), label=legend_fmt.format(value)) for value in legend_values]

        return patches

    except Exception as e:
        logger.error("{0:s}{1:s} - {2}".format(logStr, 'Error.', str(e)))

    logger.debug("{0:s}{1:s}".format(logStr, 'End.'))
