## Theme-ify your Jupyter Notebooks!


### New themes and customizable options
```sh
jt -t chesterish -cw 850 -fs 10
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-tchesterish-cw850-fs10.png?raw=true)

```sh
jt -t oceans16 -altmd -fs 10 -cw900
```
![image](https://github.com/dunovank/jupyter-themes/blob/master/screens/jt-toceans16-altmd-fs10-cw900.png?raw=true)

```sh
jt -t onedork -cw 850 -fs 10
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


### Install jupyterthemes w/ pip (officially)
```sh
pip install jupyterthemes
```

### How to...
```sh
# can call with "jupyter-themes" or "jt" interchangeably
# list available themes
# oceans16 | grade3 | chesterish (New!) | onedork (New!)
jt -l

# install a theme...
jt -t grade3

# ...with toolbar (-T) enabled
jt -T -t grade3

# ...and adjust cell width [default=950 (pixels)]
jt -t grade3 -cw 850

# ...with alternate markdown/text-cell layout
jt -t grade3 -altmd

# set font (-f) and font-size (-fs) (defaults are Hack and 11)
jt -t grade3 -f Source-Code-Pro -fs 10

# set notebook (-ff) & textcell fontfamily (-tcff) (both default to sans)
jt -t grade3 -ff serif -tcff serif

# restore (-r) default theme
jt -r
```

#### mmmm so theme-y...
