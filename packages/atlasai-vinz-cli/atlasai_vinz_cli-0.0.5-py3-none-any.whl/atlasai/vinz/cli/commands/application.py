import click

from .cli import cli
from ..api import _list
from ..output import output_result

@cli.group(help="Application management.")
@click.pass_context
def application(ctx):
    pass


@application.command(name='list', help='List Applications.')
@click.option('--query', '-q', 'query', type=str, required=False, help='Filter Groups')
@click.option('--limit', '-l', 'limit', type=str, required=False, help='Limit the number of objects to return.')
@click.option('--offset', '-o', 'offset', type=str, required=False, help='Offset the objects.')
@click.pass_context
def list_applications(ctx, query, limit, offset):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query,
    }
    _, result = _list(
        ctx.obj['access_token'], 'applications', params=params
    )
    output_result(ctx, result)
