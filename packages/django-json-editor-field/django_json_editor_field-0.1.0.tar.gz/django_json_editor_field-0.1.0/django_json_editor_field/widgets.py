from django.forms.widgets import Input


class JSONEditorWidget(Input):
    input_type = "hidden"
    template_name = "widgets/json_editor_widget.html"

    class Media:
        js = [
            "https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.js",
            "js/jsonwidget.js",
        ]
        css = {
            "all": ["css/jsonwidget.css"],
        }

    def __init__(self, schema={}, *args, **kwargs):
        self.schema = schema
        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        ctx["schema"] = self.schema
        return ctx
