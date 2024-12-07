window.addEventListener('load', () => {
    JSONEditor.defaults.options.theme = "bootstrap4";
    JSONEditor.defaults.options.disable_collapse = true;
    JSONEditor.defaults.options.disable_edit_json = true;
    JSONEditor.defaults.options.disable_properties = true;
    JSONEditor.defaults.options.disable_array_reorder = true;
    JSONEditor.defaults.options.disable_array_delete_last_row = true;
    JSONEditor.defaults.options.disable_array_delete_all_rows = true;
    JSONEditor.defaults.options.prompt_before_delete = false;
    document.querySelectorAll(".jsonfield").forEach(function(element) {
        schema = JSON.parse(element.getElementsByTagName('script')[0].textContent);
        input = element.getElementsByTagName('input')[0];
        editor = new JSONEditor(element, {
            schema: schema,
        });
        editor.on('ready', () => {
            editor.setValue(JSON.parse(input.value));
        });
        editor.on('change', () => {
            input = element.getElementsByTagName('input')[0];
            if (input) {
                input.value = JSON.stringify(editor.getValue());
            }
        });
    });
});
