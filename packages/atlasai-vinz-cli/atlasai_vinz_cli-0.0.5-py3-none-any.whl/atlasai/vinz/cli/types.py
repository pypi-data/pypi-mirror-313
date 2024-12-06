import click
import json

class JSONParamType(click.ParamType):
    name = 'json'

    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            self.fail(f'{value!r} is not a valid JSON string: {e}', param, ctx)

JSON = JSONParamType()
