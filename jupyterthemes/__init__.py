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
__version__ = '0.8.0'

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

def write_to_css():
    """ write less-compiled css file to css_fpath in jupyter_dir"""
    os.chdir(package_dir)
    css_content = lesscpy.compile(less_tempfile)
    css_content += '\n\n'
    return css_content

def make_tempfile(stylecontent):
    """ write less file with import @<theme>.less statement
    to package dir"""
    with open(less_tempfile, 'w') as f:
        f.write(stylecontent)

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

def set_nb_font(stylecontent, nbfontfamily='sans', tcfontfamily='serif'):
    """ set text and markdown cell font and font-family
    """
    # Notebook FontFamily
    if nbfontfamily == 'sans':
        nbfont = 'Droid Sans'
        nbfontfamily='sans-serif'
        nbfontsize = '12pt'
        nbfontsize_sub = '11pt'
    elif nbfontfamily == 'serif':
        nbfont = 'Crimson Text'
        nbfontsize = '13.5pt'
        nbfontsize_sub = '12pt'
    # Text Cell FontFamily
    if tcfontfamily == 'sans':
        tcfont = 'Droid Sans'
        tcfontfamily='sans-serif'
        tcfontsize = '11.5pt'
    elif tcfontfamily == 'serif':
        tcfont = 'Crimson Text'
        tcfontsize = '14pt'
    stylecontent += '@notebook-fontfamily: "{}", {}; \n'.format(nbfont, nbfontfamily)
    stylecontent += '@nb-fontsize: {}; \n'.format(nbfontsize)
    stylecontent += '@nb-fontsize-sub: {}; \n'.format(nbfontsize_sub)
    stylecontent += '@text-cell-fontfamily: "{}", {}; \n'.format(tcfont, tcfontfamily)
    stylecontent += '@text-cell-fontsize: {}; \n'.format(tcfontsize)
    return stylecontent

def set_mono_font(stylecontent, font='Hack', fontsize=11):
    # convert fontsize to float, (& if 105 --> 10.5)
    if int(fontsize)>50 and len(fontsize)>1:
        fontsize= float('.'.join([fontsize[:-1], fontsize[-1]]))
    # define monofont // monofontsize vars
    stylecontent += '@monofont: "{}"; \n'.format(font)
    stylecontent += '@monofontsize: {}pt; \n'.format(fontsize)
    return stylecontent

def toggle_toolbar(stylecontent, toolbar=False):
    """ Hides toolbar if toolbar==False (default)
    """
    toolbar_string = 'div#maintoolbar {display: none !important;}'
    if toolbar:
        print('Enabling Toolbar')
        toolbar_string = '/*' + toolbar_string + "*/"
    stylecontent += toolbar_string + '\n\n'
    return stylecontent

def style_cells(stylecontent, cellwidth=950, altmd=False):
    """ set general layout and style properties of text and code cells
    """
    textcell_bg = '@cc-input-bg'
    if altmd:
        # alt txt/md layout
        textcell_bg = '@notebook-bg'
    stylecontent += '@cell-width: {}px; \n'.format(cellwidth)
    stylecontent += '@text-cell-bg: {}; \n'.format(textcell_bg)
    return stylecontent

def install_theme(theme, font='Hack', fontsize=11, cellwidth=950, altmd=False, nbfontfamily='sans', tcfontfamily='serif', toolbar=False):
    """ install theme to css_fpath with specified font, fontsize,
    md layout, and toolbar pref
    """
    # initialize css_content as empty str
    # merged with style_content at the end
    css_content = ''
    # import fonts from googleapis
    with open(fonts_css, 'r') as fonts:
        css_content += fonts.read() + '\n'

    # initialize stylecontent & import main colors
    stylecontent = '@import "styles/{}";\n'.format(theme)
    # set codecell monofont & fontsize
    stylecontent = set_mono_font(stylecontent, font, fontsize)
    # set notebook serif &/or sans-serif font choices
    stylecontent = set_nb_font(stylecontent, nbfontfamily, tcfontfamily)
    # define some vars for cell layout
    stylecontent = style_cells(stylecontent, cellwidth, altmd)
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
    # compile temp.less to css code and add to css_content
    css_content += write_to_css()
    # append mathjax css & script to css_content
    with open(mjax_css, 'r') as mathjax:
        css_content += mathjax.read() + '\n'
    # install css_content to .jupyter/custom/custom.css
    with open(css_fpath, 'w') as f:
        f.write(css_content)
    # remove temp.less from package_dir
    os.remove(less_tempfile)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', "--theme", action='store', help="name of the theme to install")
    parser.add_argument('-altmd', "--altmd", action='store_true', default=False, help="alternative markdown layout")
    parser.add_argument('-cw', "--cellwidth", action='store', default=950, help="set cell width in pixels")
    parser.add_argument('-l', "--list", action='store_true', help="list available themes")
    parser.add_argument('-r', "--reset", action='store_true', help="reset to default theme")
    parser.add_argument('-T', "--toolbar", action='store_true', default=False, help="enable the toolbar")
    parser.add_argument('-fs', "--fontsize", action='store', default=11, help='set the CodeCell font-size')
    parser.add_argument('-f',"--font", action='store', default='Hack', help='CodeCell font')
    parser.add_argument('-ff',"--nbfontfamily", action='store', default='sans', help='Notebook font-family (sans or serif)')
    parser.add_argument('-tcff',"--tcfontfamily", action='store', default='sans', help='TextCell font-family (sans or serif)')
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
        install_theme(args.theme, font=args.font, fontsize=args.fontsize,  nbfontfamily=args.nbfontfamily, cellwidth=int(args.cellwidth), altmd=args.altmd, toolbar=args.toolbar, tcfontfamily=args.tcfontfamily)
        exit(0)
