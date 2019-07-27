from unittest import TestCase

from py_schema import SchemaValidator, SchemaValidationError, \
    IntField, StrField, BoolField, FloatField, DictField, ListField, \
    EnumField


class SchemaValidatorTest(TestCase):
    def test_required_with_none_should_raise_error(self):
        schema = IntField(
            required=True
        )
        value = None

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is required'
            )

    def test_full_schema_should_pass(self):
        schema = ListField(
            min_length=1,
            max_length=3,
            item_schema=DictField(
                schema={
                    'name': StrField(
                        min_length=2,
                        max_length=50,
                    ),
                    'age': IntField(
                        min=0,
                        max=120
                    ),
                    'money': FloatField(
                        min=0.0,
                        max=999.9
                    ),
                    'alive': BoolField(),
                    'gender': EnumField(
                        accept=['M', 'F', 'O']
                    )
                },
                strict=True,
                optional_props=['gender']
            )
        )

        value = [
            {
                'name': 'Batman',
                'age': 31,
                'money': 999.0,
                'alive': True,
                'gender': 'M'
            },
            {
                'name': 'Superman',
                'age': 29,
                'money': 0.0,
                'alive': True
            }
        ]

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class IntFieldTest(TestCase):
    def test_not_type_int_should_raise_error(self):
        schema = IntField(
            required=True
        )
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is not an int'
            )

    def test_value_less_should_raise_error(self):
        schema = IntField(
            min=1
        )
        value = 0

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is less than 1'
            )

    def test_value_greater_should_raise_error(self):
        schema = IntField(
            max=1
        )
        value = 2

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is greater than 1'
            )

    def test_valid_value_should_pass(self):
        schema = IntField(
            min=1,
            max=10
        )
        value = 5

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class StrFieldTest(TestCase):
    def test_invalid_type_should_raise_error(self):
        schema = StrField()
        value = 123

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is not a str'
            )

    def test_min_length_should_raise_error(self):
        schema = StrField(
            min_length=4
        )
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value has less then 4 length'
            )

    def test_max_length_should_raise_error(self):
        schema = StrField(
            max_length=4
        )
        value = 'abcde'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value has more then 4 length'
            )

    def test_valid_str_should_pass(self):
        schema = StrField(
            min_length=1,
            max_length=5
        )
        value = 'abcde'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class BoolFieldTest(TestCase):
    def test_invalid_type_should_raise_error(self):
        schema = BoolField()
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is not a bool'
            )

    def test_valid_bool_should_pass(self):
        schema = BoolField()
        value = False

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class FloatFieldTest(TestCase):
    def test_not_type_float_should_raise_error(self):
        schema = FloatField()
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is not a float'
            )

    def test_value_less_should_raise_error(self):
        schema = FloatField(
            min=1
        )
        value = 0.0

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is less than 1'
            )

    def test_value_greater_should_raise_error(self):
        schema = FloatField(
            max=1
        )
        value = 2.0

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is greater than 1'
            )

    def test_valid_value_should_pass(self):
        schema = FloatField(
            min=1,
            max=10
        )
        value = 5.0

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()


class DictFieldTest(TestCase):
    def test_invalid_type_should_raise_error(self):
        schema = DictField(
            schema={}
        )
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is not a dict'
            )

    def test_not_allowed_prop_should_raise_error(self):
        schema = DictField(
            schema={
                'foo': BoolField(),
                'bar': BoolField()
            },
            strict=True
        )
        value = {
            'foo': True,
            'bar': False,
            'baz': None
        }

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The property "baz" is not allowed'
            )

    def test_optional_prop_should_be_valid_if_not_present(self):
        schema = DictField(
            schema={
                'foo': BoolField(),
                'bar': BoolField()
            },
            strict=True,
            optional_props=['bar']
        )
        value = {
            'foo': True
        }

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        validator.validate()

    def test_prop_with_invalid_value_should_raise_error(self):
        schema = DictField(
            schema={
                'foo': BoolField(),
                'bar': BoolField()
            },
            strict=True
        )
        value = {
            'foo': True,
            'bar': 'abc'
        }

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root.bar'
            )
            self.assertEqual(
                e.message, 'The value is not a bool'
            )

    def test_nested_dict_with_invalid_prop_should_raise_error(self):
        schema = DictField(
            schema={
                'foo': BoolField(),
                'bar': DictField(
                    schema={
                        'baz': BoolField()
                    }
                )
            },
            strict=True
        )
        value = {
            'foo': True,
            'bar': {
                'baz': 123
            }
        }

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root.bar.baz'
            )
            self.assertEqual(
                e.message, 'The value is not a bool'
            )


class ListFieldTest(TestCase):
    def test_invalid_type_should_raise_error(self):
        schema = ListField(
            item_schema=BoolField()
        )
        value = 'abc'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is not a list'
            )

    def test_less_items_should_raise_error(self):
        schema = ListField(
            item_schema=BoolField(),
            min_length=1
        )
        value = []

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value have less then 1 item(s)'
            )

    def test_more_items_should_raise_error(self):
        schema = ListField(
            item_schema=BoolField(),
            max_length=1
        )
        value = [True, False]

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value have more then 1 item(s)'
            )

    def test_invalid_item_value_should_raise_error(self):
        schema = ListField(
            item_schema=BoolField()
        )
        value = [True, False, 'zelda']

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root.$2'
            )
            self.assertEqual(
                e.message, 'The value is not a bool'
            )

    def test_invalid_nested_list_item_value_should_raise_error(self):
        schema = ListField(
            item_schema=DictField(
                schema={
                    'values': ListField(
                        item_schema=BoolField()
                    )
                }
            )
        )
        value = [
            {
                'values': [True, False, 'Link']
            }
        ]

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root.$0.values.$2'
            )
            self.assertEqual(
                e.message, 'The value is not a bool'
            )


class EnumFieldTest(TestCase):
    def test_not_accepted_value_should_raise_error(self):
        schema = EnumField(
            accept=['123']
        )
        value = '456'

        validator = SchemaValidator(
            schema=schema,
            value=value
        )

        try:
            validator.validate()
            self.fail()
        except SchemaValidationError as e:
            self.assertEqual(
                e.path, '$root'
            )
            self.assertEqual(
                e.message, 'The value is not accepted'
            )