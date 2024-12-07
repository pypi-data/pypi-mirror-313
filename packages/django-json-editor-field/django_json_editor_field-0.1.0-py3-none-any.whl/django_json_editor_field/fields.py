from django.db import models

from django_json_editor_field.widgets import JSONEditorWidget


class JSONEditorField(models.JSONField):
    def __init__(self, *args, **kwargs):
        self.schema = kwargs.pop("schema", {})
        super().__init__(*args, **kwargs)

    def formfield(self, *args, **kwargs):
        kwargs["widget"] = JSONEditorWidget(schema=self.schema)
        return super().formfield(*args, **kwargs)
