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
IPY_HOME = HOME + '/.ipython/{profile}'
INSTALL_IPATH = HOME + '/.ipython/{profile}/static/custom'
INSTALL_JPATH = HOME + '/.jupyter/custom'
THEMES_PATH = HOME + '/.jupyter-themes'
DEFAULT_PROFILE = 'default'
DEFAULT_FONTSIZE='12'
DEFAULT_TOOLBAR_STRING='div#maintoolbar {display: none !important;}'
DEFAULT_FONTSIZE_STRING1=".cm-s-ipython.CodeMirror {font-size:%spt !important;}" % DEFAULT_FONTSIZE
DEFAULT_FONTSIZE_STRING2="div.CodeMirror pre {font-size:%spt !important;}" % DEFAULT_FONTSIZE

def get_themes():
    """ return list of available themes """
    path = THEMES_PATH
    themes = [os.path.basename(theme).replace('.css', '')
              for theme in glob('%s/*.css' % path)]
    return themes


def install_path(profile=None):
    """ return install path for profile, creates profile if profile does not exist """

    paths = []
    profile = profile or DEFAULT_PROFILE
    home_path = os.path.expanduser(os.path.join(IPY_HOME))
    profile_path = home_path.format(profile='profile_' + profile)
    custom_path = '/'.join([profile_path, 'static', 'custom'])

    if not os.path.exists(profile_path):
        print("creating profile: %s" % profile)
        print("Profile %s does not exist at %s" % (profile, home_path))
        subprocess.call(['ipython', 'profile', 'create', profile])
        try:
            shutil.copytree('/'.join([home_path, 'profile_default', 'static/']), '/'.join([profile_path, 'static/']))
        except Exception:
            if not os.path.exists(custom_path):
                os.makedirs('/'.join([profile_path, 'static']))
                os.makedirs('/'.join([profile_path, 'static', 'custom']))
        else:
            print("No ipython config files (~/.ipython/profile_default/static/custom/)")
            print("try again after running ipython, closing & refreshing your terminal session")
    paths.append(custom_path)

    #install to ~/.jupyter/custom
    actual_jpath = os.path.expanduser(os.path.join(INSTALL_JPATH))
    if not os.path.exists(actual_jpath):
        os.makedirs(actual_jpath)
    paths.append(actual_jpath)

    return paths


def install_theme(name, profile=None, update_properties=False, toolbar=False, fontsize='12'):
    """ copy given theme to theme.css and import css in custom.css """

    source_path = glob('%s/%s.css' % (THEMES_PATH, name))[0]
    paths = install_path(profile)
    FONTSIZE_STRING1=".cm-s-ipython.CodeMirror {font-size:%spt !important;}" % fontsize
    FONTSIZE_STRING2="div.CodeMirror pre {font-size:%spt !important;}" % fontsize

    for i, target_path in enumerate(paths):
        # -- install theme
        themecss_path = '%s/theme.css' % target_path
        customcss_path = '%s/custom.css' % target_path
        shutil.copy(source_path, themecss_path)
        shutil.copy(source_path, customcss_path)

        print("Installing %s at %s" % (name, target_path))
        # -- check if theme import is already there, otherwise add it
        with open(customcss_path, 'a+') as customcss:
            if not 'theme.css' in ' '.join(customcss.readlines()):
                customcss.seek(0, os.SEEK_END)
                customcss.write("\n@import url('theme.css');")
        if update_properties:
            fh, abs_path = mkstemp()
            with open(abs_path, 'w') as cssfile:
                with open(customcss_path) as old_file:
                    for line in old_file:
                        if toolbar:
                            # -- enable toolbar if requested
                            RESTORE_TOOLBAR='/*'+DEFAULT_TOOLBAR_STRING+'*/'
                            cssfile.write(line.replace(DEFAULT_TOOLBAR_STRING,RESTORE_TOOLBAR))
                        # -- set CodeCell fontsize
                        cssfile.write(line.replace(DEFAULT_FONTSIZE_STRING1, FONTSIZE_STRING1))
                        cssfile.write(line.replace(DEFAULT_FONTSIZE_STRING2, FONTSIZE_STRING2))
            os.close(fh)
            os.remove(customcss_path)
            shutil.move(abs_path, customcss_path)


def reset_default(profile=None):
    """ remove theme.css import """
    paths = install_path(profile)
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
    parser.add_argument('-f', "--fontsize", action='store',
                        default='12', help='set the fontsize in code cells')
    parser.add_argument('-t', "--theme", action='store',
                        help="the name of the theme to install")
    parser.add_argument('-l', "--list", action='store_true',
                        help="list available themes")
    parser.add_argument('-r', "--reset", action='store_true',
                        help="reset to default theme")
    parser.add_argument('-T', "--toolbar", action='store_true',
                        default=False,
                        help="if specified will enable the toolbar")
    parser.add_argument('-p', "--profile", action='store',
                        default=DEFAULT_PROFILE,
                        help="set the profile, defaults to %s" % DEFAULT_PROFILE)
    args = parser.parse_args()

    update=False
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
        if args.toolbar:
            update=True
            print("Enabling toolbar")
        else:
            print("Toolbar is disabled. Set -T to enable")
        if args.fontsize!=DEFAULT_FONTSIZE:
            update=True

        install_theme(args.theme, profile=args.profile, toolbar=args.toolbar, fontsize=str(args.fontsize), update_properties=update)
        exit(0)
    if args.toolbar:
        print("Enabling toolbar")
    else:
        print("Toolbar is disabled. Set -T to enable")
    if args.reset:
        reset_default(profile=args.profile)
