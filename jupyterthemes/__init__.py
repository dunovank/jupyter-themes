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
__version__ = '0.6.0'

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
    with open(css_fpath, 'w') as f:
        f.write(css_content)
    os.remove(less_tempfile)

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

def set_textcell_font(stylecontent, tcfont_family='sans-serif'):
    """ set text and markdown cell font and font-family
    """
    if tcfont_family == 'sans-serif':
        tcfont='Open-Sans'
    else:
        tcfont = 'Times'
    stylecontent += '@text-cell-font: "{}"; \n'.format(tcfont)
    stylecontent += '@text-cell-fontfamily: {}; \n'.format(tcfont_family)
    return stylecontent

def set_toolbar_pref(stylecontent, toolbar=False):
    # set toolbar preference
    toolbar_string = 'div#maintoolbar {display: none !important;}'
    if toolbar:
        print('Enabling Toolbar')
        toolbar_string = '/*' + toolbar_string + "*/"
    stylecontent += toolbar_string + '\n\n'
    return stylecontent

def set_cell_layout(stylecontent, view='narrow', altmd=False):
    """ set general layout and style properties of text and code cells
    """
    textcell_bg = '@cc-input-bg'
    if altmd:
        # alternative markdown/textcell layout
        textcell_bg = '@notebook-bg'
    prompt_width = '11ex'
    tc_prompt_width = prompt_width
    cell_width = 'inherit'
    prompt_fs = '9.5pt'
    tc_prompt_border = '@tc-prompt'
    if view=='narrow':
        prompt_width = '9.5ex'
        tc_prompt_width = '0ex'
        cell_width = '900px'
        prompt_fs = '9pt'
        tc_prompt_border = textcell_bg
    stylecontent += '@text-cell-bg: {}; \n'.format(textcell_bg)
    stylecontent += '@prompt-width: {}; \n'.format(prompt_width)
    stylecontent += '@tc-prompt-width: {}; \n'.format(tc_prompt_width)
    stylecontent += '@prompt-fontsize: {}; \n'.format(prompt_fs)
    stylecontent += '@cell-width: {}; \n'.format(cell_width)
    stylecontent += '@text-cell-prompt: {}; \n'.format(tc_prompt_border)
    return stylecontent

def install_theme(theme, font='Hack', fontsize=11, view='narrow', altmd=False, tcfont_family='sans-serif', toolbar=False):
    """ install theme to css_fpath with specified font, fontsize,
    md layout, and toolbar pref
    """
    # import theme colors and set font properties
    stylecontent = '@import "styles/{}";\n'.format(theme)
    stylecontent += '@monofont: "{}"; \n'.format(font)
    stylecontent += '@monofontsize: {}pt; \n'.format(fontsize)
    stylecontent = set_cell_layout(stylecontent, view, altmd)
    stylecontent = set_textcell_font(stylecontent, tcfont_family)
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
    write_to_css()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', "--theme", action='store', help="name of the theme to install")
    parser.add_argument('-altmd', "--altmd", action='store_true', default=False, help="alternative markdown layout")
    parser.add_argument('-vw', "--view", action='store', default='narrow', help="choose wide or narrow view")
    parser.add_argument('-l', "--list", action='store_true', help="list available themes")
    parser.add_argument('-r', "--reset", action='store_true', help="reset to default theme")
    parser.add_argument('-T', "--toolbar", action='store_true', default=False, help="enable the toolbar")
    parser.add_argument('-fs', "--fontsize", action='store', default=11, help='set the CodeCell font-size')
    parser.add_argument('-f',"--font", action='store', default='Hack', help='set the CodeCell font')
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
        install_theme(args.theme, font=args.font, fontsize=int(args.fontsize), view=args.view, altmd=args.altmd, toolbar=args.toolbar)
        exit(0)
