import seaborn as sns

def setup_seaborn_with_font_scale(font_scale):
    sns.set_context('notebook', font_scale)  # Contexts are paper, notebook, talk and poster
    sns.set_style('ticks')  # Styles are darkgrid, whitegrid, dark, white, ticks

    sns.set_palette('muted')
    palette = sns.color_palette()
    red = palette[2]
    palette[2] = palette[1]
    palette[1] = red
    sns.set_palette(palette)
