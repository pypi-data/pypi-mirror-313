from .units import *
import matplotlib

def set_figsize(width_pt, height_pt):
    width_in = convert_units('pt', 'in', width_pt)
    height_in = convert_units('pt', 'in', height_pt)
    matplotlib.rcParams.update({
        'figure.figsize': (width_in, height_in)
    })


def set_font(fontsize=10):
    matplotlib.rcParams.update({
        'legend.title_fontsize': fontsize,
        'font.size': fontsize,  # controls default text sizes
        'axes.titlesize': fontsize,  # fontsize of the axes title
        'axes.labelsize': fontsize,  # fontsize of the x and y labels
        'xtick.labelsize': fontsize,  # fontsize of the tick labels
        'ytick.labelsize': fontsize,  # fontsize of the tick labels
        'legend.fontsize': fontsize,  # legend fontsize
        'figure.titlesize': fontsize,  # fontsize of the figure title
    })

original_backend = None

def enable_latex(latex_mode=True, preamble = r'''
            \usepackage[utf8]{inputenc}
            \usepackage[russian]{babel}
            \usepackage{amsmath}
            \usepackage{amssymb}
            \usepackage{xfrac}
            \usepackage{siunitx}
            \usepackage{physics}
        '''):
    
    global original_backend

    if original_backend == None:
        original_backend = matplotlib.get_backend()

    if latex_mode == True:
        matplotlib.rcParams.update({
        'pgf.rcfonts': False,
        'text.usetex': True,
        'text.latex.preamble': preamble })
        matplotlib.use('pgf')
        print("Switched to PGF backend.")
        
    elif latex_mode == False:
        matplotlib.rcParams.update({
        'pgf.rcfonts': False,
        'text.usetex': False,
        'text.latex.preamble': "" })
        matplotlib.use(original_backend)
        print(f"Switched to original backend ({original_backend}).")
    
    matplotlib.pyplot.figure()