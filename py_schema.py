

class SchemaValidationError(Exception):
    def __init__(self, message: str, path: str):
        self.message = message
        self.path = path


class SchemaValidator:
    def __init__(self, schema, value):
        self.schema = schema
        self.value = value
        self.path = ['$root']

    def add_to_path(self, key: str):
        self.path.append(key)

    def pop_path(self):
        self.path.pop()

    def raise_error(self, message: str):
        raise SchemaValidationError(
            message=message,
            path='.'.join(self.path)
        )

    def validate(self):
        self.schema.value = self.value
        self.schema.ctx = self
        self.schema.validate()


class BaseField:
    def __init__(self, required: bool = True):
        self.required = required
        self.value: any = None
        self.ctx: SchemaValidator = None

    def validate_required(self):
        if self.required and self.value is None:
            self.ctx.raise_error('The value is required')

    def validator(self):
        raise NotImplementedError()

    def validate(self):
        self.validate_required()
        self.validator()


class IntField(BaseField):
    def __init__(self, min: int = None, max: int = None, *args, **kwargs):
        super(IntField, self).__init__(*args, **kwargs)
        self.min = min
        self.max = max

    def validator(self):
        if type(self.value) is not int:
            self.ctx.raise_error(
                'The value is not an int'
            )

        if self.min is not None and self.value < self.min:
            self.ctx.raise_error(
                f'The value is less than {self.min}'
            )

        if self.max is not None and self.value > self.max:
            self.ctx.raise_error(
                f'The value is greater than {self.max}'
            )


class FloatField(BaseField):
    def __init__(self, min: float = None, max: float = None, *args, **kwargs):
        super(FloatField, self).__init__(*args, **kwargs)
        self.min = min
        self.max = max

    def validator(self):
        if type(self.value) is not float:
            self.ctx.raise_error(
                'The value is not a float'
            )

        if self.min is not None and self.value < self.min:
            self.ctx.raise_error(
                f'The value is less than {self.min}'
            )

        if self.max is not None and self.value > self.max:
            self.ctx.raise_error(
                f'The value is greater than {self.max}'
            )


class StrField(BaseField):
    def __init__(self, min_length: int = None, max_length: int = None, *args, **kwargs):
        super(StrField, self).__init__(*args, *kwargs)
        self.min_length = min_length
        self.max_length = max_length

    def validator(self):
        if type(self.value) is not str:
            self.ctx.raise_error(
                'The value is not a str'
            )

        if self.min_length is not None and len(self.value) < self.min_length:
            self.ctx.raise_error(
                f'The value has less then {self.min_length} length'
            )

        if self.max_length is not None and len(self.value) > self.max_length:
            self.ctx.raise_error(
                f'The value has more then {self.max_length} length'
            )


class BoolField(BaseField):
    def validator(self):
        if type(self.value) is not bool:
            self.ctx.raise_error(
                'The value is not a bool'
            )


class DictField(BaseField):
    def __init__(self, schema: dict, optional_props: [str] = [], strict: bool = False, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)
        self.schema = schema
        self.optional_props = optional_props
        self.strict = strict

    def validator(self):
        if type(self.value) is not dict:
            self.ctx.raise_error(
                'The value is not a dict'
            )

        if self.strict:
            for value_prop_key in self.value:
                if value_prop_key not in self.schema and value_prop_key not in self.optional_props:
                    self.ctx.raise_error(
                        f'The property "{value_prop_key}" is not allowed'
                    )

        for schema_prop_key in self.schema:
            if schema_prop_key not in self.value:
                if schema_prop_key in self.optional_props:
                    continue
                else:
                    self.ctx.raise_error(
                        message='The property "{}" is missing'.format(schema_prop_key)
                    )

            prop_field = self.schema[schema_prop_key]

            self.ctx.add_to_path(schema_prop_key)

            prop_field.value = self.value[schema_prop_key]
            prop_field.ctx = self.ctx

            prop_field.validate()

            self.ctx.pop_path()


class ListField(BaseField):
    def __init__(self, item_schema: BaseField, min_length: int = None, max_length: int = None, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        self.item_schema = item_schema
        self.min_length = min_length
        self.max_length = max_length

    def validator(self):
        if type(self.value) is not list:
            self.ctx.raise_error(
                'The value is not a list'
            )

        if self.min_length is not None and len(self.value) < self.min_length:
            self.ctx.raise_error(
                f'The value have less then {self.min_length} item(s)'
            )

        if self.max_length is not None and len(self.value) > self.max_length:
            self.ctx.raise_error(
                f'The value have more then {self.max_length} item(s)'
            )

        for index, item in enumerate(self.value):
            self.ctx.add_to_path(f'${index}')

            self.item_schema.value = item
            self.item_schema.ctx = self.ctx
            self.item_schema.validate()

            self.ctx.pop_path()


class EnumField(BaseField):
    def __init__(self, accept: [any], *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        self.accept = accept

    def validator(self):
        if self.value not in self.accept:
            self.ctx.raise_error(
                f'The value is not accepted'
            )