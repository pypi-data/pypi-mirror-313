from .units import *
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def rcparams_initial_update():

    textwidth = 247.53899  # pt
    ratio = 4/3
    textwidth = convert_units('pt', 'in', textwidth)
    fontsize = 10
    plt.style.use('classic')


    matplotlib.rcParams.update({
        # Font settings
        'font.family': 'serif',        # Serif font family DejaVu Serif
        'font.size': fontsize,         # Default font size
        'axes.titlesize': fontsize,    # Font size for axis titles
        'axes.labelsize': fontsize,    # Font size for axis labels
        'xtick.labelsize': fontsize,   # Font size for X-axis tick labels
        'ytick.labelsize': fontsize,   # Font size for Y-axis tick labels
        'legend.fontsize': fontsize,   # Font size for legend
        'figure.titlesize': fontsize,  # Font size for figure title

        # Figure and axis settings
        'figure.figsize': (textwidth, textwidth / ratio),  # Figure size (in inches)
        'figure.dpi': 144,             # Figure resolution
        'figure.facecolor': "white",   # Figure background color

        # Grid and lines
        'axes.grid': True,             # Enable grid
        'axes.grid.which': "both",     # Show both major and minor grid lines
        'grid.linestyle': "-",         # Grid line style (solid)
        'grid.linewidth': 0.3,         # Grid line width
        'grid.color': "#000000",       # Grid line color (black)
        'grid.alpha': 0.2,             # Grid line transparency

        # Axis settings
        'axes.titlepad': 4.0,          # Padding for axis title
        'axes.labelpad': 2.0,          # Padding for axis labels
        'axes.axisbelow': False,       # Grid lines below the plot
        'axes.xmargin': .05,           # X-axis margin
        'axes.ymargin': .05,           # Y-axis margin
        'axes.zmargin': .05,           # Z-axis margin
        'axes.autolimit_mode': "data", # Auto-limiting mode for axes
        'axes.linewidth': 0.5,         # Axis line width

        # Legend settings
        'legend.title_fontsize': fontsize,  # Font size for legend title
        'legend.numpoints': 1,              # Number of points in the legend
        'legend.fancybox': False,           # Disable rounded corners in the legend
        'legend.borderpad': 0.4,            # Padding inside the legend border
        'legend.framealpha': 0.0,           # Legend background transparency

        # Line and marker settings
        'lines.linewidth': 0.5,          # Line width for plots
        'lines.markersize': 3,           # Marker size
        'errorbar.capsize': 1,           # Cap size for error bars

        # Boxplot settings
        'boxplot.boxprops.linewidth': 0.5,        # Line width for box
        'boxplot.whiskerprops.linewidth': 0.5,    # Line width for whiskers
        'boxplot.capprops.linewidth': 0.5,         # Line width for caps
        'boxplot.medianprops.linewidth': 0.5,      # Line width for median
        'boxplot.meanprops.linewidth': 0.5,        # Line width for mean

        # Additional settings
        'axes.titlepad': 4.0,            # Additional padding for axis titles
        'axes.labelpad': 2.0             # Additional padding for axis labels
    })






        # # Experimental
        # 'text.latex.preamble': r'''
        #     \usepackage[utf8]{inputenc}
        #     \usepackage[russian]{babel}
        #     \usepackage{amsmath}
        #     \usepackage{amssymb}
        #     \usepackage{xfrac}
        #     \usepackage{siunitx}
        #     \usepackage{physics}
        # '''






            # \usepackage{amsmath}  % Математические пакеты
            # \usepackage{amssymb}  % Символы
            # \usepackage{bm}  % Жирный шрифт для математики
            # \usepackage{xfrac}  % Поддержка дробей
            # \usepackage{mathrsfs}  % Для красивых математических шрифтов
            # \usepackage{siunitx}  % Для работы с единицами
            # \usepackage{physics}  % Для физических выражений




        # font_path = os.path.join(os.path.dirname(__file__), 'fonts')

        # font_files = [
        #     'cmunrm.ttf',  # обычный
        #     'cmunbi.ttf',  # полужирный курсив
        #     'cmunbx.ttf',  # жирный
        #     'cmunsl.ttf',  # курсив
        #     'cmunti.ttf',  # тонкий курсив
        #     'cmunui.ttf',  # ультра курсивный
        # ]

        # # Добавляем шрифты в matplotlib с использованием метода addfont
        # for font_file in font_files:
        #     font = fm.FontProperties(fname=os.path.join(font_path, font_file))
        #     fm.fontManager.addfont(os.path.join(font_path, font_file))  # Метод addfont добавляет шрифт




        #     # Font settings
        # 'font.family' : 'CMU Serif',   # Установка шрифта по умолчанию
        # 'font.weight' : 'normal',      # Указание начертания
        # 'font.style' : 'normal',       # Указание стиля
        # 'font.size': fontsize,         # Default font size
        # 'axes.titlesize': fontsize,    # Font size for axis titles
        # 'axes.labelsize': fontsize,    # Font size for axis labels
        # 'xtick.labelsize': fontsize,   # Font size for X-axis tick labels
        # 'ytick.labelsize': fontsize,   # Font size for Y-axis tick labels
        # 'legend.fontsize': fontsize,   # Font size for legend
        # 'figure.titlesize': fontsize,  # Font size for figure title