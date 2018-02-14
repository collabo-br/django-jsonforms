from django.test import TestCase, override_settings
from django.forms import ValidationError, Form
from django_jsonforms.forms import JSONSchemaField, JSONSchemaForm
import json
import os

from django_jsonforms.forms import JSONSchemaField

thisdir = os.path.dirname(os.path.dirname(__file__))

class JSONTestForm(Form):

    def __init__(self, schema, options, ajax=True, *args, **kwargs):
        super(JSONTestForm, self).__init__(*args, **kwargs)
        self.fields['json1'] = JSONSchemaField(schema=schema, options=options, ajax=ajax)
        self.fields['json2'] = JSONSchemaField(schema=schema, options=options, ajax=ajax)

class DjangoFormsTest(TestCase):

    def setUp(self):
        self.schema = {
            'type': 'object',
            'properties': {
                'color': {
                    'description': 'a color',
                    'type': 'string'
                },
                'number': {
                    'description': 'a very nice number',
                    'type': 'integer'
                },
                'list': {
                    'description': 'what a list',
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            }
        }

        self.options = {'theme': 'html'}

        self.test_json = {
            'color': 'red',
            'number': 1,
            'list': [
                'very',
                'good',
                'list'
            ]
        }

    def test_valid_data_for_schema(self):

        form_data = {'json': json.dumps(self.test_json)}
        form = JSONSchemaForm(schema=self.schema, options=self.options, data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_data_for_schema_two_fields(self):

        form_data = {'json1': json.dumps(self.test_json), 'json2': json.dumps(self.test_json)}
        form = JSONTestForm(schema=self.schema, options=self.options, data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_json(self):

        form_data = {'json': '{\"yeah\": \"yeah}'}
        form = JSONSchemaForm(schema=self.schema, options=self.options, data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['json'], [u"Invalid JSON"])

    def test_invalid_data_for_schema(self):

        test_json = {
            'color': 'red',
            'number': 'one',
        }
        form_data = {'json': json.dumps(test_json)}
        form = JSONSchemaForm(schema=self.schema, options=self.options, data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['json'], [u"\'one\' is not of type \'integer\'"])

    def test_invalid_schema_file(self):

        form = JSONSchemaForm(options=self.options, schema='very/real/file.json')
        self.assertFalse(form.is_valid())

    @override_settings(STATIC_ROOT=thisdir)
    def test_valid_data_with_schema_file(self):

        form_data = {'json': json.dumps(self.test_json)}
        form = JSONSchemaForm(schema='tests/test_schema.json', options=self.options, data=form_data)
        self.assertTrue(form.is_valid())

# Test file and dict options, file does not exist
# Test form html output to test template rendering
