## Theme-ify your Jupyter Notebooks!

###Oceans16 Notebook
Oceans16 theme is a take on the popular Ocean Dark IPyNB theme ([Nikhil Sonnad](https://github.com/nsonnad/base16-ipython-notebook)).
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/oceans16_nb.png?raw=true)

###Grade3 Notebook
Grade3 is a spinoff of the python syntax theme used by [nixCraft](http://www.cyberciti.biz/faq/python-sleep-command-syntax-example/)
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/grade3_nb.png?raw=true)

###Oceans16 Syntax
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/oceans16.png?raw=true)

###Oceans16-Bright Syntax
Bright variant of Oceans16 theme
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/oceans-16-bright.png?raw=true)

###Grade3 Syntax
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/grade3.png?raw=true)

[__Source Code Pro__](https://github.com/adobe/Source-Code-Pro) &  [__Hack__](https://github.com/chrissimpkins/Hack) fonts (.ttf) included in Fonts dir"


## Install jupyter-themes

```sh
$ pip install git+https://github.com/dunovank/jupyter-themes.git
```

## Pick a theme and install

```sh
# list themes
$ jupyter-theme -l
Themes in ~/.jupyter-themes
grade3
oceans16
oceans16-bright

# install theme (-t) for ipython/jupyter version > 3.x (-J)
$ jupyter-theme -J -t grade3

# install a theme (-t) without toolbar
$ jupyter-theme -t grade3

# install a theme (-t) with toolbar (-T) enabled
$ jupyter-theme -T -t grade3

# reset (-r) to default for ipython/jupyter version <= 2.x
# renames custom.css in in ~/.ipython/{profile}/static/custom/ to custom_old.css
$ jupyter-theme -r

# reset (-r) to default for ipython/jupyter version > 3.x (-J)
# renames custom.css in ~/.jupyter/custom/ (and ~/.ipython/../custom) to custom_old.css
$ jupyter-theme -J -r
```
#### mmmm so theme-y...

### Instructions for Restoring the Toolbar

By default, these themes hide the toolbar. If you find the notebook toolbar useful, you can restore it by commenting out (or permanently deleting) the following lines of code in the css file (around lines 20 - 40 depending on which theme you install)

```css
div#maintoolbar {
display: none !important;
}
```

![How to find the right place in the code](https://dl.dropboxusercontent.com/u/9420368/scr/maintoolbar.png)
