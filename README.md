## Theme-ify your Jupyter Notebooks!

### Oceans16 Notebook
Oceans16 theme is a take on the popular Ocean Dark IPyNB theme ([Nikhil Sonnad](https://github.com/nsonnad/base16-ipython-notebook)).
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/oceans16_nb.png?raw=true)

### Grade3 Notebook
Grade3 is a spinoff of the python syntax theme used by [nixCraft](http://www.cyberciti.biz/faq/python-sleep-command-syntax-example/)
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/grade3_nb.png?raw=true)

### Oceans16 Syntax
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/oceans16.png?raw=true)

### Grade3 Syntax
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/grade3.png?raw=true)

### Space-Legos Syntax
![image](https://github.com/dunovank/jupyter-themes/blob/master/Screens/space-legos.png?raw=true)

### Fonts
[__Source Code Pro__](https://github.com/adobe/Source-Code-Pro) &  [__Hack__](https://github.com/chrissimpkins/Hack) fonts (.ttf) included in Fonts dir

### Install jupyter-themes w/ pip
```sh
pip install git+https://github.com/dunovank/jupyter-themes.git
```

### How to...
```sh
# list available themes (located in ~/.jupyter-themes)
jt -l

# install a theme (to ~/.jupyter/custom/)
# theme names: oceans16 | grade3 | space-legos
jt -t grade3

# install a theme with toolbar (-T) enabled
jt -T -t grade3

# set font (-f) and font-size (-fs) (defaults are Hack and 11)
jt -t grade3 -f Source-Code-Pro -fs 12

# restore (-r) default theme
jt -r
```

#### Experimental
***use with caution if you have already modified
your ~/.jupyter/nbconfig/notebook.json file***

```sh
# enable linewrapping in code cells
jt -t grade3 -lw

# adjust size of indent unit (default=4)
jt -t grade3 -iu 6
```

#### mmmm so theme-y...
