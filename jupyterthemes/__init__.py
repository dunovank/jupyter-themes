"""
Juypiter theme installer
Author: miraculixx at github.com
# MODIFIED by dunovank at github.com
"""
from __future__ import print_function
from jupyter_core.paths import jupyter_config_dir
import os
import shutil
import argparse
import subprocess
from glob import glob
from tempfile import mkstemp

jnb_config_dir = jupyter_config_dir()
HOME = os.path.expanduser('~')
INSTALL_JPATH = os.path.join(jnb_config_dir, 'custom')
NBCONFIG_PATH = os.path.join(jnb_config_dir, 'nbconfig')
THEMES_PATH = os.path.join(HOME, '.jupyter-themes')
DEFAULT_FONT="'Hack'"
DEFAULT_FONTSIZE=11
DEFAULT_TOOLBAR_STRING='div#maintoolbar {display: none !important;}'
DEFAULT_FONT_STRING="div.CodeMirror pre {font-family: %s, monospace; font-size: %dpt;}" % (DEFAULT_FONT, DEFAULT_FONTSIZE)

def get_themes():
    """ return list of available themes """
    path = THEMES_PATH
    themes = [os.path.basename(theme).replace('.css', '')
              for theme in glob('%s/*.css' % path)]
    return themes

def get_install_path():
    """ return install path
    """
    #install to ~/.jupyter/custom
    actual_jpath = os.path.expanduser(os.path.join(INSTALL_JPATH))
    if not os.path.exists(actual_jpath):
        os.makedirs(actual_jpath)
    return actual_jpath

def install_theme(name, toolbar=False, fontsize=12, font="'Hack'"):
    """ copy given theme to theme.css and import css in custom.css
    """
    source_path = glob('%s/%s.css' % (THEMES_PATH, name))[0]
    install_path = get_install_path()
    FONT_STRING="div.CodeMirror pre {font-family: %s, monospace; font-size: %dpt;}" % (font, fontsize)
    # -- install theme
    customcss_path = '%s/custom.css' % install_path
    shutil.copy(source_path, customcss_path)
    print("Installing %s at %s" % (name, install_path))
    fh, abs_path = mkstemp()
    with open(abs_path, 'w') as cssfile:
        with open(customcss_path) as old_file:
            for line in old_file:
                if toolbar:
                    print("Enabling toolbar")
                    # -- enable toolbar if requested
                    RESTORE_TOOLBAR='/*'+DEFAULT_TOOLBAR_STRING+'*/'
                    line = line.replace(DEFAULT_TOOLBAR_STRING,RESTORE_TOOLBAR)
                # -- set CodeCell font and fontsize
                line = line.replace(DEFAULT_FONT_STRING, FONT_STRING)
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
    PARAMS_STRING = '{{\n{:<2}"CodeCell": {{\
    \n{:<4}"cm_config": {{\
    \n{:<6}"indentUnit": {},\
    \n{:<6}"lineWrapping": {}\
    \n{:<4}}}\n{:<2}}},\
    \n{:<2}"nbext_hide_incompat": false\n}}'.format('','','', iu,'',lw,'','','')
    actual_config_path = os.path.expanduser(os.path.join(NBCONFIG_PATH))
    if not os.path.exists(actual_config_path):
        os.makedirs(actual_config_path)
    config_file_path = '%s/notebook.json' % actual_config_path
    with open(config_file_path, 'w+') as cfile:
        cfile.write(PARAMS_STRING)

def reset_default():
    """ remove custom.css import"""
    from jupyter_core.paths import jupyter_data_dir
    jnb_cached = os.path.join(jupyter_data_dir(), 'nbextensions')
    paths = [INSTALL_JPATH, jnb_cached]
    for fpath in paths:
        old = '%s/%s.css' % (fpath, 'custom')
        old_save = '%s/%s.css' % (fpath, 'custom_old')
        try:
            shutil.copy(old, old_save)
            os.remove(old)
            print("Reset default theme here: %s" % fpath)
        except Exception:
            print("Already set to default theme in %s" % fpath)
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

    if args.list:
        themes = get_themes()
        print("Themes in %s" % THEMES_PATH)
        print('\n'.join(themes))
        exit(0)
    if args.theme:
        themes = get_themes()
        if args.theme not in themes:
            print("Theme %s not found. Available: %s"%(args.theme, ' '.join(themes)))
            exit(1)
        install_theme(args.theme, toolbar=args.toolbar, fontsize=int(args.fontsize), font="'"+args.font+"'")
        exit(0)
    if args.linewrap or args.indentunit!='4':
        edit_config(linewrap=args.linewrap, iu=str(args.indentunit))
    elif args.reset:
        reset_default()
