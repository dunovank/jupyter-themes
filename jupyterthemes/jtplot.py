
from __future__ import print_function
import os
import sys
import matplotlib as mpl
from cycler import cycler
from jupyter_core.paths import jupyter_config_dir

# path to install (~/.jupyter/custom/)
jupyter_custom = os.path.join(jupyter_config_dir(), 'custom')
# path to local site-packages/jupyterthemes
package_dir = os.path.dirname(os.path.realpath(__file__))
# theme colors, layout, and font directories
styles_dir = os.path.join(package_dir, 'styles')


def jtstyle(theme=True, style=None, grid=True):
    """
    theme'ify matplotlib plotting style
    ::Arguments::
        theme (bool): restores default rcParams if False
        style (str): theme name (will infer currently installed theme if None)
        grid (bool): removes axis grid lines if False
    """
    if not theme:
        styleMap, clist = get_default_params()
    else:
        styleMap, clist = get_theme_params(style)
    update_rc_params(styleMap, clist, grid)


def get_theme_params(style=None):
    """
    read-in theme style info and populate styleMap (dict of with mpl.rcParams)
    and clist (list of hex codes passed to color cylcler)
    """
    if style is None:
        theme_name_file = os.path.join(jupyter_custom, 'current_theme.txt')
        with open(theme_name_file) as f:
            style = f.readlines()[0]
    themeFile = os.path.join(styles_dir, style+'.less')
    styleMap = {'faceColor': '@cc-output-bg',
                'textColor': '@cc-output-fg',
                'edgeColor': '@table-border',
                'gridColor': '@df-header-border'}
    syntaxVars = ['cm-atom', '@cm-number', 'property', 'attribute', 'keyword', 'string', 'meta']
    get_hex_code = lambda line: line.split(':')[-1].split(';')[0][-7:]
    with open(themeFile) as f:
        for line in f:
            for k, v in styleMap.items():
                if v in line.strip():
                    styleMap[k] = get_hex_code(line)
            for c in syntaxVars:
                if c in line.strip():
                    syntaxVars[syntaxVars.index(c)] = get_hex_code(line)
    # remove duplicate hexcolors
    syntaxVars = list(set(syntaxVars))
    clist = get_color_list()
    clist.extend(syntaxVars)
    return styleMap, clist

def update_rc_params(styleMap={}, clist=[], grid=True):
    faceColor = styleMap['faceColor']
    textColor = styleMap['textColor']
    edgeColor = styleMap['edgeColor']
    gridColor = styleMap['gridColor']
    styleDict = {
        'axes.facecolor': faceColor,
        'figure.facecolor': faceColor,
        'text.color': textColor,
        'axes.labelcolor': textColor,
        'xtick.color': textColor,
        'ytick.color': textColor,
        'axes.edgecolor': edgeColor,
        'grid.color': gridColor,
        'axes.grid': grid,
        'axes.linewidth': 1.0,
        'font.family': u'sans-serif',
        'font.sans-serif': [u'Helvetica',
            u'Arial',
            u'Bitstream Vera Sans',
            u'sans-serif'],
        'figure.figsize': (5,4),
        'savefig.facecolor': 'white',
        'savefig.edgecolor': 'black',
        'grid.linestyle': u'-',
        'lines.solid_capstyle': u'round',
        'axes.axisbelow':True,
        'xtick.major.size': 0.0,
        'xtick.minor.size': 0.0,
        'ytick.major.size': 0.0,
        'ytick.minor.size': 0.0}
    mpl.rcParams.update(styleDict)
    mpl.rcParams['axes.prop_cycle'] = cycler(color=clist)

def get_color_list():
    return ['#3572C6',  '#c44e52', '#8172b2', '#83a83b', "#3498db", "#e5344a", '#94c273', '#6C7A89', "#8E44AD", "#16a085", "#f39c12", "#4168B7", '#34495e', "#27ae60", "#e74c3c", "#ff711a", "#ff914d"]


def get_default_params():
    styleMap = {'faceColor': 'white',
                'textColor': '.15',
                'edgeColor': '.8',
                'gridColor': '.8'}
    return styleMap, get_color_list()
