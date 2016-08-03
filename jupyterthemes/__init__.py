"""
Juypiter theme installer
Author: dunovank at github.com
"""
from __future__ import print_function
from argparse import ArgumentParser
from jupyter_core.paths import jupyter_config_dir
import os
from glob import glob
__version__ = '0.10.3'

modules = glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules]

# path to local site-packages/jupyterthemes
package_dir = os.path.dirname(os.path.realpath(__file__))
# path to save tempfile with style_less before reading/compiling
tempfile = os.path.join(package_dir, 'tempfile.less')
# path to install custom.css file (~/.jupyter/custom/)
jupyter_path = jupyter_config_dir()
jupyter_custom = os.path.join(jupyter_path, 'custom')
css_fpath = os.path.join(jupyter_custom, 'custom.css')

# Ensure all install dirs exist
if not os.path.isdir(jupyter_path):
    os.makedirs(jupyter_path)
if not os.path.isdir(jupyter_custom):
    os.makedirs(jupyter_custom)

def install_precompiled_theme(theme):
    from shutil import copyfile
    compiled_dir = os.path.join(package_dir, 'styles/compiled')
    theme_src = os.path.join(compiled_dir, '{}.css'.format(theme))
    theme_dst = os.path.join(jupyter_custom, 'custom.css')
    copyfile(theme_src, theme_dst)

def less_to_css(style_less):
    """ write less-compiled css file to css_fpath in jupyter_dir
    """
    import lesscpy
    with open(tempfile, 'w') as f:
        f.write(style_less)
    os.chdir(package_dir)
    style_css = lesscpy.compile(tempfile)
    style_css += '\n\n'
    return style_css

def get_themes():
    """ return list of available themes """
    styles_dir = os.path.join(package_dir, 'styles')
    themes = [os.path.basename(theme).replace('.less', '')
              for theme in glob('{0}/*.less'.format(styles_dir))]
    return themes

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

def install_theme(theme, monofont='Hack', monosize=11, nbfontfam='sans-serif', tcfontfam='sans-serif', cellwidth=940, lineheight=160, altlayout=False, toolbar=False, logo=False, nbname=False):
    """ install theme to css_fpath with specified font, fontsize,
    md layout, and toolbar pref
    """
    from jupyterthemes import stylefx
    less_compatible = stylefx.test_less_compatibility(theme)
    if not less_compatible:
        install_precompiled_theme(theme)
        return None
    # initialize style_less & style_css
    style_less, style_css = '', ''
    monofonts_google = stylefx.get_fonts('mono')
    if monofont in list(monofonts_google):
        monofont, ital = monofonts_google[monofont]
        style_css = stylefx.import_monofont(style_css, fontname=monofont, ital=ital)
    style_less += '@import "styles/{}";\n'.format(theme)
    style_less = stylefx.set_monofont(style_less, monofont, monosize)
    style_less = stylefx.set_nb_font(style_less, nbfontfam)
    style_less = stylefx.set_txt_font(style_less, tcfontfam)
    # define some vars for cell layout
    style_less = stylefx.style_layout(style_less, cellwidth=cellwidth, lineheight=lineheight, altlayout=altlayout, toolbar=toolbar, logo=logo, nbname=nbname)
    # compile tempfile.less to css code and append to style_css
    style_css += less_to_css(style_less)
    # append mathjax css & script to style_css
    style_css = stylefx.set_mathjax(style_css)
    # install style_css to .jupyter/custom/custom.css
    custom_css = os.path.join(jupyter_custom, 'custom.css')
    with open(css_fpath, 'w') as custom_css:
        custom_css.write(style_css)
    # remove tempfile.less from package_dir
    os.remove(tempfile)

def main():
    parser = ArgumentParser()
    parser.add_argument('-l', "--list", action='store_true', help="list available themes")
    parser.add_argument('-t', "--theme", action='store', help="theme name to install")
    parser.add_argument('-f',"--monofont", action='store', default='Hack', help='monospace code font')
    parser.add_argument('-fs', "--monosize", action='store', default=11, help='code font-size')
    parser.add_argument('-nbff',"--nbfontfam", action='store', default='sans-serif', help='nb font-family')
    parser.add_argument('-tcff',"--tcfontfam", action='store', default='sans-serif', help='txt font-family')
    parser.add_argument('-cw', "--cellwidth", action='store', default=940, help="set cell width (px)")
    parser.add_argument('-lh',"--lineheight", action='store', default=160, help='code/text line-height (%%)')
    parser.add_argument('-alt', "--altlayout", action='store_true', default=False, help="alt markdown layout")
    parser.add_argument('-T', "--toolbar", action='store_true', default=False, help="make toolbar visible")
    parser.add_argument('-N', "--nbname", action='store_true', default=False, help="make nb name visible")
    parser.add_argument('-L', "--logo", action='store_true', default=False, help="make jupyter logo visible")
    parser.add_argument('-r', "--reset", action='store_true', help="reset to default theme")
    args = parser.parse_args()
    themes = get_themes()
    say_themes = "Available Themes: \n   {}".format('\n   '.join(themes))
    if args.theme:
        if args.theme not in themes:
            print("Didn't recognize theme name: {}".format(args.theme))
            print(say_themes)
            exit(1)
        print("Installing {0} at {1}".format(args.theme, css_fpath))
        install_theme(args.theme, monofont=args.monofont, monosize=args.monosize, nbfontfam=args.nbfontfam, tcfontfam=args.tcfontfam, cellwidth=int(args.cellwidth),  lineheight=int(args.lineheight), altlayout=args.altlayout, toolbar=args.toolbar, nbname=args.nbname, logo=args.logo)
    elif args.reset:
        reset_default()
    elif args.list:
        print(say_themes)
    else:
        print('No theme provided, no changes made')
