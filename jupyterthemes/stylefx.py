from __future__ import print_function
import os, sys
from jupyter_core.paths import jupyter_config_dir, jupyter_data_dir
from shutil import copyfile, rmtree
from numpy import unique
import lesscpy

# path to local site-packages/jupyterthemes
package_dir = os.path.dirname(os.path.realpath(__file__))

# path to save tempfile with style_less before reading/compiling
tempfile = os.path.join(package_dir, 'tempfile.less')
vimtemp = os.path.join(package_dir, 'vimtemp.less')

# path to install custom.css file (~/.jupyter/custom/)
jupyter_home = jupyter_config_dir()
jupyter_data = jupyter_data_dir()

jupyter_custom = os.path.join(jupyter_home, 'custom')
jupyter_custom_fonts = os.path.join(jupyter_custom, 'fonts')
jupyter_customcss = os.path.join(jupyter_custom, 'custom.css')
jupyter_nbext = os.path.join(jupyter_data, 'nbextensions')

# theme colors, layout, and font directories
layouts_dir = os.path.join(package_dir, 'layout')
styles_dir = os.path.join(package_dir, 'styles')
fonts_dir = os.path.join(package_dir, 'fonts')

# layout files for notebook, codemirror, cells, mathjax, & vim ext
nb_style = os.path.join(layouts_dir, 'notebook.less')
cm_style = os.path.join(layouts_dir, 'codemirror.less')
cl_style = os.path.join(layouts_dir, 'cells.less')
ex_style = os.path.join(layouts_dir, 'extras.less')
jax_style = os.path.join(layouts_dir, 'mathjax.css')
vim_style = os.path.join(layouts_dir, 'vim.less')

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
    with open(tempfile, 'w') as f:
        f.write(style_less)
    os.chdir(package_dir)
    style_css = lesscpy.compile(tempfile)
    style_css += '\n\n'
    return style_css

def write_final_css(style_css):
    # install style_css to .jupyter/custom/custom.css
    with open(jupyter_customcss, 'w') as custom_css:
        custom_css.write(style_css)

def remove_temp_files(vimext=False):
    # remove tempfile.less from package_dir
    os.remove(tempfile)
    if vimext:
        os.remove(vimtemp)

def install_precompiled_theme(theme):
    # for Python 3.5, install selected theme from precompiled defaults
    compiled_dir = os.path.join(styles_dir, 'compiled')
    theme_src = os.path.join(compiled_dir, '{}.css'.format(theme))
    theme_dst = os.path.join(jupyter_custom, 'custom.css')
    copyfile(theme_src, theme_dst)
    for fontcode in ['exosans', 'loraserif', 'droidmono', 'firacode']:
        fname, fpath, ffam = stored_font_dicts(fontcode)
        fontpath = os.path.join(fonts_dir, fpath)
        for fontfile in os.listdir(fontpath):
            send_fonts_to_jupyter(os.path.join(fontpath, fontfile))

def send_fonts_to_jupyter(font_file_path):
    fname = font_file_path.split(os.sep)[-1]
    copyfile(font_file_path, os.path.join(jupyter_custom_fonts, fname))

def delete_font_files():
    for fontfile in os.listdir(jupyter_custom_fonts):
        abspath = os.path.join(jupyter_custom_fonts, fontfile)
        os.remove(abspath)

def import_stored_fonts(fontcodes=['exosans', 'loraserif', 'droidmono']):
    """ collect fontnames and local pointers to fontfiles in custom dir
    then pass information for each font to function for writing import statements
    """
    doc ='\nConcatenated font imports, .less styles, & custom variables\n'
    s = '*'*65
    style_less = '\n'.join(['/*', s, s, doc, s, s, '*/'])
    style_less += '\n\n\n'
    style_less += '/* Import Notebook, Markdown, & Code Fonts */\n'
    for fontcode in unique(fontcodes):
        fname, fpath, ffam = stored_font_dicts(fontcode)
        style_less = import_fonts(style_less, fname, fpath)
    style_less += '\n\n'
    return style_less

def convert_fontsizes(fontsizes):
    # if triple digits, move decimal (105 --> 10.5)
    fontsizes = [str(fs) for fs in fontsizes]
    for i, fs in enumerate(fontsizes):
        if len(fs)>=3:
            fontsizes[i] = '.'.join([fs[:-1], fs[-1]])
        elif int(fs)>50:
            fontsizes[i] = '.'.join([fs[0], fs[-1]])
    return fontsizes

def set_font_properties(nbfont='exosans', tcfont='loraserif', monofont='droidmono', monosize=11, tcfontsize=13, nbfontsize=13, prfontsize=95):
    """ parent function for setting notebook, text/md, and codecell font-properties
    """
    fontsizes = [monosize, nbfontsize, tcfontsize, prfontsize]
    monosize, nbfontsize, tcfontsize, prfontsize = convert_fontsizes(fontsizes)
    style_less = import_stored_fonts(fontcodes=[nbfont, tcfont, monofont, 'firacode'])
    style_less += '/* Set Font-Type and Font-Size Variables  */\n'
    # get fontname, fontpath, font-family info
    nbfont, nbfontpath, nbfontfam = stored_font_dicts(nbfont)
    tcfont, tcfontpath, tcfontfam = stored_font_dicts(tcfont)
    monofont, monofontpath, monofontfam = stored_font_dicts(monofont)
    # font names and fontfamily info for codecells, notebook & textcells
    style_less += '@monofont: "{}"; \n'.format(monofont)
    style_less += '@notebook-fontfamily: "{}", {}; \n'.format(nbfont, nbfontfam)
    style_less += '@text-cell-fontfamily: "{}", {}; \n'.format(tcfont, tcfontfam)
    # font size for codecells, main notebook, notebook-sub, & textcells
    style_less += '@monofontsize: {}pt; \n'.format(monosize)
    style_less += '@monofontsize-sub: {}pt; \n'.format(float(monosize)-1)
    style_less += '@nb-fontsize: {}pt; \n'.format(nbfontsize)
    style_less += '@nb-fontsize-sub: {}pt; \n'.format(float(nbfontsize)-1)
    style_less += '@text-cell-fontsize: {}pt; \n'.format(tcfontsize)
    style_less += '@prompt-fontsize: {}pt; \n'.format(prfontsize)
    style_less += '\n\n'
    style_less += '/* Import Theme Colors and Define Layout Variables */\n'
    return style_less

def import_fonts(style_less, fontname, font_subdir):
    """ copy all custom fonts to ~/.jupyter/custom/fonts/ and
    write import statements to style_less
    """
    ftype_dict = {'woff2':'woff2', 'woff':'woff', 'ttf':'truetype', 'otf':'opentype'}
    define_font = "@font-face {{font-family: '{fontname}';\n\tfont-weight: {weight};\n\tfont-style: {style};\n\tsrc: local('{fontname}'),\n\turl('fonts{sepp}{fontfile}') format('{ftype}');}}\n"
    fontpath = os.path.join(fonts_dir, font_subdir)
    for fontfile in os.listdir(fontpath):
        if '.txt' in fontfile or 'DS_' in fontfile:
            continue
        weight = 'normal'
        style = 'normal'
        if 'medium' in fontfile:
            weight='medium'
        elif 'ital' in fontfile:
            style='italic'
        ft = ftype_dict[fontfile.split('.')[-1]]
        style_less += define_font.format(fontname=fontname, weight=weight, style=style, sepp=os.sep, fontfile=fontfile, ftype=ft)
        send_fonts_to_jupyter(os.path.join(fontpath, fontfile))

    return style_less

def style_layout(style_less, theme='grade3', cursorwidth=2, cursorcolor='default', cellwidth=980, lineheight=170, margins='auto', altlayout=False, vimext=False, toolbar=False, nbname=False, altprompt=False, hideprompt=False):
    """ set general layout and style properties of text and code cells
    """
    style_less += '@import "styles{}";\n'.format(''.join([os.sep, theme]))
    textcell_bg = '@cc-input-bg'
    promptText = '@input-prompt'
    promptBG = '@cc-input-bg'
    promptPadding = '.25em'
    promptBorder = '2px solid @prompt-line'
    tcPromptBorder = '@tc-prompt-std'
    promptMinWidth = 12
    tcPromptWidth = promptMinWidth
    if altprompt:
        promptPadding = '.1em'
        #promptBorder = '2px solid transparent'
        tcPromptBorder = promptBorder
        promptMinWidth = 8
        tcPromptWidth = promptMinWidth
        promptText = 'transparent' #get_alt_prompt_text_color(theme)
    if altlayout:
        # alt txt/md layout
        textcell_bg = '@notebook-bg'
        tcPromptBorder = '2px solid transparent'
        tcPromptWidth = 0
    if margins!='auto':
        margins = '{}px'.format(margins)
    style_less += '@container-margins: {};\n'.format(margins)
    style_less += '@cell-width: {}px; \n'.format(cellwidth)
    style_less += '@cc-line-height: {}%; \n'.format(lineheight)
    style_less += '@text-cell-bg: {}; \n'.format(textcell_bg)
    style_less += '@cc-prompt-width: {}ex; \n'.format(promptMinWidth)
    style_less += '@cc-prompt-bg: {}; \n'.format(promptBG)
    style_less += '@prompt-text: {}; \n'.format(promptText)
    style_less += '@prompt-padding: {}; \n'.format(promptPadding)
    style_less += '@prompt-border: {}; \n'.format(promptBorder)
    style_less += '@prompt-min-width: {}ex; \n'.format(promptMinWidth)
    style_less += '@tc-prompt-border: {}; \n'.format(tcPromptBorder)
    style_less += '@tc-prompt-width: {}ex; \n'.format(tcPromptWidth)
    style_less += '@cursor-width: {}px; \n'.format(cursorwidth)
    style_less += '@cursor-info: @cursor-width solid {}; \n'.format(cursorcolor)
    style_less += '\n\n'
    # read-in notebook.less (general nb style)
    with open(nb_style, 'r') as notebook:
        style_less += notebook.read() + '\n'
    # read-in cells.less (cell layout)
    with open(cl_style, 'r') as cells:
        style_less += cells.read() + '\n'
    # read-in extras.less (misc layout)
    with open(ex_style, 'r') as extras:
        style_less += extras.read() + '\n'
    # read-in codemirror.less (syntax-highlighting)
    with open(cm_style, 'r') as codemirror:
        style_less += codemirror.read() + '\n'
    style_less += toggle_settings(toolbar, nbname, hideprompt) +'\n'

    if vimext:
        set_vim_style(theme)
    return style_less

def toggle_settings(toolbar=False, nbname=False, hideprompt=False):
    """ toggle main notebook toolbar (e.g., buttons) & filename
    """
    toggle = ''
    if toolbar:
        toggle += 'div#maintoolbar {margin-left: 8px !important;}\n'
    else:
        toggle += 'div#maintoolbar {display: none !important;}\n'
    if nbname:
        toggle += 'span.save_widget span.filename {margin-left: 8px; font-size: 120%; color: @nb-name-fg; background-color: @cc-input-bg;}\n'
        toggle += 'span.save_widget span.filename:hover {color: @nb-name-hover; background-color: @cc-input-bg;}\n'
        toggle +='#menubar {padding-top: 4px; background-color: @notebook-bg;}\n'
    else:
        toggle += '#header-container {display: none !important;}\n'
    if hideprompt:
        toggle += 'div.prompt {display: none !important;}\n'
        toggle += '.CodeMirror-gutters, .cm-s-ipython .CodeMirror-gutters { position: absolute; left: 0; top: 0; z-index: 3; width: 2em; display: inline-block !important; }'
    return toggle

def set_mathjax_style(style_css):
    """ improve mathjax fonttype setting in markdown cells
    """
    # append mathjax css & script to style_css
    with open(jax_style, 'r') as mathjax:
        style_css += mathjax.read() + '\n'
    return style_css

def set_vim_style(theme):
    """ add style and compatibility with vim notebook extension
    """
    vim_jupyter_nbext = os.path.join(jupyter_nbext, 'vim_binding')
    if not os.path.isdir(vim_jupyter_nbext):
        os.makedirs(vim_jupyter_nbext)
    vim_less = '@import "styles{}";\n'.format(''.join([os.sep, theme]))
    with open(vim_style, 'r') as vimstyle:
        vim_less += vimstyle.read() + '\n'
    with open(vimtemp, 'w') as f:
        f.write(vim_less)
    os.chdir(package_dir)
    vim_css = lesscpy.compile(vimtemp)
    vim_css += '\n\n'
    # install vim_custom_css to ...nbextensions/vim_binding/vim_binding.css
    vim_custom_css = os.path.join(vim_jupyter_nbext, 'vim_binding.css')
    with open(vim_custom_css, 'w') as vim_custom:
        vim_custom.write(vim_css)
    os.remove(vimtemp)

def reset_default(verbose=False):
    """ remove custom.css and custom fonts
    """
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
    if verbose:
        print("Reset css and font defaults in:\n{} &\n{}".format(*paths))

def set_nb_theme(name):
    """ set theme from within notebook """
    from IPython.core.display import HTML
    from glob import glob
    styles_dir = os.path.join(package_dir, 'styles/compiled/')
    css_path = glob('{0}/{1}.css'.format(styles_dir, name))[0]
    customcss = open(css_path, "r").read()
    return HTML(''.join(['<style> ', customcss, ' </style>']))

def get_colors(theme='grade3', c='default', get_dict=False):
    if theme=='grade3':
        cdict = {'b': '#1e70c7', 'default': '#ff711a', 'o': '#ff711a', 'r': '#e22978', 'p': '#AA22FF', 'g': '#2ecc71'}
    else:
        cdict = {'default': '#0095ff', 'b': '#0095ff', 'o': '#ff914d', 'r': '#DB797C', 'p': '#c776df', 'g': '#94c273'}
    if get_dict:
        return cdict
    return cdict[c]

def get_alt_prompt_text_color(theme):
    altColors = {'grade3':'#FF7823', 'oceans16':'#667FB1', 'chesterish':'#0b98c8', 'onedork':'#94c273'}
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
                'amikosans': ['Amiko', 'amikosans'],
                'exosans': ['Exo_2', 'exosans'],
                'nobilesans': ['Nobile', 'nobilesans'],
                'alegreyasans': ['Alegreya', 'alegreyasans'],
                'armatasans': ['Armata', 'armatasans'],
                'cambaysans': ['Cambay', 'cambaysans'],
                'catamaransans': ['Catamaran', 'catamaransans'],
                'franklinsans': ['Libre Franklin', 'franklinsans'],
                'frankruhlsans': ['Frank Ruhl', 'frankruhlsans'],
                'gothicsans': ['Carrois Gothic', 'gothicsans'],
                'gudeasans': ['Gudea', 'gudeasans'],
                'hindsans': ['Hind', 'hindsans'],
                'jaldisans': ['Jaldi', 'jaldisans'],
                'makosans': ['Mako', 'makosans'],
                'merrisans': ['Merriweather Sans', 'merrisans'],
                'mondasans': ['Monda', 'mondasans'],
                'oxygensans': ['Oxygen Sans', 'oxygensans'],
                'pontanosans': ['Pontano Sans', 'pontanosans'],
                'puritansans': ['Puritan Sans', 'puritansans'],
                'ralewaysans': ['Raleway', 'ralewaysans']},
            'serif':
                {'ptserif': ['PT Serif', 'ptserif'],
                'ebserif': ['EB Garamond', 'ebserif'],
                'loraserif': ['Lora', 'loraserif'],
                'merriserif': ['Merriweather', 'merriserif'],
                'crimsonserif': ['Crimson Text', 'crimsonserif'],
                'droidserif': ['Droid Serif', 'droidserif'],
                'georgiaserif': ['Georgia', 'georgiaserif'],
                'neutonserif': ['Neuton', 'neutonserif'],
                'vesperserif': ['Vesper Libre', 'vesperserif'],
                'scopeserif': ['ScopeOne Serif', 'scopeserif'],
                'sanchezserif': ['Sanchez Serif', 'sanchezserif'],
                'rasaserif': ['Rasa', 'rasaserif'],
                'vollkornserif': ['Vollkorn', 'vollkornserif'],
                'cardoserif': ['Cardo Serif', 'cardoserif'],
                'notoserif': ['Noto Serif', 'notoserif'],
                'goudyserif': ['Goudy Serif', 'goudyserif'],
                'andadaserif': ['Andada Serif', 'andadaserif'],
                'arapeyserif': ['Arapey Serif', 'arapeyserif']}}
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
        "One of the fonts you requested is not available... sorry!"
        return _
    fontdir = os.sep.join([fontfam, fontdir])
    return fontname, fontdir, fontfam
