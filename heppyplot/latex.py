import matplotlib as mpl
import matplotlib.pyplot as plt

def latexify():
    params = {'text.usetex': True}
    plt.rcParams.update(params)
    mpl.rcParams['text.latex.preamble'] = [
       r'\usepackage[T1]{fontenc}'
       r'\renewcommand*\familydefault{\sfdefault}'
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
       ]