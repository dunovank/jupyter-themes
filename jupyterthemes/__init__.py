import os
import sys
from argparse import ArgumentParser
from glob import glob
from . import stylefx
from . import jtplot

# path to local site-packages/jupyterthemes
package_dir = os.path.dirname(os.path.realpath(__file__))
modules = glob(os.path.dirname(__file__) + "/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules]

major = 0
minor = 20
patch = 0

__version__ = '.'.join([str(v) for v in [major, minor, patch]])


def get_themes():
    """ return list of available themes """
    styles_dir = os.path.join(package_dir, 'styles')
    themes = [os.path.basename(theme).replace('.less', '')
              for theme in glob('{0}/*.less'.format(styles_dir))]
    return themes


def install_theme(theme=None,
                monofont=None,
                monosize=11,
                nbfont=None,
                nbfontsize=13,
                tcfont=None,
                tcfontsize=13,
                dffontsize=93,
                outfontsize=85,
                mathfontsize=100,
                margins='auto',
                cellwidth='980',
                lineheight=170,
                cursorwidth=2,
                cursorcolor='default',
                altprompt=False,
                altmd=False,
                altout=False,
                hideprompt=False,
                vimext=False,
                toolbar=False,
                nbname=False,
                kernellogo=False,
                dfonts=False):

    """ Install theme to jupyter_customcss with specified font, fontsize,
    md layout, and toolbar pref
    """
    # get working directory
    wkdir = os.path.abspath('./')

    stylefx.reset_default(False)
    stylefx.check_directories()

    doc = '\nConcatenated font imports, .less styles, & custom variables\n'
    s = '*' * 65
    style_less = '\n'.join(['/*', s, s, doc, s, s, '*/'])
    style_less += '\n\n\n'
    style_less += '/* Import Notebook, Markdown, & Code Fonts */\n'

    # initialize style_less & style_css
    style_less = stylefx.set_font_properties(
        style_less=style_less,
        monofont=monofont,
        monosize=monosize,
        nbfont=nbfont,
        nbfontsize=nbfontsize,
        tcfont=tcfont,
        tcfontsize=tcfontsize,
        dffontsize=dffontsize,
        outfontsize=outfontsize,
        mathfontsize=mathfontsize,
        dfonts=dfonts)

    if theme is not None:
        # define some vars for cell layout
        cursorcolor = stylefx.get_colors(theme=theme, c=cursorcolor)
        style_less = stylefx.style_layout(
            style_less,
            theme=theme,
            cellwidth=cellwidth,
            margins=margins,
            lineheight=lineheight,
            altprompt=altprompt,
            altmd=altmd,
            altout=altout,
            hideprompt=hideprompt,
            cursorwidth=cursorwidth,
            cursorcolor=cursorcolor,
            vimext=vimext,
            toolbar=toolbar,
            nbname=nbname,
            kernellogo=kernellogo)

    # compile tempfile.less to css code and append to style_css
    style_css = stylefx.less_to_css(style_less)

    # append mathjax css & script to style_css
    style_css = stylefx.set_mathjax_style(style_css, mathfontsize)

    # install style_css to .jupyter/custom/custom.css
    stylefx.write_final_css(style_css)

    # change back to original working directory
    os.chdir(wkdir)

def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-l',
        "--list",
        action='store_true',
        help="list available themes")
    parser.add_argument(
        '-t',
        "--theme",
        default=None,
        action='store',
        help="theme name to install")
    parser.add_argument(
        '-f',
        "--monofont",
        action='store',
        default=None,
        help='monospace code font')
    parser.add_argument(
        '-fs',
        "--monosize",
        action='store',
        default='11',
        help='code font-size')
    parser.add_argument(
        '-nf',
        "--nbfont",
        action='store',
        default=None,
        help='notebook font')
    parser.add_argument(
        '-nfs',
        "--nbfontsize",
        action='store',
        default='13',
        help='notebook fontsize')
    parser.add_argument(
        '-tf',
        "--tcfont",
        action='store',
        default=None,
        help='txtcell font')
    parser.add_argument(
        '-tfs',
        "--tcfontsize",
        action='store',
        default='13',
        help='txtcell fontsize')
    parser.add_argument(
        '-dfs',
        "--dffontsize",
        action='store',
        default='93',
        help='pandas dataframe fontsize')
    parser.add_argument(
        '-ofs',
        "--outfontsize",
        action='store',
        default='85',
        help='output area fontsize')
    parser.add_argument(
        '-mathfs',
        "--mathfontsize",
        action='store',
        default='100',
        help='mathjax fontsize (in %%)')
    parser.add_argument(
        '-m',
        "--margins",
        action='store',
        default='auto',
        help="fix margins of main intro page")
    parser.add_argument(
        '-cursw',
        "--cursorwidth",
        action='store',
        default=2,
        help="set cursorwidth (px)")
    parser.add_argument(
        '-cursc',
        "--cursorcolor",
        action='store',
        default='default',
        help="cursor color (r, b, g, p)")
    parser.add_argument(
        '-cellw',
        "--cellwidth",
        action='store',
        default='980',
        help="set cell width (px or %%)")
    parser.add_argument(
        '-lineh',
        "--lineheight",
        action='store',
        default=170,
        help='code/text line-height (%%)')
    parser.add_argument(
        '-altp',
        "--altprompt",
        action='store_true',
        default=False,
        help="alt input prompt style")
    parser.add_argument(
        '-altmd',
        "--altmarkdown",
        action='store_true',
        default=False,
        help="alt markdown cell style")
    parser.add_argument(
        '-altout',
        "--altoutput",
        action='store_true',
        default=False,
        help="set output bg color to notebook bg")
    parser.add_argument(
        '-P',
        "--hideprompt",
        action='store_true',
        default=False,
        help="hide cell input prompt")
    parser.add_argument(
        '-T',
        "--toolbar",
        action='store_true',
        default=False,
        help="make toolbar visible")
    parser.add_argument(
        '-N',
        "--nbname",
        action='store_true',
        default=False,
        help="nb name/logo visible")
    parser.add_argument(
        '-kl',
        "--kernellogo",
        action='store_true',
        default=False,
        help="kernel logo visible")
    parser.add_argument(
        '-vim',
        "--vimext",
        action='store_true',
        default=False,
        help="toggle styles for vim")
    parser.add_argument(
        '-r',
        "--reset",
        action='store_true',
        help="reset to default theme")
    parser.add_argument(
        '-dfonts',
        "--defaultfonts",
        action='store_true',
        default=False,
        help="force fonts to browser default")

    args = parser.parse_args()
    themes = get_themes()
    themes.sort()
    say_themes = "Available Themes: \n   {}".format('\n   '.join(themes))

    if args.reset:
        stylefx.reset_default(verbose=True)
        exit(1)

    elif args.list:
        print(say_themes)
        exit(1)

    elif args.theme is not None:
        if args.theme not in themes:
            print("Didn't recognize theme name: {}".format(args.theme))
            print(say_themes)
            args.theme=None

    install_theme(
        theme=args.theme,
        monofont=args.monofont,
        monosize=args.monosize,
        nbfont=args.nbfont,
        nbfontsize=args.nbfontsize,
        tcfont=args.tcfont,
        tcfontsize=args.tcfontsize,
        dffontsize=args.dffontsize,
        outfontsize=args.outfontsize,
        mathfontsize=args.mathfontsize,
        cellwidth=args.cellwidth,
        margins=args.margins,
        lineheight=int(args.lineheight),
        cursorwidth=args.cursorwidth,
        cursorcolor=args.cursorcolor,
        altprompt=args.altprompt,
        altmd=args.altmarkdown,
        altout=args.altoutput,
        hideprompt=args.hideprompt,
        vimext=args.vimext,
        toolbar=args.toolbar,
        nbname=args.nbname,
        kernellogo=args.kernellogo,
        dfonts=args.defaultfonts)
