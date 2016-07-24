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
__version__ = '0.9.1'

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

# install I/O paths
jupyter_custom = os.path.join(jupyter_dir, 'custom')
css_fpath = os.path.join(jupyter_custom, 'custom.css')

# Ensure all install dirs exist
if not os.path.isdir(jupyter_dir):
    os.makedirs(jupyter_dir)
if not os.path.isdir(jupyter_custom):
    os.makedirs(jupyter_custom)

def compile_less2css(style_less):
    """ write less-compiled css file to css_fpath in jupyter_dir
    """
    # write all style_less to package_dir/temp_file.less
    temp_less = os.path.join(package_dir, 'temp_file.less')
    with open(temp_less, 'w') as f:
        f.write(style_less)
    os.chdir(package_dir)
    style_css = lesscpy.compile(less_tempfile, tabs=True)
    style_css += '\n\n'
    return style_css

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

def import_google_fonts(style_less, monofont='Hack', monofontsize=11, nbfontfamily='sans', tcfontfamily='sans'):
    style_css = ''
    g_api = '@import url(https://fonts.googleapis.com/css?family={});'
    fontfamily = {'sans': ['Droid Sans', 'sans-serif', 13, 10.7],
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
    nbf, nbff, nbfsize, nbfsizesub = fontfamily[nbfontfamily]
    tcf, tcff = fontfamily[tcfontfamily][:2]
    google_api_fonts = [nbf, tcf]
    monofonts = list(fontfamily['mono'])
    if not monofont in monofonts:
        if '-' in monofont:
            monofont = ' '.join(monofont.split('-'))
        monof = monofont
    else:
        monof, ital = fontfamily['mono'][monofont]
        google_api_fonts.append(monof)

    for fontname in google_api_fonts:
        is_mono = False
        if fontname in monofonts:
            is_mono = True
        googlefont = fontname
        if ' ' in googlefont:
            googlefont = '+'.join(googlefont.split(' '))
        if is_mono and ital:
            googlefont += ':400,400italic'
        style_css += g_api.format(googlefont) + '\n'

    # if >20, move decimal up (eg 105 --> 10.5)
    if int(monofontsize)>20:
        monofontsize = '.'.join([monofontsize[:-1], monofontsize[-1]])
    # convert monofontsize to float
    monofontsize = float(monofontsize)
    # define all fontvars and append to style_less
    style_less += '@monofont: "{}"; \n'.format(monof)
    style_less += '@monofontsize: {}pt; \n'.format(monofontsize)
    style_less += '@notebook-fontfamily: "{}", {}; \n'.format(nbf, nbff)
    style_less += '@nb-fontsize: {}pt; \n'.format(nbfsize)
    style_less += '@nb-fontsize-sub: {}pt; \n'.format(nbfsizesub)
    style_less += '@text-cell-fontfamily: "{}", {}; \n'.format(tcf, tcff)
    style_less += '@text-cell-fontsize: {}pt; \n'.format(nbfsizesub+1.2)
    return style_css, style_less

def toggle_toolbar(style_less, toolbar=False):
    """ Hides toolbar if toolbar==False (default)
    """
    toolbar_string = 'div#maintoolbar {display: none !important;}'
    if toolbar:
        print('Enabling Toolbar')
        toolbar_string = '/*' + toolbar_string + "*/"
    style_less += toolbar_string + '\n\n'
    return style_less

def style_cells(style_less, cellwidth=930, lineheight=160, altlayout=False):
    """ set general layout and style properties of text and code cells
    """
    textcell_bg = '@cc-input-bg'
    if altlayout:
        # alt txt/md layout
        textcell_bg = '@notebook-bg'
    style_less += '@cell-width: {}px; \n'.format(cellwidth)
    style_less += '@cc-line-height: {}%; \n'.format(lineheight)
    style_less += '@text-cell-bg: {}; \n'.format(textcell_bg)
    return style_less

def install_theme(theme, monofont='Hack', monofontsize=11, nbfontfamily='sans', tcfontfamily='serif', cellwidth=930, lineheight=160, altlayout=False, toolbar=False):
    """ install theme to css_fpath with specified font, fontsize,
    md layout, and toolbar pref
    """
    # initialize style_less & import main colors
    style_less = '@import "styles/{}";\n'.format(theme)
    # set font properties for code, txt/md cells, and notebook
    style_css, style_less = import_google_fonts(style_less, monofont=monofont, monofontsize=monofontsize, nbfontfamily=nbfontfamily, tcfontfamily=tcfontfamily)
    # define some vars for cell layout
    style_less = style_cells(style_less, cellwidth=cellwidth, lineheight=lineheight, altlayout=altlayout)
    # toggle on/off toolbar (hidden by default)
    style_less = toggle_toolbar(style_less, toolbar)

    # read-in notebook.less (general nb style)
    with open(nb_layout, 'r') as notebook:
        style_less += notebook.read() + '\n'
    # read-in cells.less (cell layous)
    with open(cl_layout, 'r') as cells:
        style_less += cells.read() + '\n'
    # read-in codemirror.less (syntax-highlighting)
    with open(cm_layout, 'r') as codemirror:
        style_less += codemirror.read() + '\n'
    # compile temp.less to css code and append to style_css
    style_css += compile_less2css(style_less)
    # append mathjax css & script to style_css
    with open(mjax_css, 'r') as mathjax:
        style_css += mathjax.read() + '\n'
    # install style_css to .jupyter/custom/custom.css
    with open(css_fpath, 'w') as f:
        f.write(style_css)
    # remove temp.less from package_dir
    os.remove(less_tempfile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', "--list", action='store_true', help="list available themes")
    parser.add_argument('-t', "--theme", action='store', help="name of the theme to install")
    parser.add_argument('-f',"--monofont", action='store', default='Hack', help='monospace code font')
    parser.add_argument('-fs', "--monofontsize", action='store', default=11, help='code font-size')
    parser.add_argument('-ff',"--nbfontfamily", action='store', default='sans', help='notebook font-family')
    parser.add_argument('-tcff',"--tcfontfamily", action='store', default='sans', help='text/md font-family')
    parser.add_argument('-cw', "--cellwidth", action='store', default=910, help="set cell width (in px)")
    parser.add_argument('-lh',"--lineheight", action='store', default=160, help='code/text line-height (in %)')
    parser.add_argument('-altmd', "--altlayout", action='store_true', default=False, help="alternative markdown layout")
    parser.add_argument('-T', "--toolbar", action='store_true', default=False, help="enable the toolbar")
    parser.add_argument('-r', "--reset", action='store_true', help="reset to default theme")
    args = parser.parse_args()
    feedback = "Available Themes: {}".format('\n\t'.join(get_themes()))
    if args.theme:
        themes = get_themes()
        if args.theme not in themes:
            print("Theme {0} not found\n{1}").format(args.theme, feedback)
            exit(1)
        print("Installing {0} at {1}".format(args.theme, css_fpath))
        install_theme(args.theme, monofont=args.monofont, monofontsize=args.monofontsize, nbfontfamily=args.nbfontfamily, tcfontfamily=args.tcfontfamily, cellwidth=int(args.cellwidth),  lineheight=int(args.lineheight), altlayout=args.altlayout, toolbar=args.toolbar)
    elif args.reset:
        reset_default()
    elif args.list:
        print(feedback)
    else:
        print('No theme provided, no changes made')
