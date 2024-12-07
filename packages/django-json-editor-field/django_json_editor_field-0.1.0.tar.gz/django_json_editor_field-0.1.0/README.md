# Django JSON Editor Field

The Django JSON Editor field enhances [Djangos JSON
Field](https://docs.djangoproject.com/en/stable/ref/models/fields/#django.db.models.JSONField)
add adds a [json-editor](https://github.com/json-editor/json-editor) on top.
You can use a JSON Schema to describe a form for the underlying JSON field. The
input is then stored as JSON.

# Installation

Add `django_json_editor_field` to your [INSTALLED_APPS](https://docs.djangoproject.com/en/stable/ref/settings/#std-setting-INSTALLED_APPS).

Use the field in your model:

```python
from django_json_editor_field.fields import JSONEditorField

schema = {
        "title": "My JSON Array of Objects",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "start": {
                    "type": "string",
                    "format": "date",
                },
                "end": {
                    "type": "string",
                    "format": "date",
                }
            }
        }
}

data = JSONEditorField(schema=schema)
```
