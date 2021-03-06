from marshmallow import fields
from marshmallow import Schema
from marshmallow import RAISE
from marshmallow import ValidationError
from marshmallow import validates


class Policy(Schema):
    enabled = fields.Bool(required=True)
    enforcing = fields.Bool(required=True)
    version = fields.Str(required=True)


class ValidatePipeVars(Schema):
    run_pipe = fields.Bool(required=True)
    url = fields.Str(required=True)
    version = fields.Str(required=True)
    policy = fields.Nested(Policy)

    @validates('run_pipe')
    def validate_run_pipe(self, value):
        defined_value = True
        pipe_boolean = ('disabled', 'enabled')[defined_value]
        if value != defined_value:
            raise ValidationError(f'Validate Pipe must be {pipe_boolean}')

    @validates('url')
    def validate_url(self, value):
        defined_value = 'http://172.17.0.1:8080/function'
        if value != defined_value:
            raise ValidationError(f'Validate pipe URL must be {defined_value}')


class ValidatePipeConfig(Schema):
    pi_validate_pipe_vars = fields.Nested(ValidatePipeVars)


def validate(config):
    schema = ValidatePipeConfig()
    try:
       _ = schema.load(config)
       result = True
    except ValidationError as err:
        result = err

    return result
