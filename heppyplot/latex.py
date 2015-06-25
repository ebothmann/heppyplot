import matplotlib as mpl
import matplotlib.pyplot as plt

def latexify(context):
    plt.rc('text', usetex=True)

    if context == 'talk':
        mpl.rcParams['text.latex.preamble'] = [
           r'\renewcommand*\familydefault{\sfdefault}',
           r'\usepackage{siunitx}',   # you'll need...
           r'\sisetup{number-mode=text}',   # ...this to force siunitx to actually use your fonts
           r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
           r'\sansmath',               # <- tricky! -- gotta actually tell tex to use!
           ]
    else:
        mpl.rcParams['text.latex.preamble'] = [
           r'\usepackage{siunitx}'
           ]
