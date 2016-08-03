# jupyterthemes
## Theme-ify your Jupyter Notebooks!

```sh
jt -t chesterish -cw 850 -fs 10
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-tchesterish-cw850-fs10.png?raw=true)

```sh
jt -t oceans16 -alt -fs 10 -cw 900
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-toceans16-altmd-fs10-cw900.png?raw=true)

```sh
jt -t onedork -fs 10 -cw 850
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-tonedork-cw850-fs10.png?raw=true)

```sh
jt -t grade3 -alt -fs 10 -cw 900 -tcff serif
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-tgrade3-altmd-fs10-cw900.png?raw=true)

```sh
jt -t onedork -nbff serif -tcff serif
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-tonedork-ffserif-tcffserif.png?raw=true)



# Install with pip
```sh
pip install jupyterthemes
```

## How To...

```
usage: jt [-l] [-t THEME] [-f MONOFONT] [-fs MONOSIZE ] [-nbff NBFONTFAM]  
        [-tcff TCFONTFAM] [-cw CELLWIDTH] [-lh LINEHEIGHT] [-alt] [-T]  [-r ]
```

|        options        |   arg     |     default    |
|:----------------------|:---------:|:--------------:|
| List Themes           |  -l       |       --       |
| Select Theme          |  -t       |       --       |
| Code Font             |  -f       |      Hack      |
| Code Font-Size        |  -fs      |       11       |
| NB Font-Family        |  -nbff    |   sans-serif   |
| TxtCell Font-Family   |  -tcff    |   sans-serif   |
| Cell Width            |  -cw      |      940       |
| Line Height           |  -lh      |      160       |
| Alt Txt/MD Layout     |  -alt     |       --       |
| Toolbar Visible       |  -T       |       --       |
| Notebook Name Visible |  -N       |       --       |
| Jupyter Logo Visible  |  -L       |       --       |
| Restore Default       |  -r       |       --       |

## Importable Code Fonts from Google Fonts API

|    Font-Name     |    -f       |     comments     |
|:-----------------|:-----------:|:----------------:|     
|     Hack         |    --       |     italics      |
|  Roboto Mono     |  roboto     |     italics      |
|  Space Mono      |  space      |     italics      |         
|  Anonymous Pro   |  anon       |     italics      |
|  Cousine         |  cousine    |     italics      |     
|  Ubuntu Mono     |  ubuntu     |     italics      |
|  Source Code Pro |  source     |     normal       |
|  Fira Mono       |  fira       |     normal       |                  
|  Droid Sans Mono |  droid      |     normal       |         
|  Oxygen Mono     |  oxygen     |     normal       |
|  Inconsolata     |  incon      |     normal       |

* or provide the name of any monospace font you have installed locally



## Examples
```sh
# list available themes
# oceans16 | grade3 | chesterish | onedork
jt -l

# select theme...
jt -t chesterish

# toggle toolbar ON [Default: hidden]
jt -t grade3 -T

# set code font to 'Space Mono' 12pt
# see table above for more options
jt -t oceans16 -f space -fs 12

# set notebook & text-cell font-family to serif
# both default to sans-serif
jt -t onedork -nbff serif -tcff serif

# adjust cell width and line-height
jt -t chesterish -cw 870 -lh 170

# choose alternate txt/markdown layout
jt -t grade3 -alt -fs 10 -cw 900 -tcff serif

# restore default theme
jt -r
```

## Known Issues
* jupyterthemes relies on ![lesscpy](https://github.com/lesscpy/lesscpy) to compile the custom arguments supplied by the user into into the css body that eventually gets saved as custom.css in your jupyter config directory.

* Unfortunately, lesscpy currently only supports up to Python 3.4. However, if you're running Python 3.5 you can still install and use jupyterthemes but you won't be able to modify the default settings (e.g., font, font-size, cell width, etc.)

* Examples for Python 3.5 users:
```sh
# install a theme
jt -t grade3
# list theme
jt -l
# reset theme
jt -r

```
