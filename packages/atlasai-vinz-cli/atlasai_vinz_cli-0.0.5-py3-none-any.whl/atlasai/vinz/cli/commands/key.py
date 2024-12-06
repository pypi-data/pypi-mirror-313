import click

from .cli import cli
from ..api import _delete, _list, _create
from ..output import output_result, output_message

@cli.group(help="Key management.")
@click.pass_context
def key(ctx):
    pass

@key.command(name='list', help='List Keys.')
@click.pass_context
def list_keys(ctx):
    params = {}
    _, result = _list(
        ctx.obj['access_token'], 'keys', params=params, is_paginated=False
    )

    result = result.get('api_keys', [])
    output_result(ctx, result)

@key.command(name='create', help='Create a new Key.')
@click.pass_context
def create_key(ctx):
    params = {}
    data = {}
    _, result = _create(
        ctx.obj['access_token'], 'key', data=data, params=params
    )
    output_result(ctx, result)

@key.command(name='delete', help='Delete a Key.')
@click.option('--access-key', 'access_key', type=str, required=True, help='Access key to delete')
@click.pass_context
def delete_key(ctx, access_key):
    params = {}
    _, result = _delete(
        ctx.obj['access_token'], f'key/{access_key}', params=params
    )
    output_result(ctx, result)
    output_message('Key deleted successfully!')
