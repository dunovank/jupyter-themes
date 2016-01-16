"""
Juypiter theme installer
Author: miraculixx at github.com
# MODIFIED by dunovank at github.com
"""
import argparse
from glob import glob
import os
import sys
import shutil
import subprocess

IPY_HOME = '~/.ipython/{profile}'
INSTALL_IPATH = '~/.ipython/{profile}/static/custom'
INSTALL_JPATH = '~/.jupyter/custom'
THEMES_PATH = os.path.expanduser('~/.jupyter-themes')
DEFAULT_PROFILE = 'default'


def get_themes():
    """ return list of available themes """
    path = THEMES_PATH
    themes = [os.path.basename(theme).replace('.css', '')
              for theme in glob('%s/*.css' % path)]
    return themes


def install_path(profile=None, jupyter=True):
    """ return install path for profile, creates profile if profile does not exist """

    paths = []
    profile = profile or DEFAULT_PROFILE
    home_path = os.path.expanduser(os.path.join(IPY_HOME))
    profile_path = home_path.format(profile='profile_'+profile)
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
    if jupyter:
        actual_jpath = os.path.expanduser(os.path.join(INSTALL_JPATH))
        if not os.path.exists(actual_jpath):
            os.makedirs(actual_jpath)
        paths.append(actual_jpath)

    return paths

def install_theme(name, profile=None, toolbar=False, jupyter=True):
    """ copy given theme to theme.css and import css in custom.css """

    source_path = glob('%s/%s.css' % (THEMES_PATH, name))[0]
    paths = install_path(profile, jupyter)

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

        # -- enable toolbar if requested
        if toolbar:
            print("Enabling toolbar")
            with open(themecss_path, 'w+') as themefile:
                # TODO do some proper css rewrite
                lines = (line.replace('div#maintoolbar', 'div#maintoolbar_active')
                                  for line in themefile.readlines())
                themefile.seek(0)
                themefile.writelines(lines)
                themefile.truncate()
        else:
            print("Toolbar is disabled. Set -T to enable")


def reset_default(profile=None, jupyter=True):
    """ remove theme.css import """
    paths = install_path(profile, jupyter)
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
                        help="the name of the theme to install")
    parser.add_argument('-l', "--list", action='store_true',
                        help="list available themes")
    parser.add_argument('-r', "--reset", action='store_true',
                        help="reset to default theme")
    parser.add_argument('-T', "--toolbar", action='store_true',
                        default=False,
                        help="if specified will enable the toolbar")
    parser.add_argument('-J', "--jupyter", action='store_true',
                        default=False,
                        help="install for jupyter (ipython 4.X+)")
    parser.add_argument('-p', "--profile", action='store',
                        default=DEFAULT_PROFILE,
                        help="set the profile, defaults to %s" % DEFAULT_PROFILE)
    args = parser.parse_args()

    if args.list:
        themes = get_themes()
        print("Themes in %s" % THEMES_PATH)
        print('\n'.join(themes))
        exit(0)
    if args.theme:
        themes = get_themes()
        if args.theme not in themes:
            print("Theme %s not found. Available: %s" % (args.theme,
                                                         ' '.join(themes)))
            exit(1)
        install_theme(args.theme, profile=args.profile, toolbar=args.toolbar, jupyter=args.jupyter)
        exit(0)
    if args.reset:
        reset_default(profile=args.profile, jupyter=args.jupyter)
