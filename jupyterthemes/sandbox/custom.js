// leave at least 2 line with only a star on it below, or doc generation fails
/**
 *
 *
 *
 *
 * @module IPython
 * @namespace IPython
 * @class customjs
 * @static

 MathJax.Hub.Config({
  "HTML-CSS": {
    availableFonts: [], preferredFont: null, // force Web fonts
    webFont: "Neo-Euler"
  }
});


* OR


MathJax.Hub.Config({
  "HTML-CSS": {
   availableFonts: ["TeX","STIX-Web","Neo-Euler"],
   preferredFont: "Neo-Euler",
  }
});
 */
 define([
    'base/js/namespace',
    'base/js/events'
    ],
    function(IPython, events) {
        events.on("app_initialized.NotebookApp", function () {
            Jupyter.keyboard_manager.command_shortcuts.add_shortcut('Ctrl-Shift-Up', {
                help : 'move cell up',
                help_index : 'zz',
                handler : function (event) {
                    IPython.notebook.move_cell_up();
                    return false;
                }}
            );
            Jupyter.keyboard_manager.command_shortcuts.add_shortcut('Ctrl-Shift-Down', {
                help : 'move cell down',
                help_index : 'zz',
                handler : function (event) {
                    IPython.notebook.move_cell_down();
                    return false;
                }}
            );
        });
    }
);
