import matplotlib as mpl
import matplotlib.pyplot as plt

def latexify(context):
    params = {'text.usetex': True}
    plt.rcParams.update(params)

    if context == 'talk':
        mpl.rcParams['text.latex.preamble'] = [
           r'\renewcommand*\familydefault{\sfdefault}',
           r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
           r'\sisetup{number-mode=text}',   # ...this to force siunitx to actually use your fonts
           r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
           r'\sansmath',               # <- tricky! -- gotta actually tell tex to use!
           ]
    else:
        mpl.rcParams['text.latex.preamble'] = [
           r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
           r'\sisetup{number-mode=text}',   # ...this to force siunitx to actually use your fonts
           ]
