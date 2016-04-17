"""
Juypiter theme installer
Author: miraculixx at github.com
# MODIFIED by dunovank at github.com
"""
from __future__ import print_function

import os
import shutil
import argparse
import subprocess
from glob import glob
from tempfile import mkstemp

HOME = os.path.expanduser('~')
INSTALL_JPATH = HOME + '/.jupyter/custom'
THEMES_PATH = HOME + '/.jupyter-themes'

DEFAULT_FONT='Hack'
DEFAULT_FONTSIZE='11'
DEFAULT_TOOLBAR_STRING='div#maintoolbar {display: none !important;}'
DEFAULT_FONT_STRING="div.CodeMirror pre {font-family: %s, monospace; font-size: %spt;}" % (DEFAULT_FONT, DEFAULT_FONTSIZE)

def get_themes():
    """ return list of available themes """
    path = THEMES_PATH
    themes = [os.path.basename(theme).replace('.css', '')
              for theme in glob('%s/*.css' % path)]
    return themes


def install_path(paths=[]):
    """ return install path for profile, creates profile if profile does not exist """

    #install to ~/.jupyter/custom
    actual_jpath = os.path.expanduser(os.path.join(INSTALL_JPATH))
    if not os.path.exists(actual_jpath):
        os.makedirs(actual_jpath)
    paths.append(actual_jpath)

    return paths


def install_theme(name, toolbar=False, fontsize='12', font='Hack'):
    """ copy given theme to theme.css and import css in custom.css """

    source_path = glob('%s/%s.css' % (THEMES_PATH, name))[0]
    paths = install_path()
    FONT_STRING="div.CodeMirror pre {font-family: %s, monospace; font-size: %spt;}" % (font, fontsize)

    for i, target_path in enumerate(paths):
        # -- install theme
        customcss_path = '%s/custom.css' % target_path
        shutil.copy(source_path, customcss_path)
        print("Installing %s at %s" % (name, target_path))
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


def reset_default():
    """ remove theme.css import """
    paths = install_path()
    for actual_path in paths:
        old = '%s/%s.css' % (actual_path, 'custom')
        old_save = '%s/%s.css' % (actual_path, 'custom_old')
        try:
            shutil.copy(old, old_save)
            os.remove(old)
            print("Reset default theme here: %s" % actual_path)
        except Exception:
            print("Already set to default theme in %s" % actual_path)
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', "--theme", action='store',
                        help="name of the theme to install")
    parser.add_argument('-l', "--list", action='store_true',
                        help="list available themes")
    parser.add_argument('-r', "--reset", action='store_true',
                        help="reset to default theme")
    parser.add_argument('-T', "--toolbar", action='store_true',
                        default=False,
                        help="if specified will enable the toolbar")
    parser.add_argument('-fs', "--fontsize", action='store',
                        default='12', help='set the CodeCell font-size')
    parser.add_argument('-f', "--font", action='store',
                        default='Hack', help='set the CodeCell font')
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
        install_theme(args.theme, toolbar=args.toolbar, fontsize=str(args.fontsize), font=str(args.font))
        exit(0)
    if args.reset:
        reset_default()
