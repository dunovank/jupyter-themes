### Release Notes

#### **v0.20.0**
- fixed output display (no longer clips output)
- added seaborn style update
- fix toolbar style in terminal mode

#### **v0.19.6**
- added notebook>=5.6.0 as dependency

#### **v0.19.5**
- added style compatibility with `notebook 5.6.0`

#### **v0.19.4**
- binder update
- fixed prompt alignment across cell types

#### **v0.19.3**
- only display run code-cell button on prompt hover
- fixed code cell soft-selected prompt style

#### **v0.19.2**
- Apply theme to run code-cell button (input prompt)
- Fixed notification area alignment with kernel, modal_indicators
- disabled command/edit mode indicators in notification_area
- Markdown: align left for h1

#### **v0.19.1**
- fixed header alignment (align center for h1; left for h<=h2)

#### **v0.19.0**
- merged [PR #190](https://github.com/dunovank/jupyter-themes/pull/190/files) submitted by [tnilanon](https://github.com/tnilanon)

#### **v0.18.9**
- added glob import to jtplot

#### **v0.18.8**
- add defaults folder to tar

#### **v0.18.6**
- hopefully encoding error is fixed for Python2* users.
- added defaults folder with custom.css/js files to override JT on reset
- Several PR merged including new fonts, Markdown headers fixed, etc.

#### **v0.18.5**
- apply style to table-of-contents sidebar

#### **v0.18.4**
- merged [PR #227](https://github.com/dunovank/jupyter-themes/pull/227) submitted by [rightx2](https://github.com/rightx2) fixing encoding error

#### **v0.18.3**
- merged [PR #215](https://github.com/dunovank/jupyter-themes/pull/215) submitted by [PegasusWithoutWings](https://github.com/PegasusWithoutWings) fixing lesscpy dependency
- updated setup.py dependencies to fix Travis checks

#### **v0.18.2**
- fixed soft-selected cell border style
- misc. style updates

#### **v0.18.0**
- updated all styles (fixed broken themes)
- misc. style updates

#### **v0.17.9**
- merged [PR #180](https://github.com/dunovank/jupyter-themes/pull/180) submitted by  [fry95116](https://github.com/fry95116) fixing str formatting issue with `-mathfs` arg
- misc. style updates

#### **v0.17.8**
- fixed soft-selected cell highlighting
- misc. style updates from "safarinb" project (buttons, tabs, hover, focus, etc.)

#### **v0.17.7**
- removed dependency check from setup.py script (caused issues with dependencies)
- added cl flag for setting math (latex) fontsize (`-mathfs`)

#### **v0.17.6**
- added dependency check to setup.py script (prevent unnecessary dep upgrades)

#### **v0.17.5**
- removed version on ipython requirement
- merged gruvbox themes PR
- modified selected code-cell behavior (border-left colors in command and edit_mode)
- removed command- and edit-mode border colors on output-prompt
- added `-altout` (--altoutput) argument for setting output area background to notebook bg**

#### **v0.17.3**
- removed develop branch
- changed README build status to master branch
- correction to cell-width help docs (px or %)

#### **v0.17.1**
- fixed bug caused by [PR #152](https://github.com/dunovank/jupyter-themes/pull/152) preventing install on Windows machines
- added explicit pointers to layout and styles.less/.css package data in setup.py

#### **v0.17.0**
- fixed neglected dependencies issue

#### **v0.16.7**
- fixed hbox widget display (no longer vertically stacks objects)
- applied style to pager documentation
- added gridlines option to jtplot.style() to set linestyle of axis grid
- README update with more jtplot documentation
- removed seaborn from dependencies
- explicitly import stylefx and jtplot modules to \__init__.py

#### **v0.16.6**
- minor bug-fix in jtplot (prevent clist printing)

#### **v0.16.5**
- improved monokai comment visibility
- solarized style improvements (l & d flavors)
- improved kernel-busy animation
- moved kernel-idle/busy code from extras.less to notebook.less
- notebook-fontsize (-nfs) adjusts header
- minor cosmetic improvements
- fixed matplotlib error in jtplot
- added check_dependencies() fx to prevent unnecessary dependency installs

#### **v0.16.4:**
- fixed pulse kernel-busy indicator

#### **v0.16.4:**
- fixed pulse kernel-busy indicator

#### **v0.16.3:**
- removed broken matplotlib dependency
- added pulse kernel-busy indicator

#### **v0.16.2:**
- added matplotlib and seaborn dependencies
- updated index.ipynb for binder and compiled themes
- minor cosmetic improvements

#### **v0.16.1:**
- removed some excess fonts from sans-serif and serif collections
- added option for setting pandas dataframe font-size (-dfs , --dffontsize)
- added option for output area font-size (-ofs , --outfontsize)
- minor cosmetic improvements

#### **v0.16.0:**
- all fonts now default to whatever browser defaults are (users can still specify custom code-cell (-f), text-cell (-tcf), and notebook (-nbf) fonts as before).
- improved prompt style for text cells
- re-compiled css for binder
- minor cosmetic improvements

####  **v0.15.9:**
- improved kernel and notification widget alignment
- added helvetica, helveticaneue fonts
- fixed bug that prevented install if fontname not recognized
- added compatibility for hide_header nbext
- minor cosmetic improvements

#### **v0.15.8:**
- made changes to solarizedd style

#### **v0.15.7:**
- added solarized-dark theme "jt -t solarizedd" ([PR #103](https://github.com/dunovank/jupyter-themes/pull/103) submitted by [raybuhr](https://github.com/raybuhr))
- fixed jupyter-soft-selected style (multiple cell selected)
- modified table style
- deprecated -alt/--altlayout (use -altp/--altprompt for smaller prompts, no number)

#### **v0.15.6:**
- fixed bug that prevented fonts from being imported correctly

#### **v0.15.5:**
- added compatibility for Jupyter terminal app
- improved toolbar and NB name visibility
- better syntax highlighting in tracebacks
- widened main menubar container at top of NB
- notification widgets no longer interfere with menubar height
- minor cosmetic improvements
- added Hasklig monofont

#### **v0.15.4:**
- improved text editor visibility
- minor cosmetic improvements

#### **v0.15.3:**
- README & doc updates for jtplot module
- style fixes for new "add keyboard shortcuts" form
- minor cosmetic improvements

#### **v0.15.2:**
- re-added solarizedl theme (accidentally not included in v0.15.1)

#### **v0.15.1:**
- updated styles for notebook 5.0
- changed solarized-light to solarizedl
- cosmetic changes to onedork, solarizedl

#### **v0.15.0:**
- themed plotting styles
- python 3.6 compatibility

#### **v0.14.4:**
- fixed attribute and property syntax highlighting
- removed 'TeX' as preferred mathjax font

#### **v0.14.3:**
- [PR #102](https://github.com/dunovank/jupyter-themes/pull/102) submitted by  [pussinboot](https://github.com/pussinboot) fixed font installation [issue #71](https://github.com/dunovank/jupyter-themes/issues/71)

#### **v0.14.2:**
-removed numpy dependency ([meowklaski](https://github.com/meowklaski) : [PR #97](https://github.com/dunovank/jupyter-themes/pull/97))

#### **v0.14.1**
-fixed linenumbers in onedork theme

#### **v0.14.0:**
-add solarized light theme ([svendx4f](https://github.com/svendx4f): [PR #84](https://github.com/dunovank/jupyter-themes/pull/84))
-fixed bug that prevented theme reset
-fixed bug that prevented cursor settings from being applied
-made upload button visible on main page

#### **v0.13.9**
* minor bug fixes and thematic adjustments

#### **v0.13.8**
* add monokai theme ([bdell](https://github.com/bdell) : [PR #59](https://github.com/dunovank/jupyter-themes/pull/59))
* apply theme to auto-complete menu ([svendx4f](https://github.com/svendx4f) : [PR #69](https://github.com/dunovank/jupyter-themes/pull/69))
* added support for user less/precompiled themes ([osamaar](https://github.com/osamaar) : [PR #82](https://github.com/dunovank/jupyter-themes/pull/82))

#### **v0.13.7**
* misc visibility improvements

#### **v0.13.6**
* altlayout is now default for grade3 (white bg for txt/markdown)

#### **v0.13.5**
* full functionality has been added for Python 3.5
* better theme integration for command palette, keyboard shortcuts
* integration with Running, Clusters, and NBExtension pages.
* added font options for code-cells and notebook body
* vim nbextension compatibility provided by [alextfkd](https://github.com/alextfkd)
* customizable cursor color and size
