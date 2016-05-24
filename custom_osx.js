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
 */


 define([
    'base/js/namespace',
    'base/js/events'
    ],
    function(IPython, events) {
        events.on("app_initialized.NotebookApp", function () {
            Jupyter.keyboard_manager.command_shortcuts.add_shortcut('Cmd-Shift-Up', {
                help : 'move cell up',
                help_index : 'zz',
                handler : function (event) {
                    IPython.notebook.move_cell_up();
                    return false;
                }}
            );
            Jupyter.keyboard_manager.command_shortcuts.add_shortcut('Cmd-Shift-Down', {
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
