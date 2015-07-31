// leave at least 2 line with only a star on it below, or doc generation fails
/**
 *
 *
 * Placeholder for custom user javascript
 * mainly to be overridden in profile/static/custom/custom.js
 * This will always be an empty file in IPython
 *
 * User could add any javascript in the `profile/static/custom/custom.js` file
 * (and should create it if it does not exist).
 * It will be executed by the ipython notebook at load time.
 *
 * Same thing with `profile/static/custom/custom.css` to inject custom css into the notebook.
 *
 * Example :
 *
 * Create a custom button in toolbar that execute `%qtconsole` in kernel
 * and hence open a qtconsole attached to the same kernel as the current notebook
 *
 *    $([IPython.events]).on('app_initialized.NotebookApp', function(){
 *        IPython.toolbar.add_buttons_group([
 *            {
 *                 'label'   : 'run qtconsole',
 *                 'icon'    : 'icon-terminal', // select your icon from http://fortawesome.github.io/Font-Awesome/icons
 *                 'callback': function () {
 *                     IPython.notebook.kernel.execute('%qtconsole')
 *                 }
 *            }
 *            // add more button here if needed.
 *            ]);
 *    });
 *
 * Example :
 *
 *  Use `jQuery.getScript(url [, success(script, textStatus, jqXHR)] );`
 *  to load custom script into the notebook.
 *
 *    // to load the metadata ui extension example.
 *    $.getScript('/static/notebook/js/celltoolbarpresets/example.js');
 *    // or
 *    // to load the metadata ui extension to control slideshow mode / reveal js for nbconvert
 *    $.getScript('/static/notebook/js/celltoolbarpresets/slideshow.js');
 *
 *
 * @module IPython
 * @namespace IPython
 * @class customjs
 * @static
 */
 // Example for custom.js

// we want strict javascript that fails on ambiguous syntax
"using strict";
// activate extensions only after Notebook is initialized

require(["base/js/events"], function (events) {

      $([IPython.events]).on("app_initialized.NotebookApp", function () {
                /*
                * all exentensions from IPython-notebook-extensions, uncomment to activate
                */
            IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-k', function (event) {
                  IPython.notebook.move_cell_up();
                  return false;
            });

            IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-j', function (event) {
                  IPython.notebook.move_cell_down();
                  return false;
            });

            IPython.tab_as_tab_everywhere = function(use_tabs) {
                  if (use_tabs === undefined) {
                  use_tabs = true;
                  }

                  // apply setting to all current CodeMirror instances
                  IPython.notebook.get_cells().map(
                  function(c) {  return c.code_mirror.options.indentWithTabs=use_tabs;  }
                  );
                  // make sure new CodeMirror instances created in the future also use this setting
                  CodeMirror.defaults.indentWithTabs=use_tabs;

                  };

            IPython.load_extensions('notify');
            IPython.Cell.options_default.cm_config.lineWrapping = true;
            IPython.CodeCell.options_default['cm_config']['indentUnit'] = 6;
            IPython.CodeCell.options_default['cm_config']['tabSize'] = 6;

      });
});
