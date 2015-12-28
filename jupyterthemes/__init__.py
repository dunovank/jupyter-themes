"""
Juypiter theme installer
Author: miraculixx at github.com
"""
import argparse
from glob import glob
import os
import sys

INSTALL_PATH = '~/.ipython/{profile}/static/custom/'
THEMES_PATH = os.path.expanduser('~/.jupyter-themes')
DEFAULT_PROFILE = 'profile_default' 

def get_themes():
    """ return list of available themes """
    path = THEMES_PATH
    themes = [os.path.basename(theme).replace('.css', '') 
              for theme in glob('%s/*.css' % path)]
    return themes

def install_path(profile=None):
    """ return install path for profile, exits if profile does not exists """
    profile = profile or DEFAULT_PROFILE 
    actual_path = os.path.expanduser(os.path.join(INSTALL_PATH))
    actual_path = actual_path.format(profile=profile)
    if not os.path.exists(actual_path):
        print "Profile %s does not exist at %s" % (profile, actual_path) 
        exit(1)
    return actual_path

def install_theme(name, profile=None, toolbar=False):
    """ copy given theme to theme.css and import css in custom.css """
    from sh import cp  # @UnresolvedImport (annotation for pydev)
    source_path = glob('%s/%s.css' % (THEMES_PATH, name))[0]
    target_path = install_path(profile)
    # -- install theme
    themecss_path = '%s/theme.css' % target_path
    cp(source_path, themecss_path)
    # -- check if theme import is already there, otherwise add it
    print "Installing %s at %s" % (name, target_path)
    with open('%s/custom.css' % target_path, 'r+a') as customcss:
        if not 'theme.css' in ' '.join(customcss.readlines()):
            customcss.seek(0, os.SEEK_END)
            customcss.write("\n@import url('theme.css');")
    # -- enable toolbar if requested
    if toolbar:
        print "Enabling toolbar"
        with open(themecss_path, 'rs+w') as themefile:
            # TODO do some proper css rewrite
            lines = (line.replace('div#maintoolbar', 'div#maintoolbar_active') 
                                  for line in themefile.readlines())
            themefile.seek(0)
            themefile.writelines(lines)
            themefile.truncate()
    else:
        print "Toolbar is disabled. Set -T to enable"
          
def reset_default(profile=None):
    """ remove theme.css import """
    actual_path = install_path(profile)
    with open('%s/custom.css' % actual_path, 'r+w') as customcss:
        lines = (line for line in customcss.readlines() 
                 if 'theme.css' not in line)
        customcss.seek(0)
        customcss.writelines(lines)
        customcss.truncate()
    print "Reset theme for profile %s at %s" % (profile or DEFAULT_PROFILE, 
                                                actual_path)

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
    parser.add_argument('-p', "--profile", action='store', 
                        default=DEFAULT_PROFILE,
                        help="set the profile, defaults to %s" % DEFAULT_PROFILE)
    args = parser.parse_args()
    if args.list:
        themes = get_themes()
        print "Themes in %s" % THEMES_PATH
        print '\n'.join(themes)
        exit(0)
    if args.theme:
        themes = get_themes()
        if args.theme not in themes:
            print "Theme %s not found. Available: %s" % (args.theme, 
                                                         ' '.join(themes))
            exit(1)
        install_theme(args.theme, profile=args.profile, toolbar=args.toolbar) 
        exit(0)
    if args.reset:
        reset_default(profile=args.profile)
        