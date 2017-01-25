# jupyterthemes
## Theme-ify your Jupyter Notebooks!

###### *plots & equations*
![image](screens/grade3_plot_example.png)

###### *markdown & text cells*
![image](screens/oceans16_markdown.png)

###### *pandas dataframes*
![image](screens/grade3_table.png)

###### *command palette*
![image](screens/oceans16_command_palette.png)

###### *oceans16 syntax*
![image](screens/oceans16_code_headers.png)

###### *grade3 syntax*
![image](screens/grade3_code_headers.png)

###### *onedork syntax*
![image](screens/onedork_code_headers.png)

###### *chesterish syntax*
![image](screens/chesterish_code_headers.png)

### TravisCI Build status:
![image](https://travis-ci.org/dunovank/jupyter-themes.svg?branch=develop)

### Interactive Binder Demo
[![Binder](http://mybinder.org/badge.svg)](http://mybinder.org:/repo/dunovank/jupyter-themes)

### Links
* [jupyterthemes on PyPI](https://pypi.python.org/pypi/jupyterthemes/)
* [jupyterthemes on GitHub](https://github.com/dunovank/jupyter-themes)

### Requirements
* Python 2.7, 3.3, 3.4, or 3.5
* Jupyter ([Anaconda](https://www.continuum.io/downloads) recommended)

### Recent updates

###### v0.14.1
* fixed linenumbers in onedork theme

###### v0.14.0
* add solarized light theme (added by [svendx4f](https://github.com/svendx4f)
* fixed bug that prevented theme reset
* fixed bug that prevented cursor settings from being applied
* made upload button visible on main page
* other minor thematic adjustments

###### v0.13.9
* minor bug fixes and thematic adjustments

###### v0.13.8
* add monokai theme ([bdell](https://github.com/bdell) : [PR #59](https://github.com/dunovank/jupyter-themes/pull/59))
* apply theme to auto-complete menu ([svendx4f](https://github.com/svendx4f) : [PR #69](https://github.com/dunovank/jupyter-themes/pull/69))
* added support for user less/precompiled themes ([osamaar](https://github.com/osamaar) : [PR #82](https://github.com/dunovank/jupyter-themes/pull/82))


### Install with pip
```sh
pip install jupyterthemes
```

### Command Line Usage
```
usage: jt [-h] [-l] [-t THEME] [-f MONOFONT] [-fs MONOSIZE] [-nf NBFONT]
          [-nfs NBFONTSIZE] [-tf TCFONT] [-tfs TCFONTSIZE] [-m MARGINS]
          [-cursw CURSORWIDTH] [-cursc CURSORCOLOR] [-cellw CELLWIDTH]
          [-lineh LINEHEIGHT] [-alt] [-vim] [-T] [-N] [-r]
```
|        options        |   arg     |     default   |
|:----------------------|:---------:|:-------------:|
| Usage help            |  -h       |      --       |
| List Themes           |  -l       |      --       |
| Theme Name to Install |  -t       |      --       |
| Code Font             |  -f       |   droidmono   |
| Code Font-Size        |  -fs      |      11       |
| Notebook Font         |  -nf      |    exosans    |
| Notebook Font Size    |  -nfs     |      13       |
| Text/MD Cell Font     |  -tf      |   loraserif   |
| Text/MD Cell Fontsize |  -tfs     |      13       |
| Intro Page Margins    |  -m       |     auto      |
| Cell Width            |  -cellw   |      980      |
| Line Height           |  -lineh   |      170      |
| Cursor Width          |  -cursw   |       2       |
| Cursor Color          |  -cursc   |      --       |
| Alt Text/MD Layout    |  -alt     |      --       |
| Alt Prompt Layout     |  -altp    |      --       |
| Style Vim NBExt*      |  -vim     |      --       |
| Toolbar Visible       |  -T       |      --       |
| Name & Logo Visible   |  -N       |      --       |
| Restore Default       |  -r       |      --       |

### Examples
```sh
# list available themes
# oceans16 | grade3 | chesterish | onedork | monokai
jt -l

# select theme...
jt -t chesterish

# restore default theme
# NOTE: Need to delete browser cache after running jt -r
# If this doesn't work, try starting a new notebook session.
jt -r

# toggle toolbar ON and notebook name ON
jt -t grade3 -T -N

# set code font to 'Roboto Mono' 12pt
# (see monospace font table below)
jt -t oceans16 -f roboto -fs 12

# set code font to Fira Mono, 11.5pt
# 3digit font-size gets converted into float (115-->11.5)
jt -t grade3 -f fira -fs 115

# set text-cell/markdown and notebook fonts
# (see sans-serif & serif font tables below)
jt -t onedork -tf georgiaserif -nf droidsans

# adjust cell width, line-height of codecells
jt -t chesterish -cellw 900 -lineh 170

# fix the container-margins on the intro page (defaults to 'auto')
jt -t onedork -m 200

# adjust cursor width (in px) and make cursor red (r)
# options: b (blue), o (orange), r (red), p (purple), g (green)
jt -t grade3 -cursc r -cursw 5

# toggle toolbar ON and notebook name ON
jt -t grade3 -T -N

# choose alternate txt/markdown layout (-alt)
# and alternate cell prompt (narrow, no numbers)
jt -t grade3 -alt -altp
```

### Monospace Fonts (codecells)
| -f arg | Monospace Font |
|:--|:--|
|anka|Anka/Coder|
|anonymous|Anonymous Pro|
|aurulent|Aurulent Sans Mono|
|bitstream|Bitstream Vera Sans Mono|
|bpmono|BPmono|
|code|Code New Roman|
|consolamono|Consolamono|
|cousine|Cousine|
|dejavu|DejaVu Sans Mono|
|droidmono|Droid Sans Mono|
|fira|Fira Mono|
|firacode|Fira Code|
|generic|Generic Mono|
|hack|Hack|
|inconsolata|Inconsolata-g|
|inputmono|Input Mono|
|liberation|Liberation Mono|
|meslo|Meslo|
|office|Office Code Pro|
|oxygen|Oxygen Mono|
|roboto|Roboto Mono|
|saxmono|saxMono|
|source|Source Code Pro|
|sourcemed|Source Code Pro Medium|
|ptmono|PT Mono|
|ubuntu|Ubuntu Mono|

### Sans-Serif Fonts
| -nf/-tf arg | Sans-Serif Font |
|:--|:--|
|exosans|Exo_2|
|opensans|Open Sans|
|droidsans|Droid Sans|
|latosans|Lato|
|ptsans|PT Sans|
|robotosans|Roboto|
|sourcesans|Source Sans Pro|
|amikosans|Amiko|
|nobilesans|Nobile|
|alegreyasans|Alegreya|
|armatasans|Armata|
|cambaysans|Cambay|
|catamaransans|Catamaran|
|franklinsans|Libre Franklin|
|frankruhlsans|Frank Ruhl|
|gothicsans|Carrois Gothic|
|gudeasans|Gudea|
|hindsans|Hind|
|jaldisans|Jaldi|
|makosans|Mako|
|merrisans|Merriweather Sans|
|mondasans|Monda|
|oxygensans|Oxygen Sans|
|pontanosans|Pontano Sans|
|puritansans|Puritan Sans|
|ralewaysans|Raleway|

### Serif Fonts
| -nf/-tf arg | Serif Font |
|:--|:--|
|loraserif|Lora|
|andadaserif|Andada|
|arapeyserif|Arapey|
|ptserif|PT Serif|
|georgiaserif|Georgia|
|cardoserif|Cardo|
|crimsonserif|Crimson Text|
|droidserif|Droid Serif|
|ebserif|EB Garamond|
|merriserif|Merriweather|
|notoserif|Noto Serif|
|vesperserif|Vesper Libre|
|scopeserif|ScopeOne|
|sanchezserif|Sanchez|
|neutonserif|Neuton|
|rasaserif|Rasa|
|goudyserif|Sorts Mill Goudy|
|vollkornserif|Vollkorn|
