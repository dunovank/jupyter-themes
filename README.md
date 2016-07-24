# jupyterthemes
## Theme-ify your Jupyter Notebooks!

```sh
jt -t chesterish -cw 850 -fs 10
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-tchesterish-cw850-fs10.png?raw=true)

```sh
jt -t oceans16 -altmd -fs 10 -cw 900
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-toceans16-altmd-fs10-cw900.png?raw=true)

```sh
jt -t onedork -fs 10 -cw 850
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-tonedork-cw850-fs10.png?raw=true)

```sh
jt -t grade3 -altmd -fs 10 -cw 900 -tcff serif
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-tgrade3-altmd-fs10-cw900.png?raw=true)

```sh
jt -t onedork -ff serif -tcff serif
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-tonedork-ffserif-tcffserif.png?raw=true)



# Install with pip
```sh
pip install jupyterthemes
```



## How to use
```
usage: jt [-l] [-t THEME] [-f FONT] [-fs FONTSIZE ] [-ff NBFONTFAMILY]  
        [-tcff TCFONTFAMILY] [-cw CELLWIDTH] [-lh LINEHEIGHT] [-altmd] [-T]  [-r ]
```

|        options        | arguments |     default    |
|:----------------------|:---------:|:--------------:|     
| List Themes           |  -l       |       --       |
| Select Theme          |  -t       |       --       |
| Code Font             |  -f       |      Hack      |
| Code Font-Size        |  -fs      |       11       |
| NB Font-Family        |  -ff      |   sans-serif   |
| TxtCell Font-Family   |  -tcff    |   sans-serif   |
| Cell Width            |  -cw      |      910       |
| Line Height           |  -lh      |      160       |
| Alt Txt/MD Layout     |  -altmd   |       --       |
| Make Toolbar Visible  |  -T       |       --       |
| Restore Default       |  -r       |       --       |

### Importable Code Fonts from Google Fonts API

|    Font-Name     |    -f       |     comments     |
|:-----------------|:-----------:|:----------------:|     
|     Hack         |    --       |     italics      |
|  Source Code Pro |  source     |     italics      |
|  Roboto Mono     |  roboto     |     italics      |
|  Space Mono      |  space      |     italics      |         
|  Anonymous Pro   |  anon       |     italics      |
|  Cousine         |  cousine    |     italics      |     
|  Ubuntu Mono     |  ubuntu     |     italics      |
|  Fira Mono       |  fira       |     normal       |                  
|  Droid Sans Mono |  droid      |     normal       |         
|  Oxygen Mono     |  oxygen     |     normal       |
|  Inconsolata     |  incon      |     normal       |
* or pass the name of any monospace font you have installed locally (hyphenate spaces)


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
jt -t onedork -ff serif -tcff serif

# adjust cell width and line-height
jt -t chesterish -cw 870 -lh 170

# choose alternate txt/markdown layout
jt -t grade3 -altmd -fs 10 -cw 895 -tcff serif

# restore default theme
jt -r
```

#### mmmm so theme-y...
