import os, sys
import lesscpy
from shutil import copyfile, rmtree
from jupyter_core.paths import jupyter_config_dir, jupyter_data_dir
from glob import glob
from tempfile import mkstemp

# path to local site-packages/jupyterthemes
package_dir = os.path.dirname(os.path.realpath(__file__))

# path to user jupyter-themes dir
user_dir = os.path.join(os.path.expanduser('~'), '.jupyter-themes')

# path to save tempfile with style_less before reading/compiling
_, tempfile = mkstemp('.less')
_, vimtemp = mkstemp('.less')

# path to install custom.css file (~/.jupyter/custom/)
jupyter_home = jupyter_config_dir()
jupyter_data = jupyter_data_dir()

jupyter_custom = os.path.join(jupyter_home, 'custom')
jupyter_custom_fonts = os.path.join(jupyter_custom, 'fonts')
jupyter_customcss = os.path.join(jupyter_custom, 'custom.css')
jupyter_customjs = os.path.join(jupyter_custom, 'custom.js')
jupyter_nbext = os.path.join(jupyter_data, 'nbextensions')

# theme colors, layout, and font directories
layouts_dir = os.path.join(package_dir, 'layout')
styles_dir = os.path.join(package_dir, 'styles')
styles_dir_user = os.path.join(user_dir, 'styles')
fonts_dir = os.path.join(package_dir, 'fonts')
defaults_dir = os.path.join(package_dir, 'defaults')

# default custom.css/js files to override JT on reset
defaultCSS = os.path.join(defaults_dir, 'custom.css')
defaultJS = os.path.join(defaults_dir, 'custom.js')

# layout files for notebook, codemirror, cells, mathjax, & vim ext
nb_style = os.path.join(layouts_dir, 'notebook.less')
cm_style = os.path.join(layouts_dir, 'codemirror.less')
cl_style = os.path.join(layouts_dir, 'cells.less')
ex_style = os.path.join(layouts_dir, 'extras.less')
vim_style = os.path.join(layouts_dir, 'vim.less')
comp_style = os.path.join(layouts_dir, 'completer.less')
theme_name_file = os.path.join(jupyter_custom, 'current_theme.txt')


def fileOpen(filename, mode):
    if sys.version_info[0]==3:
        return open(filename, mode, encoding='utf8', errors='ignore')
    else:
        return open(filename, mode)

def check_directories():
    # Ensure all install dirs exist
    if not os.path.isdir(jupyter_home):
        os.makedirs(jupyter_home)
    if not os.path.isdir(jupyter_custom):
        os.makedirs(jupyter_custom)
    if not os.path.isdir(jupyter_custom_fonts):
        os.makedirs(jupyter_custom_fonts)
    if not os.path.isdir(jupyter_data):
        os.makedirs(jupyter_data)
    if not os.path.isdir(jupyter_nbext):
        os.makedirs(jupyter_nbext)


def less_to_css(style_less):
    """ write less-compiled css file to jupyter_customcss in jupyter_dir
    """
    with fileOpen(tempfile, 'w') as f:
            f.write(style_less)
    os.chdir(package_dir)
    style_css = lesscpy.compile(tempfile)
    style_css += '\n\n'
    return style_css

def write_final_css(style_css):
    # install style_css to .jupyter/custom/custom.css
    with fileOpen(jupyter_customcss, 'w') as custom_css:
        custom_css.write(style_css)


def install_precompiled_theme(theme):
    # for Python 3.5, install selected theme from precompiled defaults
    compiled_dir = os.path.join(styles_dir, 'compiled')
    compiled_dir_user = os.path.join(styles_dir_user, 'compiled')

    if (os.path.isdir(compiled_dir_user) and
            '{}.css'.format(theme) in os.listdir(compiled_dir_user)):
        theme_src = os.path.join(compiled_dir_user, '{}.css'.format(theme))
    else:
        theme_src = os.path.join(compiled_dir, '{}.css'.format(theme))
    theme_dst = os.path.join(jupyter_custom, 'custom.css')
    copyfile(theme_src, theme_dst)

def send_fonts_to_jupyter(font_file_path):
    fname = font_file_path.split(os.sep)[-1]
    copyfile(font_file_path, os.path.join(jupyter_custom_fonts, fname))


def delete_font_files():
    for fontfile in os.listdir(jupyter_custom_fonts):
        abspath = os.path.join(jupyter_custom_fonts, fontfile)
        os.remove(abspath)


def convert_fontsizes(fontsizes):
    # if triple digits, move decimal (105 --> 10.5)
    fontsizes = [str(fs) for fs in fontsizes]
    for i, fs in enumerate(fontsizes):
        if len(fs) >= 3:
            fontsizes[i] = '.'.join([fs[:-1], fs[-1]])
        elif int(fs) > 25:
            fontsizes[i] = '.'.join([fs[0], fs[-1]])
    return fontsizes


def set_font_properties(style_less,
                        nbfont=None,
                        tcfont=None,
                        monofont=None,
                        monosize=11,
                        tcfontsize=13,
                        nbfontsize=13,
                        prfontsize=95,
                        dffontsize=93,
                        outfontsize=85,
                        mathfontsize=100,
                        dfonts=False):
    """Parent function for setting notebook, text/md, and
    codecell font-properties
    """

    fontsizes = [monosize, nbfontsize, tcfontsize, prfontsize, dffontsize, outfontsize]
    monosize, nbfontsize, tcfontsize, prfontsize, dffontsize, outfontsize = convert_fontsizes(fontsizes)
    if dfonts==True:
        monofont, tcfont, nbfont = ['monospace', 'sans-serif', 'sans-serif']
    else:
        if monofont is not None:
            monofont, monofpath = stored_font_dicts(monofont)
            style_less = import_fonts(style_less, monofont, monofpath)
        else:
            monofont='monospace'
        if tcfont is not None:
            tcfont, tcfontpath = stored_font_dicts(tcfont)
            style_less = import_fonts(style_less, tcfont, tcfontpath)
        else:
            tcfont='sans-serif'
        if nbfont is not None:
            if nbfont == 'proxima':
                nbfont, tcfont = ["'Proxima Nova'"]*2
                style_less = proxima_nova_imports(style_less)
            else:
                nbfont, nbfontpath = stored_font_dicts(nbfont)
                style_less = import_fonts(style_less, nbfont, nbfontpath)
        else:
            nbfont='sans-serif'

    style_less += '/* Set Font-Type and Font-Size Variables  */\n'
    # font names and fontfamily info for codecells, notebook & textcells
    style_less += '@monofont: {}; \n'.format(monofont)
    style_less += '@notebook-fontfamily: {}; \n'.format(nbfont)
    style_less += '@text-cell-fontfamily: {}; \n'.format(tcfont)
    # font size for codecells, main notebook, notebook-sub, & textcells
    style_less += '@monofontsize: {}pt; \n'.format(monosize)
    style_less += '@monofontsize-sub: {}pt; \n'.format(float(monosize) - 1)
    style_less += '@nb-fontsize: {}pt; \n'.format(nbfontsize)
    style_less += '@nb-fontsize-sub: {}pt; \n'.format(float(nbfontsize) - 1)
    style_less += '@text-cell-fontsize: {}pt; \n'.format(tcfontsize)
    style_less += '@df-header-fontsize: {}pt; \n'.format(float(dffontsize) + 1)
    style_less += '@df-fontsize: {}pt; \n'.format(dffontsize)
    style_less += '@output-font-size: {}pt; \n'.format(outfontsize)
    style_less += '@prompt-fontsize: {}pt; \n'.format(prfontsize)
    style_less += '@mathfontsize: {}%; \n'.format(mathfontsize)
    style_less += '\n\n'
    style_less += '/* Import Theme Colors and Define Layout Variables */\n'
    return style_less


def import_fonts(style_less, fontname, font_subdir):
    """Copy all custom fonts to ~/.jupyter/custom/fonts/ and
    write import statements to style_less
    """

    ftype_dict = {'woff2': 'woff2',
                  'woff': 'woff',
                  'ttf': 'truetype',
                  'otf': 'opentype',
                  'svg': 'svg'}

    define_font = (
        "@font-face {{font-family: {fontname};\n\tfont-weight:"
        "{weight};\n\tfont-style: {style};\n\tsrc: local('{fontname}'),"
        "\n\turl('fonts{sepp}{fontfile}') format('{ftype}');}}\n")
    fontname = fontname.split(',')[0]
    fontpath = os.path.join(fonts_dir, font_subdir)
    for fontfile in os.listdir(fontpath):
        if '.txt' in fontfile or 'DS_' in fontfile:
            continue
        weight = 'normal'
        style = 'normal'
        if 'medium' in fontfile:
            weight = 'medium'
        elif 'ital' in fontfile:
            style = 'italic'
        ft = ftype_dict[fontfile.split('.')[-1]]
        style_less += define_font.format(
            fontname=fontname,
            weight=weight,
            style=style,
            sepp='/',
            fontfile=fontfile,
            ftype=ft)
        send_fonts_to_jupyter(os.path.join(fontpath, fontfile))

    return style_less


def style_layout(style_less,
                 theme='grade3',
                 cursorwidth=2,
                 cursorcolor='default',
                 cellwidth='980',
                 lineheight=170,
                 margins='auto',
                 vimext=False,
                 toolbar=False,
                 nbname=False,
                 kernellogo=False,
                 altprompt=False,
                 altmd=False,
                 altout=False,
                 hideprompt=False):
    """Set general layout and style properties of text and code cells"""

    # write theme name to ~/.jupyter/custom/ (referenced by jtplot.py)
    with fileOpen(theme_name_file, 'w') as f:
        f.write(theme)

    if (os.path.isdir(styles_dir_user) and
            '{}.less'.format(theme) in os.listdir(styles_dir_user)):
        theme_relpath = os.path.relpath(
            os.path.join(styles_dir_user, theme), package_dir)
    else:
        theme_relpath = os.path.relpath(
            os.path.join(styles_dir, theme), package_dir)

    style_less += '@import "{}";\n'.format(theme_relpath)

    textcell_bg = '@cc-input-bg'
    promptText = '@input-prompt'
    promptBG = '@cc-input-bg'
    promptPadding = '.25em'
    promptBorder = '2px solid @prompt-line'
    tcPromptBorder = '2px solid @tc-prompt-std'
    promptMinWidth = 11.5
    outpromptMinWidth = promptMinWidth # remove + 3 since it will overlay output print() text
    tcPromptWidth = promptMinWidth + 3
    tcPromptFontsize = "@prompt-fontsize"
    ccOutputBG = '@cc-output-bg-default'

    if theme == 'grade3':
        textcell_bg = '@notebook-bg'
    if altprompt:
        promptPadding = '.1em'
        promptMinWidth = 8
        outpromptMinWidth = promptMinWidth + 3
        tcPromptWidth = promptMinWidth + 3
        promptText = 'transparent'
        tcPromptBorder = '2px solid transparent'
    if altmd:
        textcell_bg = '@notebook-bg'
        tcPromptBorder = '2px dotted @tc-border-selected'
    if altout:
        ccOutputBG = '@notebook-bg'
    if margins != 'auto':
        margins = '{}px'.format(margins)
    if '%' not in cellwidth:
        cellwidth = str(cellwidth) + 'px'

    style_less += '@container-margins: {};\n'.format(margins)
    style_less += '@cell-width: {}; \n'.format(cellwidth)
    style_less += '@cc-line-height: {}%; \n'.format(lineheight)
    style_less += '@text-cell-bg: {}; \n'.format(textcell_bg)
    style_less += '@cc-prompt-width: {}ex; \n'.format(promptMinWidth)
    style_less += '@cc-prompt-bg: {}; \n'.format(promptBG)
    style_less += '@cc-output-bg: {}; \n'.format(ccOutputBG)
    style_less += '@prompt-text: {}; \n'.format(promptText)
    style_less += '@prompt-padding: {}; \n'.format(promptPadding)
    style_less += '@prompt-border: {}; \n'.format(promptBorder)
    style_less += '@prompt-min-width: {}ex; \n'.format(promptMinWidth)
    style_less += '@out-prompt-min-width: {}ex; \n'.format(outpromptMinWidth)
    style_less += '@tc-prompt-width: {}ex; \n'.format(tcPromptWidth)
    style_less += '@tc-prompt-border: {}; \n'.format(tcPromptBorder)
    style_less += '@cursor-width: {}px; \n'.format(cursorwidth)
    style_less += '@cursor-info: @cursor-width solid {}; \n'.format(
        cursorcolor)
    style_less += '@tc-prompt-fontsize: {}; \n'.format(tcPromptFontsize)
    style_less += '\n\n'

    # read-in notebook.less (general nb style)
    with fileOpen(nb_style, 'r') as notebook:
        style_less += notebook.read() + '\n'

    # read-in cells.less (cell layout)
    with fileOpen(cl_style, 'r') as cells:
        style_less += cells.read() + '\n'

    # read-in extras.less (misc layout)
    with fileOpen(ex_style, 'r') as extras:
        style_less += extras.read() + '\n'

    # read-in codemirror.less (syntax-highlighting)
    with fileOpen(cm_style, 'r') as codemirror:
        style_less += codemirror.read() + '\n'
    with fileOpen(comp_style, 'r') as codemirror:
        style_less += codemirror.read() + '\n'

    style_less += toggle_settings(
        toolbar, nbname, hideprompt, kernellogo) + '\n'
    if vimext:
        set_vim_style(theme)

    return style_less


def toggle_settings(
        toolbar=False, nbname=False, hideprompt=False, kernellogo=False):
    """Toggle main notebook toolbar (e.g., buttons), filename,
    and kernel logo."""

    toggle = ''
    if toolbar:
        toggle += 'div#maintoolbar {margin-left: 8px !important;}\n'
        toggle += '.toolbar.container {width: 100% !important;}\n'
    else:
        toggle += 'div#maintoolbar {display: none !important;}\n'
    if nbname:
        toggle += ('span.save_widget span.filename {margin-left: 8px; height: initial;'
                   'font-size: 100%; color: @nb-name-fg; background-color:'
                   '@cc-input-bg;}\n')
        toggle += ('span.save_widget span.filename:hover {color:'
                   '@nb-name-hover; background-color: @cc-input-bg;}\n')
        toggle += ('#menubar {padding-top: 4px; background-color:'
                   '@notebook-bg;}\n')
    else:
        toggle += '#header-container {display: none !important;}\n'
    if hideprompt:
        toggle += 'div.prompt.input_prompt {display: none !important;}\n'
        toggle += 'div.prompt.output_prompt {width: 5ex !important;}\n'
        toggle += 'div.out_prompt_overlay.prompt:hover {width: 5ex !important; min-width: 5ex !important;}\n'
        toggle += (
            '.CodeMirror-gutters, .cm-s-ipython .CodeMirror-gutters'
            '{ position: absolute; left: 0; top: 0; z-index: 3; width: 2em; '
            'display: inline-block !important; }\n')
        toggle += ('div.cell.code_cell .input { border-left: 5px solid @cm-gutters !important; border-bottom-left-radius: 5px; border-top-left-radius: 5px; }\n')
    if kernellogo:
        toggle += '@kernel-logo-display: block;'
    else:
        toggle += '@kernel-logo-display: none;'

    return toggle


def proxima_nova_imports(style_less):

    style_less += """@font-face {
        font-family: 'Proxima Nova Bold';
        src: url('fonts/Proxima Nova Alt Bold-webfont.eot');
        src: url('fonts/Proxima Nova Alt Bold-webfont.eot?#iefix') format('embedded-opentype'),
             url('fonts/Proxima Nova Alt Bold-webfont.woff2') format('woff2'),
             url('fonts/Proxima Nova Alt Bold-webfont.woff') format('woff'),
             url('fonts/Proxima Nova Alt Bold-webfont.ttf') format('truetype'),
             url('fonts/Proxima Nova Alt Bold-webfont.svg#proxima_nova_altbold') format('svg');
        font-weight: 600;
        font-style: normal;
    }

    @font-face {
        font-family: 'Proxima Nova';
        src: url('fonts/Proxima Nova Alt Regular-webfont.eot');
        src: url('fonts/Proxima Nova Alt Regular-webfont.eot?#iefix') format('embedded-opentype'),
             url('fonts/Proxima Nova Alt Regular-webfont.woff') format('woff'),
             url('fonts/Proxima Nova Alt Regular-webfont.ttf') format('truetype'),
             url('fonts/Proxima Nova Alt Regular-webfont.svg#proxima_nova_altregular') format('svg');
        font-weight: 400;
        font-style: normal;
    }"""

    font_subdir = os.path.join(fonts_dir, "sans-serif/proximasans")
    fontpath = os.path.join(fonts_dir, font_subdir)
    for fontfile in os.listdir(font_subdir):
        send_fonts_to_jupyter(os.path.join(fontpath, fontfile))

    return style_less


def set_mathjax_style(style_css, mathfontsize):
    """Write mathjax settings, set math fontsize
    """

    jax_style = """<script>
    MathJax.Hub.Config({
        "HTML-CSS": {
            /*preferredFont: "TeX",*/
            /*availableFonts: ["TeX", "STIX"],*/
            styles: {
                scale: %d,
                ".MathJax_Display": {
                    "font-size": %s,
                }
            }
        }
    });\n</script>
    """ % (int(mathfontsize), '"{}%"'.format(str(mathfontsize)))

    style_css += jax_style
    return style_css



def set_vim_style(theme):
    """Add style and compatibility with vim notebook extension"""

    vim_jupyter_nbext = os.path.join(jupyter_nbext, 'vim_binding')

    if not os.path.isdir(vim_jupyter_nbext):
        os.makedirs(vim_jupyter_nbext)

    vim_less = '@import "styles{}";\n'.format(''.join([os.sep, theme]))

    with open(vim_style, 'r') as vimstyle:
        vim_less += vimstyle.read() + '\n'
    with open(vimtemp, 'w') as vtemp:
        vtemp.write(vim_less)
    os.chdir(package_dir)
    vim_css = lesscpy.compile(vimtemp)
    vim_css += '\n\n'

    # install vim_custom_css to ...nbextensions/vim_binding/vim_binding.css
    vim_custom_css = os.path.join(vim_jupyter_nbext, 'vim_binding.css')
    with open(vim_custom_css, 'w') as vim_custom:
        vim_custom.write(vim_css)


def reset_default(verbose=False):
    """Remove custom.css and custom fonts"""
    paths = [jupyter_custom, jupyter_nbext]

    for fpath in paths:
        custom = '{0}{1}{2}.css'.format(fpath, os.sep, 'custom')
        try:
            os.remove(custom)
        except Exception:
            pass
    try:
        delete_font_files()
    except Exception:
        check_directories()
        delete_font_files()

    copyfile(defaultCSS, jupyter_customcss)
    copyfile(defaultJS, jupyter_customjs)

    if os.path.exists(theme_name_file):
        os.remove(theme_name_file)

    if verbose:
        print("Reset css and font defaults in:\n{} &\n{}".format(*paths))


def set_nb_theme(name):
    """Set theme from within notebook """
    from IPython.core.display import HTML
    styles_dir = os.path.join(package_dir, 'styles/compiled/')
    css_path = glob('{0}/{1}.css'.format(styles_dir, name))[0]
    customcss = open(css_path, "r").read()

    return HTML(''.join(['<style> ', customcss, ' </style>']))


def get_colors(theme='grade3', c='default', get_dict=False):
    if theme == 'grade3':
        cdict = {'default': '#ff711a',
                 'b': '#1e70c7',
                 'o': '#ff711a',
                 'r': '#e22978',
                 'p': '#AA22FF',
                 'g': '#2ecc71'}
    else:
        cdict = {'default': '#0095ff',
                 'b': '#0095ff',
                 'o': '#ff914d',
                 'r': '#DB797C',
                 'p': '#c776df',
                 'g': '#94c273'}

    cdict['x'] = '@cc-input-fg'

    if get_dict:
        return cdict

    return cdict[c]


def get_alt_prompt_text_color(theme):
    altColors = {'grade3': '#FF7823',
                 'oceans16': '#667FB1',
                 'chesterish': '#0b98c8',
                 'onedork': '#94c273',
                 'monokai': '#94c273'}

    return altColors[theme]


def stored_font_dicts(fontcode, get_all=False):
    fonts = {'mono':
             {'anka': ['Anka/Coder', 'anka-coder'],
              'anonymous': ['Anonymous Pro', 'anonymous-pro'],
              'aurulent': ['Aurulent Sans Mono', 'aurulent'],
              'bitstream': ['Bitstream Vera Sans Mono', 'bitstream-vera'],
              'bpmono': ['BPmono', 'bpmono'],
              'code': ['Code New Roman', 'code-new-roman'],
              'consolamono': ['Consolamono', 'consolamono'],
              'cousine': ['Cousine', 'cousine'],
              'dejavu': ['DejaVu Sans Mono', 'dejavu'],
              'droidmono': ['Droid Sans Mono', 'droidmono'],
              'fira': ['Fira Mono', 'fira'],
              'firacode': ['Fira Code', 'firacode'],
              'generic': ['Generic Mono', 'generic'],
              'hack': ['Hack', 'hack'],
              'hasklig': ['Hasklig', 'hasklig'],
              'iosevka' : ['Iosevka', 'iosevka'],
              'inputmono': ['Input Mono', 'inputmono'],
              'inconsolata': ['Inconsolata-g', 'inconsolata-g'],
              'liberation': ['Liberation Mono', 'liberation'],
              'meslo': ['Meslo', 'meslo'],
              'office': ['Office Code Pro', 'office-code-pro'],
              'oxygen': ['Oxygen Mono', 'oxygen'],
              'roboto': ['Roboto Mono', 'roboto'],
              'saxmono': ['saxMono', 'saxmono'],
              'source': ['Source Code Pro', 'source-code-pro'],
              'sourcemed': ['Source Code Pro Medium', 'source-code-medium'],
              'ptmono': ['PT Mono', 'ptmono'],
              'ubuntu': ['Ubuntu Mono', 'ubuntu']},
             'sans':
             {'droidsans': ['Droid Sans', 'droidsans'],
              'opensans': ['Open Sans', 'opensans'],
              'ptsans': ['PT Sans', 'ptsans'],
              'sourcesans': ['Source Sans Pro', 'sourcesans'],
              'robotosans': ['Roboto', 'robotosans'],
              'latosans': ['Lato', 'latosans'],
              'exosans': ['Exo_2', 'exosans'],
              'proxima': ['Proxima Nova', 'proximasans']},
             'serif':
             {'ptserif': ['PT Serif', 'ptserif'],
              'ebserif': ['EB Garamond', 'ebserif'],
              'loraserif': ['Lora', 'loraserif'],
              'merriserif': ['Merriweather', 'merriserif'],
              'crimsonserif': ['Crimson Text', 'crimsonserif'],
              'georgiaserif': ['Georgia', 'georgiaserif'],
              'neutonserif': ['Neuton', 'neutonserif'],
              'cardoserif': ['Cardo Serif', 'cardoserif'],
              'goudyserif': ['Goudy Serif', 'goudyserif']}}
    if get_all:
        return fonts
    if fontcode in list(fonts['mono']):
        fontname, fontdir = fonts['mono'][fontcode]
        fontfam = 'monospace'
    elif fontcode in list(fonts['sans']):
        fontname, fontdir = fonts['sans'][fontcode]
        fontfam = 'sans-serif'
    elif fontcode in list(fonts['serif']):
        fontname, fontdir = fonts['serif'][fontcode]
        fontfam = 'serif'
    else:
        print("\n\tOne of the fonts you requested is not available\n\tSetting all fonts to default")
        return ''
    fontdir = os.sep.join([fontfam, fontdir])
    return '"{}", {}'.format(fontname, fontfam), fontdir
