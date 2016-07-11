## Theme-ify your Jupyter Notebooks!

### Oceans16
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/oceans16_nb.png?raw=true)

### Grade3
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/grade3_nb.png?raw=true)

### Install jupyterthemes w/ pip (officially)
```sh
pip install jupyterthemes
```

### How to...
```sh
# list available themes
# can call with "jupyter-themes" or "jt" interchangeably
jt -l

# install a theme (to ~/.jupyter/custom/)
# theme names: oceans16 | grade3 | space-legos | chesterish (NEW!)
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
