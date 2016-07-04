"""
Juypiter theme installer
Author: miraculixx at github.com, dunovank at github.com
"""
from __future__ import print_function
from jupyter_core.paths import jupyter_config_dir, jupyter_data_dir
import os
import shutil
import argparse
from glob import glob
from tempfile import mkstemp
__version__ = '0.4.6'

jnb_config_dir = jupyter_config_dir()
HOME = os.path.expanduser('~')
install_path = os.path.join(jnb_config_dir, 'custom')
nbconfig_path = os.path.join(jnb_config_dir, 'nbconfig')

# Ensure all install dirs exist
if not os.path.isdir(jnb_config_dir):
    os.makedirs(jnb_config_dir)
if not os.path.isdir(install_path):
    os.makedirs(install_path)
if not os.path.isdir(nbconfig_path):
    os.makedirs(nbconfig_path)

package_dir = os.path.dirname(os.path.realpath(__file__))
styles_dir = os.path.join(package_dir, 'styles')
default_toolbar_string='div#maintoolbar {display: none !important;}'
default_font_string="div.CodeMirror pre {font-family: 'Hack', monospace; font-size: 11pt;}"

def get_themes():
    """ return list of available themes """
    themes = [os.path.basename(theme).replace('.css', '')
              for theme in glob('{0}/*.css'.format(styles_dir))]
    return themes

def set_nb_theme(name):
    """ set theme from within notebook """
    from IPython.core.display import HTML
    css_path = glob('{0}/{1}.css'.format(styles_dir, name))[0]
    customcss = open(css_path, "r").read()
    return HTML(''.join(['<style> ', customcss, ' </style>']))

def install_theme(name, toolbar=False, fontsize=12, font="'Hack'"):
    """ copy given styles/<theme name>.css --> ~/.jupyter/custom/custom.css
    """
    source_path = glob('{0}/{1}.css'.format(styles_dir, name))[0]
    font_string="div.CodeMirror pre {font-family: %s, monospace; font-size: %dpt;}" % (font, fontsize)
    # -- install theme
    customcss_path = '{0}/custom.css'.format(install_path)
    shutil.copy(source_path, customcss_path)
    print("Installing {0} at {1}".format(name, install_path))
    fh, abs_path = mkstemp()
    with open(abs_path, 'w') as cssfile:
        with open(customcss_path) as old_file:
            for line in old_file:
                if toolbar:
                    # -- enable toolbar if requested
                    restore_toolbar='/*'+default_toolbar_string+'*/'
                    line = line.replace(default_toolbar_string, restore_toolbar)
                # -- set CodeCell font and fontsize
                line = line.replace(default_font_string, font_string)
                cssfile.write(line)
    os.close(fh)
    os.remove(customcss_path)
    shutil.move(abs_path, customcss_path)

def edit_config(linewrap=False, iu=4):
    """ toggle linewrapping and set size of indent unit
        with notebook.json config file in ~/.jupyter/nbconfig/
    """
    if linewrap:
        lw='true'
    else:
        lw='false'
    PARAMS_string = '{{\n{:<2}"CodeCell": {{\
    \n{:<4}"cm_config": {{\
    \n{:<6}"indentUnit": {},\
    \n{:<6}"lineWrapping": {}\
    \n{:<4}}}\n{:<2}}},\
    \n{:<2}"nbext_hide_incompat": false\n}}'.format('','','', iu,'',lw,'','','')
    actual_config_path = os.path.expanduser(os.path.join(nbconfig_path))
    if not os.path.exists(actual_config_path):
        os.makedirs(actual_config_path)
    config_file_path = '%s/notebook.json' % actual_config_path
    with open(config_file_path, 'w+') as cfile:
        cfile.write(PARAMS_string)

def reset_default():
    """ remove custom.css import"""
    jnb_cached = os.path.join(jupyter_data_dir(), 'nbextensions')
    paths = [install_path, jnb_cached]
    for fpath in paths:
        old = '{0}/{1}.css'.format(fpath, 'custom')
        old_save = '{0}/{1}.css'.format(fpath, 'custom_old')
        try:
            shutil.copy(old, old_save)
            os.remove(old)
            print("Reset default theme here: {0}".format(fpath))
        except Exception:
            print("Already set to default theme in {0}".format(fpath))
            pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', "--theme", action='store',
                        help="name of the theme to install")
    parser.add_argument('-l', "--list", action='store_true',
                        help="list available themes")
    parser.add_argument('-r', "--reset", action='store_true',
                        help="reset to default theme")
    # notebook options
    parser.add_argument('-T', "--toolbar", action='store_true',
                        default=False,
                        help="if specified will enable the toolbar")
    parser.add_argument('-fs', "--fontsize", action='store',
                        default=11, help='set the CodeCell font-size')
    parser.add_argument('-f', "--font", action='store',
                        default='Hack', help='set the CodeCell font')
    # nb config options
    parser.add_argument('-lw', "--linewrap", action='store_true',
                        default=False,
                        help="if specified will enable linewrapping in code cells")
    parser.add_argument('-iu', "--indentunit", action='store',
                        default='4', help="set indent unit for code cells")
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
        if args.toolbar:
            print('Enabling Toolbar')
        install_theme(args.theme, toolbar=args.toolbar, fontsize=int(args.fontsize), font="'"+args.font+"'")
        exit(0)
    if args.linewrap or args.indentunit!='4':
        edit_config(linewrap=args.linewrap, iu=str(args.indentunit))
