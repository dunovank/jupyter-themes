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
__version__ = '0.5.6'

package_dir = os.path.dirname(os.path.realpath(__file__))
jupyter_dir = jpaths.jupyter_config_dir()
jupyter_custom = os.path.join(jupyter_dir, 'custom')
jupyter_config = os.path.join(jupyter_dir, 'nbconfig')
layouts_dir = os.path.join(package_dir, 'layout')
styles_dir = os.path.join(package_dir, 'styles')

css_fpath = os.path.join(jupyter_custom, 'custom.css')
less_tempfile = os.path.join(package_dir, 'temp_file.less')
less_template = os.path.join(layouts_dir, 'notebook.less')

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

def install_theme(theme, font='Hack', fontsize=11, toolbar=False):
    """ install theme to css_fpath with specified font, fontsize, and toolbar pref
    """
    font_string = "@monofont: '{}';\n".format(font)
    fontsize_string = "@monofontsize: {}pt;\n".format(fontsize)
    toolbar_string = 'div#maintoolbar {display: none !important;}'
    if toolbar:
        print('Enabling Toolbar')
        toolbar_string = '/*' + toolbar_string + "*/"

    print("Installing {0} at {1}".format(theme, css_fpath))
    theme_fpath = os.path.join(styles_dir, '{}.less'.format(theme))
    stylecontent = '@import "styles/{}";\n'.format(theme)
    stylecontent += font_string
    stylecontent += fontsize_string
    stylecontent += toolbar_string+'\n\n'
    with open(less_template, 'r') as f_template:
        stylecontent += f_template.read() + '\n'
    make_tempfile(stylecontent)
    write_to_css()

def set_nb_theme(theme):
    """ set theme from within notebook """
    from IPython.core.display import HTML
    install_theme(theme)
    # css_path = glob('{0}/{1}.css'.format(css, name))[0]
    customcss = open(css_fpath, "r").read()
    return HTML(''.join(['<style> ', customcss, ' </style>']))

def edit_config(linewrap=False, iu=4):
    """ toggle linewrapping and set size of indent unit
        with notebook.json config file in ~/.jupyter/nbconfig/
    """
    if linewrap:
        lw='true'
    else:
        lw='false'
    params_string = '{{\n{:<2}"CodeCell": {{\
    \n{:<4}"cm_config": {{\
    \n{:<6}"indentUnit": {},\
    \n{:<6}"lineWrapping": {}\
    \n{:<4}}}\n{:<2}}},\
    \n{:<2}"nbext_hide_incompat": false\n}}'.format('','','', iu,'',lw,'','','')
    config_file_path = os.path.join(jupyter_config, 'notebook.json')
    with open(config_file_path, 'w+') as cfile:
        cfile.write(params_string)

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', "--theme", action='store', help="name of the theme to install")
    parser.add_argument('-l', "--list", action='store_true', help="list available themes")
    parser.add_argument('-r', "--reset", action='store_true', help="reset to default theme")
    parser.add_argument('-T', "--toolbar", action='store_true', default=False, help="enable the toolbar")
    parser.add_argument('-fs', "--fontsize", action='store', default=11, help='set the CodeCell font-size')
    parser.add_argument('-f', "--font", action='store', default='Hack', help='set the CodeCell font')
    parser.add_argument('-lw', "--linewrap", action='store_true', default=False, help="enable linewrapping")
    parser.add_argument('-iu', "--indentunit", action='store', default='4', help="set indent unit")
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
        install_theme(args.theme, font=args.font, fontsize=int(args.fontsize), toolbar=args.toolbar)
        exit(0)
    if args.linewrap or args.indentunit!='4':
        edit_config(linewrap=args.linewrap, iu=str(args.indentunit))
