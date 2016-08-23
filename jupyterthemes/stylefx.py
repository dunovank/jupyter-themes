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

def send_fonts_to_jupyter(font_file_path):
    fname = font_file_path.split('/')[-1]
    copyfile(font_file_path, os.path.join(jupyter_custom_fonts, fname))

def stored_font_dicts(fontcode, get_all=False):
    fonts = {'mono':
                {'anka': ['Anka/Coder', 'monospace/anka-coder'],
                'anonymous': ['Anonymous Pro', 'monospace/anonymous-pro'],
                'aurulent': ['Aurulent Sans Mono', 'monospace/aurulent'],
                'bitstream': ['Bitstream Vera Sans Mono', 'monospace/bitstream-vera'],
                'bpmono': ['BPmono', 'monospace/bpmono'],
                'code': ['Code New Roman', 'monospace/code-new-roman'],
                'consolamono': ['Consolamono', 'monospace/consolamono'],
                'cousine': ['Cousine', 'monospace/cousine'],
                'dejavu': ['DejaVu Sans Mono', 'monospace/dejavu'],
                'droidmono': ['Droid Sans Mono', 'monospace/droidmono'],
                'fira': ['Fira Mono', 'monospace/fira'],
                'firacode': ['Fira Code', 'monospace/firacode'],
                'generic': ['Generic Mono', 'monospace/generic'],
                'hack': ['Hack', 'monospace/hack'],
                'inconsolata': ['Inconsolata-g', 'monospace/inconsolata-g'],
                'liberation': ['Liberation Mono', 'monospace/liberation'],
                'meslo': ['Meslo', 'monospace/meslo'],
                'office': ['Office Code Pro', 'monospace/office-code-pro'],
                'oxygen': ['Oxygen Mono', 'monospace/oxygen'],
                'roboto': ['Roboto Mono', 'monospace/roboto'],
                'saxmono': ['saxMono', 'monospace/saxmono'],
                'source': ['Source Code Pro', 'monospace/source-code-pro'],
                'sourcemed': ['Source Code Pro Medium', 'monospace/source-code-medium'],
                'ubuntu': ['Ubuntu Mono', 'monospace/ubuntu']},
            'sans':
                {'droidsans': ['Droid Sans', 'sans-serif/droidsans'],
                'opensans': ['Open Sans', 'sans-serif/opensans'],
                'ptsans': ['PT Sans', 'sans-serif/ptsans'],
                'sourcesans': ['Source Sans Pro', 'sans-serif/sourcesans'],
                'robotosans': ['Roboto', 'sans-serif/robotosans'],
                'latosans': ['Lato', 'sans-serif/latosans']},
            'serif':
                {'ptserif': ['PT Serif', 'serif/ptserif'],
                'ebserif': ['EB Garamond', 'serif/ebserif'],
                'loraserif': ['Lora', 'serif/loraserif'],
                'merriserif': ['Merriweather', 'serif/merriserif'],
                'crimsonserif': ['Crimson Text', 'serif/crimsonserif'],
                'droidserif': ['Droid Serif', 'serif/droidserif'],
                'georgiaserif': ['Georgia', 'serif/georgiaserif']}}
    if get_all:
        return fonts
    if fontcode in list(fonts['mono']):
        fontinfo = fonts['mono'][fontcode] + ['monospace']
    elif fontcode in list(fonts['sans']):
        fontinfo = fonts['sans'][fontcode] + ['sans-serif']
    elif fontcode in list(fonts['serif']):
        fontinfo = fonts['serif'][fontcode] + ['serif']
    return fontinfo

def import_stored_fonts(style_less='', fontcodes=['opensans', 'ptserif', 'source']):
    """ collect fontnames and local pointers to fontfiles in custom dir
    then pass information for each font to function for writing import statements
    """
    for fontcode in unique(fontcodes):
        fname, fpath, ffam = stored_font_dicts(fontcode)
        style_less = import_fonts(style_less, fname, fpath)
    return style_less

def convert_fontsizes(fontsizes):
    # if triple digits, move decimal (105 --> 10.5)
    fontsizes = [str(fs) for fs in fontsizes]
    for i, fs in enumerate(fontsizes):
        if len(fs)>=3:
            fontsizes[i] = '.'.join([fs[:-1], fs[-1]])
    return fontsizes

def set_font_properties(nbfont='opensans', tcfont='ptserif', monofont='source', monosize=11, tcfontsize=13, nbfontsize=13):
    """ parent function for setting notebook, text/md, and codecell font-properties
    """
    fontsizes = [monosize, nbfontsize, tcfontsize]
    monosize, nbfontsize, tcfontsize = convert_fontsizes(fontsizes)
    style_less=''
    style_less = import_stored_fonts(style_less, fontcodes=[nbfont, tcfont, monofont])
    nbfont, nbfontpath, nbfontfam = stored_font_dicts(nbfont)
    tcfont, tcfontpath, tcfontfam = stored_font_dicts(tcfont)
    monofont, monofontpath, monofontfam = stored_font_dicts(monofont)
    # font names and fontfamily info for codecells, notebook & textcells
    style_less += '@monofont: "{}"; \n'.format(monofont)
    style_less += '@notebook-fontfamily: "{}", {}; \n'.format(nbfont,nbfontfam)
    style_less += '@text-cell-fontfamily: "{}", {}; \n'.format(tcfont,tcfontfam)
    # font size for codecells, main notebook, notebook-sub, & textcells
    style_less += '@monofontsize: {}pt; \n'.format(monosize)
    style_less += '@nb-fontsize: {}pt; \n'.format(nbfontsize)
    style_less += '@nb-fontsize-sub: {}pt; \n'.format(float(nbfontsize)-1.5)
    style_less += '@text-cell-fontsize: {}pt; \n'.format(tcfontsize)
    return style_less

def import_fonts(style_less, fontname, font_subdir):
    """ copy all custom fonts to ~/.jupyter/custom/fonts/ and
    write import statements to style_less
    """
    ftype_dict = {'woff2':'woff2', 'woff':'woff', 'ttf':'truetype', 'otf':'opentype'}
    define_font = "@font-face {{font-family: '{fontname}';\n\tfont-weight: {weight};\n\tfont-style: {style};\n\tsrc: local('{fontname}'),\n\turl('fonts/{fontfile}') format('{ftype}');}}\n"
    fontpath = os.path.join(fonts_dir, font_subdir)
    for fontfile in os.listdir(fontpath):
        if '.txt' in fontfile:
            continue
        weight = 'normal'
        style = 'normal'
        if 'medium' in fontfile:
            weight='medium'
        elif 'ital' in fontfile:
            style='italic'
        ft = ftype_dict[fontfile.split('.')[-1]]
        style_less += define_font.format(fontname=fontname, weight=weight, style=style, fontfile=fontfile, ftype=ft)
        send_fonts_to_jupyter(os.path.join(fontpath, fontfile))
    return style_less

def style_layout(style_less, theme='grade3', cellwidth=980, lineheight=170, altlayout=False, vimext=False, toolbar=False, nbname=False):
    """ set general layout and style properties of text and code cells
    """
    style_less += '@import "styles/{}";\n'.format(theme)
    style_less += '@cell-width: {}px; \n'.format(cellwidth)
    style_less += '@cc-line-height: {}%; \n'.format(lineheight)
    textcell_bg = '@cc-input-bg'
    tc_prompt_line = '@tc-prompt-std'
    cc_prompt_width = 13
    tc_prompt_width = cc_prompt_width
    if altlayout:
        # alt txt/md layout
        textcell_bg = '@notebook-bg'
        tc_prompt_line = 'transparent'
        tc_prompt_width = 0
    style_less += '@text-cell-bg: {}; \n'.format(textcell_bg)
    style_less += '@cc-prompt-width: {}ex;\n'.format(cc_prompt_width)
    style_less += '@tc-prompt-width: {}ex;\n'.format(tc_prompt_width)
    style_less += '@tc-prompt-line: {};\n'.format(tc_prompt_line)
    # read-in notebook.less (general nb style)
    with open(nb_style, 'r') as notebook:
        style_less += notebook.read() + '\n'
    # read-in cells.less (cell layous)
    with open(cl_style, 'r') as cells:
        style_less += cells.read() + '\n'
    # read-in codemirror.less (syntax-highlighting)
    with open(cm_style, 'r') as codemirror:
        style_less += codemirror.read() + '\n'
    style_less += toggle_settings(toolbar, nbname) +'\n'
    if vimext:
        set_vim_style(theme)
    return style_less

def toggle_settings(toolbar=False, nbname=False):
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
    vim_less = '@import "styles/{}";\n'.format(theme)
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
        custom = '{0}/{1}.css'.format(fpath, 'custom')
        try:
            os.remove(custom)
        except Exception:
            pass
    try:
        for fontfile in os.listdir(jupyter_custom_fonts):
            abspath = os.path.join(jupyter_custom_fonts, fontfile)
            os.remove(abspath)
    except Exception:
        check_directories()
    if verbose:
        print("Reset css and font defaults in:\n{} &\n{}".format(*paths))
