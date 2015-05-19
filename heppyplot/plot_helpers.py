import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText

def setup_axes(diff=False):
    fig = plt.figure()
    axes = []
    if diff:
        gs = gridspec.GridSpec(2, 1, height_ratios=[2,1])
        main_axis = plt.subplot(gs[0])
        axes.append(plt.subplot(gs[0]))
        axes.append(plt.subplot(gs[1], sharex=main_axis))
    else:
        axes.append(plt.subplot())
    return fig, axes

def layout_main_and_diff_axis(fig, axes):
    main_axis, diff_axis = axes
    fig.subplots_adjust(hspace=0.0)
    main_axis.spines['bottom'].set_visible(False)
    plt.setp(main_axis.get_xticklabels(), visible=False)
    main_axis.set_xlabel('')
    diff_axis.xaxis.tick_bottom()

def configure_legend_on_axis(axis, title='', loc='best', borderpad=1.2):
    legend = axis.legend(loc=loc,
                         title=title,
                         borderaxespad=borderpad,
                         framealpha=0.8,
                         frameon=True,
                         fancybox=True)
    legend.get_frame().set_color((0.96,0.96,0.96))
    for line in legend.get_lines():
        line.set_alpha(1.0)

def add_annotation_on_axis(axis, annotation, loc='upper right', borderpad=1.2):
    codes = {'upper right': 1, 'upper left': 2, 'lower left': 3, 'lower right': 4,
             'right': 5, 'center left': 6,'center right': 7,
             'lower center': 8, 'upper center': 9, 'center': 10}
    at = AnchoredText(annotation,
                      codes[loc],
                      frameon=False,
                      borderpad=borderpad,
                      prop=dict(linespacing=2.5))
    axis.add_artist(at)
