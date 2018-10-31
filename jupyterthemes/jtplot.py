import os
import sys
import re
from glob import glob
import matplotlib as mpl
from jupyter_core.paths import jupyter_config_dir

# path to install (~/.jupyter/custom/)
jupyter_custom = os.path.join(jupyter_config_dir(), 'custom')
# path to local site-packages/jupyterthemes
package_dir = os.path.dirname(os.path.realpath(__file__))
# theme colors, layout, and font directories
styles_dir = os.path.join(package_dir, 'styles')
# text file containing name of currently installed theme
theme_name_file = os.path.join(jupyter_custom, 'current_theme.txt')


# base style params
base_style = {
    'axes.axisbelow': True,
    'figure.autolayout': True,
    'grid.linestyle': u'-',
    'lines.solid_capstyle': u'round',
    'legend.frameon': False,
    "legend.numpoints": 1,
    "legend.scatterpoints": 1}

# base context params
base_context = {
    'axes.linewidth': 1.4,
    "grid.linewidth": 1.4,
    "lines.linewidth": 1.5,
    "patch.linewidth": .2,
    "lines.markersize": 7,
    "lines.markeredgewidth": 0,
    "xtick.major.width": 1,
    "ytick.major.width": 1,
    "xtick.minor.width": .5,
    "ytick.minor.width": .5,
    "xtick.major.pad": 7,
    "ytick.major.pad": 7,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "xtick.minor.size": 0,
    "ytick.minor.size": 0}

# base font params
base_font = {
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "xtick.labelsize": 10.5,
    "ytick.labelsize": 10.5,
    "legend.fontsize": 10.5}


def remove_non_colors(clist):
    checkHex = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
    return [clr for clr in clist if re.search(checkHex, clr)]


def infer_theme():
    """ checks jupyter_config_dir() for text file containing theme name
    (updated whenever user installs a new theme)
    """
    themes = [os.path.basename(theme).replace('.less', '')
                  for theme in glob('{0}/*.less'.format(styles_dir))]
    if os.path.exists(theme_name_file):
        with open(theme_name_file) as f:
            theme = f.readlines()[0]
        if theme not in themes:
            theme = 'default'
    else:
        theme = 'default'

    return theme


def style(theme=None, context='paper', grid=True, gridlines=u'-', ticks=False, spines=True, fscale=1.2, figsize=(8., 7.)):
    """
    main function for styling matplotlib according to theme

    ::Arguments::
        theme (str): 'oceans16', 'grade3', 'chesterish', 'onedork', 'monokai', 'solarizedl', 'solarizedd'. If no theme name supplied the currently installed notebook theme will be used.

        context (str): 'paper' (Default), 'notebook', 'talk', or 'poster'

        grid (bool): removes axis grid lines if False

        gridlines (str): set grid linestyle (e.g., '--' for dashed grid)

        ticks (bool): make major x and y ticks visible

        spines (bool): removes x (bottom) and y (left) axis spines if False

        fscale (float): scale font size for axes labels, legend, etc.

        figsize (tuple): default figure size of matplotlib figures
    """

    # set context and font rc parameters, return rcdict
    rcdict = set_context(context=context, fscale=fscale, figsize=figsize)

    # read in theme name from ~/.jupyter/custom/current_theme.txt
    if theme is None:
        theme = infer_theme()

    # combine context & font rcparams with theme style
    set_style(rcdict, theme=theme, grid=grid, gridlines=gridlines, ticks=ticks, spines=spines)



def set_style(rcdict, theme=None, grid=True, gridlines=u'-', ticks=False, spines=True):
    """
    This code has been modified from seaborn.rcmod.set_style()
    ::Arguments::
        rcdict (str): dict of "context" properties (filled by set_context())
        theme (str): name of theme to use when setting color properties
        grid (bool): turns off axis grid if False (default: True)
        ticks (bool): removes x,y axis ticks if True (default: False)
        spines (bool): removes axis spines if False (default: True)
    """

    # extract style and color info for theme
    styleMap, clist = get_theme_style(theme)

    # extract style variables
    figureFace = styleMap['figureFace']
    axisFace = styleMap['axisFace']
    textColor = styleMap['textColor']
    edgeColor = styleMap['edgeColor']
    gridColor = styleMap['gridColor']

    if not spines:
        edgeColor = 'none'

    style_dict = {
        'figure.edgecolor': figureFace,
        'figure.facecolor': figureFace,
        'axes.facecolor': axisFace,
        'axes.edgecolor': edgeColor,
        'axes.labelcolor': textColor,
        'axes.grid': grid,
        'grid.linestyle': gridlines,
        'grid.color': gridColor,
        'text.color': textColor,
        'xtick.color': textColor,
        'ytick.color': textColor,
        'patch.edgecolor': axisFace,
        'patch.facecolor': gridColor,
        'savefig.facecolor': figureFace,
        'savefig.edgecolor': figureFace}

    # update rcdict with style params
    rcdict.update(style_dict)

    # Show or hide the axes ticks
    if ticks:
        rcdict.update({
            "xtick.major.size": 6,
            "ytick.major.size": 6,
            "xtick.minor.size": 3,
            "ytick.minor.size": 3})

    base_style.update(rcdict)

    # update matplotlib with rcdict (incl. context, font, & style)
    mpl.rcParams.update(rcdict)

    # update seaborn with rcdict (incl. context, font, & style)
    try:
        import seaborn as sns
        sns.set_style(rc=rcdict)
    except Exception:
        pass

    try:
        from cycler import cycler
        # set color cycle to jt-style color list
        mpl.rcParams['axes.prop_cycle'] = cycler(color=clist)
    except Exception:
        pass

    # replace default blue, green, etc. with jt colors
    for code, color in zip("bgrmyck", clist[:7]):
        rgb = mpl.colors.colorConverter.to_rgb(color)
        mpl.colors.colorConverter.colors[code] = rgb
        mpl.colors.colorConverter.cache[code] = rgb


def set_context(context='paper', fscale=1., figsize=(8., 7.)):
    """
    Most of this code has been copied/modified from seaborn.rcmod.plotting_context()
    ::Arguments::
        context (str): 'paper', 'notebook', 'talk', or 'poster'
        fscale (float): font-size scalar applied to axes ticks, legend, labels, etc.
    """
    # scale all the parameters by the same factor depending on the context
    scaling = dict(paper=.8, notebook=1, talk=1.3, poster=1.6)[context]
    context_dict = {k: v * scaling for k, v in base_context.items()}

    # scale default figsize
    figX, figY = figsize
    context_dict["figure.figsize"] = (figX*scaling, figY*scaling)

    # independently scale the fonts
    font_dict = {k: v * fscale for k, v in base_font.items()}
    font_dict["font.family"] = ["sans-serif"]
    font_dict["font.sans-serif"] = ["Helvetica", "Helvetica Neue", "Arial",
                                "DejaVu Sans", "Liberation Sans", "sans-serif"]
    context_dict.update(font_dict)
    return context_dict


def figsize(x=8, y=7., aspect=1.):
    """ manually set the default figure size of plots
    ::Arguments::
        x (float): x-axis size
        y (float): y-axis size
        aspect (float): aspect ratio scalar
    """
    # update rcparams with adjusted figsize params
    mpl.rcParams.update({'figure.figsize': (x*aspect, y)})


def get_theme_style(theme):
    """
    read-in theme style info and populate styleMap (dict of with mpl.rcParams)
    and clist (list of hex codes passed to color cylcler)
    ::Arguments::
        theme (str): theme name
    ::Returns::
        styleMap (dict): dict containing theme-specific colors for figure properties
        clist (list): list of colors to replace mpl's default color_cycle
    """
    styleMap, clist = get_default_jtstyle()
    if theme == 'default':
        return styleMap, clist

    syntaxVars = ['@yellow:', '@orange:', '@red:', '@magenta:', '@violet:', '@blue:', '@cyan:', '@green:']

    get_hex_code = lambda line: line.split(':')[-1].split(';')[0][-7:]

    themeFile = os.path.join(styles_dir, theme+'.less')
    with open(themeFile) as f:
        for line in f:
            for k, v  in styleMap.items():
                if k in line.strip():
                    styleMap[k] = get_hex_code(line)
            for c in syntaxVars:
                if c in line.strip():
                    syntaxVars[syntaxVars.index(c)] = get_hex_code(line)

    # remove duplicate hexcolors
    syntaxVars = list(set(syntaxVars))
    clist.extend(syntaxVars)
    clist = remove_non_colors(clist)
    return styleMap, clist


def get_default_jtstyle():
    styleMap = {'axisFace': 'white',
                'figureFace': 'white',
                'textColor': '.15',
                'edgeColor': '.8',
                'gridColor': '.8'}
    return styleMap, get_color_list()


def get_color_list():
    return ['#3572C6', '#83a83b', '#c44e52', '#8172b2', "#ff914d",
    "#77BEDB", "#222222", "#4168B7", "#27ae60", "#e74c3c",'#bc89e0',
    "#ff711a", "#3498db", '#6C7A89']


def reset():
    """ full reset of matplotlib default style and colors
    """
    colors = [(0., 0., 1.), (0., .5, 0.), (1., 0., 0.), (.75, .75, 0.),
            (.75, .75, 0.), (0., .75, .75), (0., 0., 0.)]
    for code, color in zip("bgrmyck", colors):
        rgb = mpl.colors.colorConverter.to_rgb(color)
        mpl.colors.colorConverter.colors[code] = rgb
        mpl.colors.colorConverter.cache[code] = rgb
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['figure.facecolor'] = 'white'
    mpl.rcParams['axes.facecolor'] = 'white'
