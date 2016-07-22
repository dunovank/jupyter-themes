"""
Juypiter theme installer
Author: dunovank at github.com
"""
from __future__ import print_function
from jupyter_core import paths as jpaths
import os
import argparse
from glob import glob
import lesscpy
__version__ = '0.9.0'

# juypter config and package dir
package_dir = os.path.dirname(os.path.realpath(__file__))
jupyter_dir = jpaths.jupyter_config_dir()

# directories containing theme colors and layout files (.less)
layouts_dir = os.path.join(package_dir, 'layout')
styles_dir = os.path.join(package_dir, 'styles')
less_tempfile = os.path.join(package_dir, 'temp_file.less')

# layout files for notebook, codemirror, and cells (.less)
nb_layout = os.path.join(layouts_dir, 'notebook.less')
cm_layout = os.path.join(layouts_dir, 'codemirror.less')
cl_layout = os.path.join(layouts_dir, 'cells.less')
mjax_css = os.path.join(layouts_dir, 'mathjax.css')
fonts_css = os.path.join(layouts_dir, 'fonts.css')

# install I/O paths
jupyter_custom = os.path.join(jupyter_dir, 'custom')
jupyter_config = os.path.join(jupyter_dir, 'nbconfig')
css_fpath = os.path.join(jupyter_custom, 'custom.css')

# Ensure all install dirs exist
if not os.path.isdir(jupyter_dir):
    os.makedirs(jupyter_dir)
if not os.path.isdir(jupyter_custom):
    os.makedirs(jupyter_custom)
if not os.path.isdir(jupyter_config):
    os.makedirs(jupyter_config)

def get_themes():
    """ return list of available themes """
    themes = [os.path.basename(theme).replace('.less', '')
              for theme in glob('{0}/*.less'.format(styles_dir))]
    return themes

def set_nb_theme(theme):
    """ set theme from within notebook """
    from IPython.core.display import HTML
    install_theme(theme)
    # css_path = glob('{0}/{1}.css'.format(css, name))[0]
    customcss = open(css_fpath, "r").read()
    return HTML(''.join(['<style> ', customcss, ' </style>']))

def reset_default():
    """ remove custom.css import"""
    from jupyter_core.paths import jupyter_data_dir
    jnb_cached = os.path.join(jupyter_data_dir(), 'nbextensions')
    paths = [jupyter_custom, jnb_cached]
    for fpath in paths:
        custom = '{0}/{1}.css'.format(fpath, 'custom')
        try:
            os.remove(custom)
            print("Reset default theme in: {0}".format(fpath))
        except Exception:
            print("Already set to default theme in {0}".format(fpath))

def write_to_css():
    """ write less-compiled css file to css_fpath in jupyter_dir
    """
    os.chdir(package_dir)
    csscontent = lesscpy.compile(less_tempfile, tabs=True)
    csscontent += '\n\n'
    return csscontent

def make_tempfile(stylecontent):
    """ write less file with import @<theme>.less statement
    to package dir"""
    with open(less_tempfile, 'w') as f:
        f.write(stylecontent)

def import_google_fonts(stylecontent, monofont='Hack', monofontsize=11, nbfontfamily='sans', tcfontfamily='sans'):
    csscontent = ''
    g_api = 'https://fonts.googleapis.com/css?family={}'
    url = '@import url({});'
    typeface = {'sans': ['Droid Sans', 'sans-serif', 13, 10.7],
                'serif': [ 'PT Serif', 'serif', 13, 12],
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
    nbf, nbff, nbfsize, nbfsizesub = typeface[nbfontfamily]
    tcf, tcff = typeface[tcfontfamily][:2]
    google_api_fonts = [nbf, tcf]
    monofonts = list(typeface['mono'])
    if not monofont in monofonts:
        if '-' in monofont:
            monofont = ' '.join(monofont.split('-'))
        monof = monofont
    else:
        monof, ital = typeface['mono'][monofont]
        google_api_fonts.append(monof)
    # define monofont // monofontsize vars
    stylecontent += '@monofont: "{}"; \n'.format(monof)
    stylecontent += '@monofontsize: {}pt; \n'.format(monofontsize)
    stylecontent += '@notebook-fontfamily: "{}", {}; \n'.format(nbf, nbff)
    stylecontent += '@nb-fontsize: {}pt; \n'.format(nbfsize)
    stylecontent += '@nb-fontsize-sub: {}pt; \n'.format(nbfsizesub)
    stylecontent += '@text-cell-fontfamily: "{}", {}; \n'.format(tcf, tcff)
    stylecontent += '@text-cell-fontsize: {}pt; \n'.format(nbfsizesub+1.2)
    for fontname in google_api_fonts:
        is_mono = False
        if fontname in monofonts:
            is_mono = True
        googlefont = fontname
        if ' ' in googlefont:
            googlefont = '+'.join(googlefont.split(' '))
        if is_mono and ital:
            googlefont += ':400,400italic'
        csscontent += url.format(g_api.format(googlefont))+'\n'

    return csscontent, stylecontent


def toggle_toolbar(stylecontent, toolbar=False):
    """ Hides toolbar if toolbar==False (default)
    """
    toolbar_string = 'div#maintoolbar {display: none !important;}'
    if toolbar:
        print('Enabling Toolbar')
        toolbar_string = '/*' + toolbar_string + "*/"
    stylecontent += toolbar_string + '\n\n'
    return stylecontent

def style_cells(stylecontent, cellwidth=930, lineheight=160, altlayout=False):
    """ set general layout and style properties of text and code cells
    """
    textcell_bg = '@cc-input-bg'
    if altlayout:
        # alt txt/md layout
        textcell_bg = '@notebook-bg'
    stylecontent += '@cell-width: {}px; \n'.format(cellwidth)
    stylecontent += '@cc-line-height: {}%; \n'.format(lineheight)
    stylecontent += '@text-cell-bg: {}; \n'.format(textcell_bg)
    return stylecontent


def install_theme(theme, font='Hack', fontsize=11, nbfontfamily='sans', tcfontfamily='serif', cellwidth=930, lineheight=160, altlayout=False, toolbar=False):
    """ install theme to css_fpath with specified font, fontsize,
    md layout, and toolbar pref
    """
    # initialize stylecontent & import main colors
    stylecontent = '@import "styles/{}";\n'.format(theme)

    # convert fontsize to float, (& if 105 --> 10.5)
    if int(fontsize)>50 and len(fontsize)>1:
        fontsize= float('.'.join([fontsize[:-1], fontsize[-1]]))
    csscontent, stylecontent = import_google_fonts(stylecontent, monofont=font, monofontsize=fontsize, nbfontfamily=nbfontfamily, tcfontfamily=tcfontfamily)

    # define some vars for cell layout
    stylecontent = style_cells(stylecontent, cellwidth=cellwidth, lineheight=lineheight, altlayout=altlayout)
    # toggle on/off toolbar (hidden by default)
    stylecontent = toggle_toolbar(stylecontent, toolbar)

    # read-in notebook.less (general nb style)
    with open(nb_layout, 'r') as notebook:
        stylecontent += notebook.read() + '\n'
    # read-in cells.less (cell layous)
    with open(cl_layout, 'r') as cells:
        stylecontent += cells.read() + '\n'
    # read-in codemirror.less (syntax-highlighting)
    with open(cm_layout, 'r') as codemirror:
        stylecontent += codemirror.read() + '\n'

    # write all stylecontent to package_dir/temp.less
    make_tempfile(stylecontent)
    # compile temp.less to css code and add to csscontent
    csscontent += write_to_css()

    # append mathjax css & script to csscontent
    with open(mjax_css, 'r') as mathjax:
        csscontent += mathjax.read() + '\n'
    # install csscontent to .jupyter/custom/custom.css
    with open(css_fpath, 'w') as f:
        f.write(csscontent)

    # remove temp.less from package_dir
    os.remove(less_tempfile)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', "--theme", action='store', help="name of the theme to install")
    parser.add_argument('-altmd', "--altlayout", action='store_true', default=False, help="alternative markdown layout")
    parser.add_argument('-cw', "--cellwidth", action='store', default=910, help="set cell width in pixels")
    parser.add_argument('-l', "--list", action='store_true', help="list available themes")
    parser.add_argument('-r', "--reset", action='store_true', help="reset to default theme")
    parser.add_argument('-T', "--toolbar", action='store_true', default=False, help="enable the toolbar")
    parser.add_argument('-fs', "--fontsize", action='store', default=11, help='set the CodeCell font-size')
    parser.add_argument('-f',"--font", action='store', default='Hack', help='CodeCell font')
    parser.add_argument('-lh',"--lineheight", action='store', default=160, help='Code/TextCell line-height %')
    parser.add_argument('-ff',"--nbfontfamily", action='store', default='sans', help='Notebook font-family (sans/serif)')
    parser.add_argument('-tcff',"--tcfontfamily", action='store', default='sans', help='TextCell font-family (sans/serif)')
    args = parser.parse_args()
    if args.reset:
        reset_default()
        exit(0)
    if args.list:
        themes = get_themes()
        print("Available Themes")
        print('\n'.join(themes))
        exit(0)
    if args.theme:
        themes = get_themes()
        if args.theme not in themes:
            print("Theme {0} not found. Available: {1}".format(args.theme, ' '.join(themes)))
            exit(1)
        # print feedback
        print("Installing {0} at {1}".format(args.theme, css_fpath))
        install_theme(args.theme, font=args.font, fontsize=args.fontsize, nbfontfamily=args.nbfontfamily, tcfontfamily=args.tcfontfamily, cellwidth=int(args.cellwidth),  lineheight=int(args.lineheight), altlayout=args.altlayout, toolbar=args.toolbar)
        exit(0)
