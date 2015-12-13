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

###Instructions for Restoring the Toolbar
By default, these themes hide the toolbar. If you find the notebook toolbar useful, you can restore it by commenting out (or permanently deleting) the following lines of code in the css file (around lines 20 - 40 depending on which theme you install)

```css
div#maintoolbar {
display: none !important;
}
```

## install jupyter-themes

```sh
$ pip install git+https://git@github.com:dunovank/jupyter-themes.git
```

## Pick a theme and install

```sh
# list themes
$ jupyter-theme -l
grade3
oceans16
ansi-colors
oceans16-bright
# install a theme without toolbar
jupyter-theme -t grade3
# install a theme with toolbar enabled
jupyter-theme -T -t grade3
# reset to default
 jupyter-theme -r
```
#### mmmm so theme-y...
