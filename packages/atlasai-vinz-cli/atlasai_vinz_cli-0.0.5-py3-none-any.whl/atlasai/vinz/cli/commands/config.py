import click
from .cli import cli
from ..config import write_config, get_config
from ..output import output_result, output_message


@cli.group(name="config", help="Config management.")
@click.pass_context
def config(ctx):
    pass

@config.command(name='set', help='Set a configuration')
@click.argument('key_value', type=str, required=False)
def set_conf(key_value):
    params = key_value.split(':')
    if not len(params) == 2:
        output_message('Configuration format not valid. Please set it in key:value format')
        return
    key, value = params[0], params[1]
    if key == 'output' and value not in ['json', 'yaml', 'table', 'csv']:
        output_message('Output format is not valid. Please choose one of the following: json,csv,yaml,csv')
        return
    data = {key: value}
    if data:
        write_config(data)

@config.command(name='get', help='List the configuration')
@click.pass_context
def get_conf(ctx):
    data = get_config()
    output_result(ctx, data)
