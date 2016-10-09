"""
Juypiter theme installer
Author: dunovank at github.com
"""
from __future__ import print_function
import os, sys
from argparse import ArgumentParser
from glob import glob
modules = glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules]

major = 0
minor = 13
patch = 7
__version__ = '.'.join([str(v) for v in [major, minor, patch]])

# path to local site-packages/jupyterthemes
package_dir = os.path.dirname(os.path.realpath(__file__))

def get_themes():
    """ return list of available themes """
    styles_dir = os.path.join(package_dir, 'styles')
    themes = [os.path.basename(theme).replace('.less', '')
              for theme in glob('{0}/*.less'.format(styles_dir))]
    return themes

def install_theme(theme, monofont='droidmono', monosize=11, nbfont='exosans', nbfontsize=13, tcfont='loraserif', tcfontsize=13, margins='auto', cellwidth=980, lineheight=170, cursorwidth=2, cursorcolor='default', altlayout=False, altprompt=False, hideprompt=False, vimext=False, toolbar=False, nbname=False):
    """ install theme to jupyter_customcss with specified font, fontsize,
    md layout, and toolbar pref
    """
    from jupyterthemes import stylefx
    stylefx.reset_default(False)
    stylefx.check_directories()
    # initialize style_less & style_css
    style_less = stylefx.set_font_properties(monofont=monofont, monosize=monosize, nbfont=nbfont, nbfontsize=nbfontsize, tcfont=tcfont, tcfontsize=tcfontsize)
    # define some vars for cell layout
    cursorcolor = stylefx.get_colors(theme=theme, c=cursorcolor)
    style_less = stylefx.style_layout(style_less, theme=theme, cellwidth=cellwidth, margins=margins, lineheight=lineheight, altlayout=altlayout, altprompt=altprompt, hideprompt=hideprompt, cursorwidth=cursorwidth, cursorcolor=cursorcolor, vimext=vimext, toolbar=toolbar, nbname=nbname)
    # compile tempfile.less to css code and append to style_css
    style_css = stylefx.less_to_css(style_less)
    # append mathjax css & script to style_css
    style_css = stylefx.set_mathjax_style(style_css)
    # install style_css to .jupyter/custom/custom.css
    stylefx.write_final_css(style_css)
    # remove tempfile.less from package_dir
    stylefx.remove_temp_files(vimext=vimext)

def main():
    parser = ArgumentParser()
    parser.add_argument('-l', "--list", action='store_true', help="list available themes")
    parser.add_argument('-t', "--theme", action='store', help="theme name to install")
    parser.add_argument('-f',"--monofont", action='store', default='droidmono', help='monospace code font')
    parser.add_argument('-fs', "--monosize", action='store', default='11', help='code font-size')
    parser.add_argument('-nf',"--nbfont", action='store', default='exosans', help='notebook font')
    parser.add_argument('-nfs',"--nbfontsize", action='store', default='13', help='notebook fontsize')
    parser.add_argument('-tf',"--tcfont", action='store', default='loraserif', help='txtcell font')
    parser.add_argument('-tfs',"--tcfontsize", action='store', default='13', help='txtcell fontsize')
    parser.add_argument('-m', "--margins", action='store', default='auto', help="fix margins of main intro page")
    parser.add_argument('-cursw', "--cursorwidth", action='store', default=2, help="set cursorwidth (px)")
    parser.add_argument('-cursc', "--cursorcolor", action='store', default='default', help="cursor color (r, b, g, p)")
    parser.add_argument('-cellw', "--cellwidth", action='store', default=980, help="set cell width (px)")
    parser.add_argument('-lineh',"--lineheight", action='store', default=170, help='code/text line-height (%%)')
    parser.add_argument('-alt', "--altlayout", action='store_true', default=False, help="alt markdown layout")
    parser.add_argument('-altp', "--altprompt", action='store_true', default=False, help="alt input prompt style")
    parser.add_argument('-P', "--hideprompt", action='store_true', default=False, help="hide cell input prompt")
    parser.add_argument('-T', "--toolbar", action='store_true', default=False, help="make toolbar visible")
    parser.add_argument('-N', "--nbname", action='store_true', default=False, help="nb name/logo visible")
    parser.add_argument('-vim', "--vimext", action='store_true', default=False, help="toggle styles for vim")
    parser.add_argument('-r', "--reset", action='store_true', help="reset to default theme")
    args = parser.parse_args()
    themes = get_themes()
    say_themes = "Available Themes: \n   {}".format('\n   '.join(themes))
    if args.theme:
        if args.theme not in themes:
            print("Didn't recognize theme name: {}".format(args.theme))
            print(say_themes)
            exit(1)
        install_theme(args.theme, monofont=args.monofont, monosize=args.monosize, nbfont=args.nbfont, nbfontsize=args.nbfontsize, tcfont=args.tcfont, tcfontsize=args.tcfontsize, cellwidth=int(args.cellwidth), margins=args.margins, lineheight=int(args.lineheight), cursorwidth=args.cursorwidth, cursorcolor=args.cursorcolor, altlayout=args.altlayout, altprompt=args.altprompt, hideprompt=args.hideprompt, vimext=args.vimext, toolbar=args.toolbar, nbname=args.nbname)
    elif args.reset:
        from jupyterthemes import stylefx
        stylefx.reset_default(verbose=True)
    elif args.list:
        print(say_themes)
    else:
        print('No theme provided, no changes made')
