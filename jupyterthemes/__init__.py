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
__version__ = '0.7.2'

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

def set_font_family(stylecontent, nbfontfamily='sans', tcfontfamily='serif'):
    """ set text and markdown cell font and font-family
    """
    # Notebook FontFamily
    if nbfontfamily == 'sans':
        nbfont = 'Droid Sans'
        nbfontfamily='sans-serif'
    elif fontfamily == 'serif':
        nbfont = 'Crimson Text'
    # Text Cell FontFamily
    if tcfontfamily == 'sans':
        tcfont = 'Droid Sans'
        tcfontfamily='sans-serif'
        tcfontsize = "105%"
    elif tcfontfamily == 'serif':
        tcfont = 'Libre Baskerville'
        tcfontsize = "105%"
    stylecontent += '@notebook-fontfamily: "{}", {}; \n'.format(nbfont, nbfontfamily)
    stylecontent += '@text-cell-fontfamily: "{}", {}; \n'.format(tcfont, tcfontfamily)
    stylecontent += '@text-cell-fontsize: {}; \n'.format(tcfontsize)
    return stylecontent

def set_toolbar_pref(stylecontent, toolbar=False):
    """ Hides toolbar if toolbar==False (default)
    """
    toolbar_string = 'div#maintoolbar {display: none !important;}'
    if toolbar:
        print('Enabling Toolbar')
        toolbar_string = '/*' + toolbar_string + "*/"
    stylecontent += toolbar_string + '\n\n'
    return stylecontent

def set_cell_layout(stylecontent, cellwidth=950, altmd=False):
    """ set general layout and style properties of text and code cells
    """
    textcell_bg = '@cc-input-bg'
    if altmd:
        # alternative markdown/textcell layout
        textcell_bg = '@notebook-bg'
    tc_prompt_border = '@text-cell-bg'
    prompt_width = 10.8
    tc_prompt_width = 5
    prompt_fs = 8
    if cellwidth>=950:
        prompt_width = 11.5
        tc_prompt_width = prompt_width
        prompt_fs = 9
        tc_prompt_border = '@tc-prompt'
    stylecontent += '@cell-width: {}px; \n'.format(cellwidth)
    stylecontent += '@prompt-width: {}ex; \n'.format(prompt_width)
    stylecontent += '@prompt-fontsize: {}pt; \n'.format(prompt_fs)
    stylecontent += '@text-cell-bg: {}; \n'.format(textcell_bg)
    stylecontent += '@tc-prompt-width: {}ex; \n'.format(tc_prompt_width)
    stylecontent += '@text-cell-prompt: {}; \n'.format(tc_prompt_border)
    return stylecontent

def install_theme(theme, font='Hack', fontsize=11, cellwidth=950, altmd=False, nbfontfamily='sans', tcfontfamily='serif', toolbar=False):
    """ install theme to css_fpath with specified font, fontsize,
    md layout, and toolbar pref
    """
    css_content = ''
    with open(fonts_css, 'r') as fonts:
        css_content += fonts.read() + '\n'
    # import theme colors and set font properties
    stylecontent = '@import "styles/{}";\n'.format(theme)
    stylecontent += '@monofont: "{}"; \n'.format(font)
    stylecontent += '@monofontsize: {}pt; \n'.format(fontsize)
    stylecontent = set_cell_layout(stylecontent, cellwidth, altmd)
    stylecontent = set_font_family(stylecontent, nbfontfamily, tcfontfamily)
    stylecontent = set_toolbar_pref(stylecontent, toolbar)
    # read and append main NOTEBOOK layout .less
    with open(nb_layout, 'r') as notebook:
        stylecontent += notebook.read() + '\n'
    # read and append CODEMIRROR layout .less
    with open(cm_layout, 'r') as codemirror:
        stylecontent += codemirror.read() + '\n'
    # read and append CELL layout .less
    with open(cl_layout, 'r') as cells:
        stylecontent += cells.read() + '\n'
    # write all content to temp less file
    make_tempfile(stylecontent)
    # compile less to custom.css and write to install dir
    css_content += write_to_css()
    # read and append CELL layout .less
    with open(mjax_css, 'r') as mathjax:
        css_content += mathjax.read() + '\n'
    with open(css_fpath, 'w') as f:
        f.write(css_content)
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
        install_theme(args.theme, font=args.font, fontsize=int(args.fontsize),  nbfontfamily=args.nbfontfamily, cellwidth=int(args.cellwidth), altmd=args.altmd, toolbar=args.toolbar, tcfontfamily=args.tcfontfamily)
        exit(0)
