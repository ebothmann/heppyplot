import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, LogLocator

from .configuration import *
from .data import *
from .plot_dataframe import *
from .plot_helpers import *
from .seaborn_setup import *


def plot(config):

    font_scale = 1.1
    setup_seaborn_with_font_scale(font_scale, context=config['context'])

    # obtain data
    main_distributions, diff_distributions, distribution_settings, has_bands = dataframes_from_config(config)
    has_diff = False
    for diff_distribution in diff_distributions:
        if diff_distribution is not None:
            has_diff = True
            break
    distributions = [main_distributions]
    if has_diff:
        distributions.append(diff_distributions)

    # obtain fig and axes
    fig, axes = setup_axes(has_diff)
    main_axis = axes[0]
    try:
        diff_axis = axes[1]
    except IndexError:
        diff_axis = None

    # Add figure title
    title = read_configuration_value(config, key='title', default=None)
    if title is not None:
        fig.suptitle(title, fontsize=mpl.rcParams["axes.titlesize"])

    # prepare dataframe plotting
    legend_title = read_configuration_value(config, key='legend_title', default='')
    band_style = read_configuration_value(config, key='band_style', default=['ci_band'])
    legend_hidden = read_configuration_value(config, key='legend_hidden', default=False)
    linewidth = 1.0 if has_bands else 2.0
    alpha = 0.75 if has_bands else 1.0

    # plot dataframes
    for axis, distribution, legend in zip(axes, distributions, [not legend_hidden, False]):
        for dataframe, setting, color in zip(distribution, distribution_settings, sns.color_palette()):
            if dataframe is not None:
                plot_dataframe(dataframe,
                               axis=axis,
                               condition=legend_title,
                               band_style=band_style,
                               legend=legend,
                               color=color,
                               linewidth=linewidth,
                               err_estimator=setting['err_estimator'],
                               alpha=alpha)

    # plot guides
    horizontal_lines = read_configuration_subplot_values(config, key='horizontal_lines', defaults=[[],[]])
    for axis, subplot_horizontal_lines in zip(axes, horizontal_lines):
        for line in subplot_horizontal_lines:
            axis.plot([axis.get_xlim()[0], axis.get_xlim()[-1]],
                      [line]*2,
                      color="lightgray",
                      zorder=-1,
                      linewidth=linewidth)

    # set x and y scales and disable offsets for non-log y scales
    if read_configuration_value(config, key='x_log', default=False):
        for axis in axes:
            axis.set_xscale('log')
    y_log = read_configuration_subplot_values(config, key='y_log', defaults=[False, False])
    for axis, subplot_y_log in zip(axes, y_log):
        if subplot_y_log:
            axis.set_yscale('log')
        else:
            axis.get_yaxis().get_major_formatter().set_useOffset(False)

    # make axes adjacent
    if has_diff:
        layout_main_and_diff_axis(fig, axes)

    x_lim = read_configuration_value(config, key='x_lim', default=None)
    if x_lim is not None:
        x_lim_trim = read_configuration_value(config, key='x_lim_trim', default=None)
        if x_lim_trim is not None:
            x_title = read_configuration_value(config, key='x_title')
            if (x_lim_trim[0]):
                x_lim[0] = main_distributions[0].head(1)[x_title].iloc[0]
            if (x_lim_trim[1]):
                x_lim[1] = main_distributions[0].tail(1)[x_title].iloc[0]
        main_axis.set_xlim(x_lim)

    # adjust y range
    y_lim = read_configuration_subplot_values(config, key='y_lim', defaults=[None, None])
    for axis, subplot_y_lim in zip(axes, y_lim):
        if subplot_y_lim is not None:
            axis.set_ylim(subplot_y_lim)

    # reformat y major ticks
    prune = []
    if read_configuration_value(config, key='y_tick_prune_lower', default=False):
        prune.append('lower')
    else:
        prune.append(None)
    try:
      if read_configuration_value(config, key='y_tick_prune_upper', default=False, diff=True):
          prune.append('upper')
      else:
          prune.append(None)
    except KeyError:
      pass
    max_ticks = read_configuration_subplot_values(config, key='y_max_ticks', defaults=[None, None])
    for axis, subplot_prune, subplot_max_ticks, subplot_y_log in zip(axes, prune, max_ticks, y_log):
        if subplot_max_ticks is None:
            subplot_max_ticks = len(axis.get_yticklabels())
        if subplot_y_log:
            axis.yaxis.set_major_locator(LogLocator(numticks=subplot_max_ticks))
            ticks = get_major_ticks_within_view_interval(axis.yaxis)
            if subplot_prune == 'lower':
                ticks[0].label.set_visible(False)
            if subplot_prune == 'upper':
                ticks[-1].label.set_visible(False)
        else:
            axis.yaxis.set_major_locator(MaxNLocator(nbins=subplot_max_ticks-1, prune=subplot_prune))

    if has_diff:
        for axis in axes:
            axis.get_yaxis().set_label_coords(-0.13,0.5)

    # customize the default legend created by tsplot
    if not legend_hidden:
        loc = read_configuration_value(config, key='legend_loc', default='best')
        borderpad = read_configuration_value(config, key='legend_borderpad', default=1.2)
        configure_legend_on_axis(main_axis, title=legend_title, loc=loc, borderpad=borderpad)

    # add anchored annotation
    annotation = read_configuration_value(config, key='annotation', default=None)
    if annotation is not None:
        loc = read_configuration_value(config, key='annotation_loc', default='upper right')
        borderpad = read_configuration_value(config, key='annotation_borderpad', default=1.2)
        add_annotation_on_axis(main_axis, annotation, loc=loc, borderpad=borderpad)

    width = read_configuration_value(config, key='width', default=None)
    if width is not None:
        set_figure_size_with_width(width)
    if title is None:
        plt.subplots_adjust(top=0.95)
    if read_configuration_value(config, key='x_log', default=False) or config['context'] == 'paper':
        plt.subplots_adjust(bottom=0.13*font_scale)
    else:
        plt.subplots_adjust(bottom=0.1*font_scale)
