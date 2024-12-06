import click

from .cli import cli
from ..api import _list
from ..output import output_result

@cli.group(help="Api management.")
@click.pass_context
def api(ctx):
    pass


@api.command(name='list', help='List Apis.')
@click.option('--query', '-q', 'query', type=str, required=False, help='Filter Groups')
@click.option('--limit', '-l', 'limit', type=str, required=False, help='Limit the number of objects to return.')
@click.option('--offset', '-o', 'offset', type=str, required=False, help='Offset the objects.')
@click.pass_context
def list_apis(ctx, query, limit, offset):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query,
    }
    _, result = _list(
        ctx.obj['access_token'], 'apis', params=params
    )
    output_result(ctx, result)


@api.group(name='permissions', help='Api Permissions')
@click.pass_context
def permissions(ctx):
    pass


@permissions.command(name='list', help='Retrieve permissions of an api.')
@click.option('--query', '-q', 'query', type=str, required=False, help='Filter Organizations')
@click.option('--limit', '-l', 'limit', type=str, required=False, help='Limit the number of objects to return.')
@click.option('--offset', '-o', 'offset', type=str, required=False, help='Offset the objects.')
@click.option('--api-id', 'api_id', type=str, required=True, help='The id of the api.')
@click.pass_context
def list_permissions(ctx, api_id, limit, offset, query):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query
    }

    _, result = _list(
        ctx.obj['access_token'], f'apis/{api_id}/permissions', params=params
    )
    output_result(ctx, result)
