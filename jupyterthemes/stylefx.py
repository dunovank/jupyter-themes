from __future__ import print_function
import os
from warnings import warn

# path to local site-packages/jupyterthemes
package_dir = os.path.dirname(os.path.realpath(__file__))
# theme colors and layout files (.less)
layouts_dir = os.path.join(package_dir, 'layout')
styles_dir = os.path.join(package_dir, 'styles')
# layout files for notebook, codemirror, and cells (.less)
nb_layout = os.path.join(layouts_dir, 'notebook.less')
cm_layout = os.path.join(layouts_dir, 'codemirror.less')
cl_layout = os.path.join(layouts_dir, 'cells.less')
mjax_css = os.path.join(layouts_dir, 'mathjax.css')
fonts_css = os.path.join(layouts_dir, 'fonts.css')


def toggle_toolbar(toolbar=False):
    """ Hides toolbar if toolbar==False (default)
    """
    toolbar_string = 'div#maintoolbar {display: none !important;}'
    if toolbar:
        toolbar_string = 'div#maintoolbar {margin-left: 8px !important;}'
    return toolbar_string

def style_layout(style_less, cellwidth=930, lineheight=160, altlayout=False, toolbar=False):
    """ set general layout and style properties of text and code cells
    """
    textcell_bg = '@cc-input-bg'
    if altlayout:
        # alt txt/md layout
        textcell_bg = '@notebook-bg'
    style_less += '@cell-width: {}px; \n'.format(cellwidth)
    style_less += '@cc-line-height: {}%; \n'.format(lineheight)
    style_less += '@text-cell-bg: {}; \n'.format(textcell_bg)
    # read-in notebook.less (general nb style)
    with open(nb_layout, 'r') as notebook:
        style_less += notebook.read() + '\n'
    # read-in cells.less (cell layous)
    with open(cl_layout, 'r') as cells:
        style_less += cells.read() + '\n'
    # read-in codemirror.less (syntax-highlighting)
    with open(cm_layout, 'r') as codemirror:
        style_less += codemirror.read() + '\n'
    style_less += toggle_toolbar(toolbar) +'\n'
    return style_less

def get_fonts(fontfamily='sans-serif'):
    if 'sans' in fontfamily:
        fontfamily = 'sans-serif'
    fonts_dict={'sans-serif': 'Droid Sans',
                'serif': 'PT Serif',
                'mono':{'roboto': ['Roboto Mono', True],
                        'space': ['Space Mono', True],
                        'anon': ['Anonymous Pro', True],
                        'cousine': ['Cousine' , True],
                        'ubuntu': ['Ubuntu Mono', True],
                        'source': ['Source Code Pro', False],
                        'oxygen': ['Oxygen Mono', False],
                        'droid': ['Droid Sans Mono', False],
                        'fira': ['Fira Mono', False],
                        'incon': ['Inconsolata', False]}}
    try:
        result = fonts_dict[fontfamily.lower()]
    except KeyError:
        warn("unknown font family: %s" % fontfamily)
        result = fontfamily

    return result

def import_monofont(style_css, fontname='Source Code Pro', ital=False):
    g_api = '@import url(https://fonts.googleapis.com/css?family={});'
    if ' ' in fontname:
        fontname = '+'.join(fontname.split(' '))
    if ital:
        fontname += ':400,400italic'
    with open(fonts_css, 'r') as fonts:
        style_css += fonts.read() + '\n'
    style_css += g_api.format(fontname) + '\n'
    return style_css

def set_nb_font(style_less, fontfam='sans'):
    fontsize=12.5
    if 'sans' in fontfam:
        fontfam = 'sans-serif'
        fontsize = 11.5
    nbfont = get_fonts(fontfamily=fontfam)
    style_less += '@notebook-fontfamily: "{}", {}; \n'.format(nbfont, fontfam)
    style_less += '@nb-fontsize: {}pt; \n'.format(fontsize+1.5)
    style_less += '@nb-fontsize-sub: {}pt; \n'.format(fontsize)
    return style_less

def set_txt_font(style_less, fontfam='sans'):
    fontsize=14
    if 'sans' in fontfam:
        fontfam = 'sans-serif'
        fontsize = 12.5
    tcfont = get_fonts(fontfamily=fontfam)
    style_less += '@text-cell-fontfamily: "{}", {}; \n'.format(tcfont, fontfam)
    style_less += '@text-cell-fontsize: {}pt; \n'.format(fontsize)
    return style_less

def set_monofont(style_less, monofont='Hack', monosize=11):
    # if triple digits, move decimal (105 --> 10.5)
    if len(str(monosize))>2:
        monosize = '.'.join([monosize[:-1], monosize[-1]])
    # define all fontvars and append to style_less
    style_less += '@monofont: "{}"; \n'.format(monofont)
    style_less += '@monofontsize: {}pt; \n'.format(monosize)
    return style_less

def set_mathjax(style_css):
    # append mathjax css & script to style_css
    with open(mjax_css, 'r') as mathjax:
        style_css += mathjax.read() + '\n'
    return style_css
