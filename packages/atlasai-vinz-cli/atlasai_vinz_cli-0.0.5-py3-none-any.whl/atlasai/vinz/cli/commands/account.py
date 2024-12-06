import click

from .cli import cli
from ..api import _get, _list, _update
from ..output import output_result, output_message
from ..types import JSON


@cli.group(help='Account management.')
@click.pass_context
def account(ctx):
    pass

@account.command(name='info', help='Get account info.')
@click.pass_context
def get_info(ctx):
    _, result = _get(
        ctx.obj['access_token'], '/account'
    )
    output_result(ctx, result)

@account.command(name='update', help='Update the account.')
@click.option('--user-metadata', 'user_metadata', type=JSON, required=False, help='User metadata.')
@click.option('--app-metadata', 'app_metadata', type=JSON, required=False, help='App metadata.')
@click.pass_context
def update_info(ctx, user_metadata, app_metadata):
    data = {
        "user_metadata": user_metadata,
        "app_metadata": app_metadata
    }
    _, result = _update(ctx.obj['access_token'], 'account', data=data)
    output_result(ctx, result)

@account.command(name='reset-password', help='Reset password of the account.')
@click.pass_context
def reset_password(ctx):
    _update(ctx.obj['access_token'], 'account/reset-password')
    output_message('Reset password sent successfully!')


@account.command(name='roles', help='List roles of the account.')
@click.option('--query', '-q', 'query', type=str, required=False, help='Filter roles')
@click.option('--limit', '-l', 'limit', type=str, required=False, help='Limit the number of objects to return.')
@click.option('--offset', '-o', 'offset', type=str, required=False, help='Offset the objects.')
@click.pass_context
def list_roles(ctx, query, limit, offset):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query,
    }
    _, result = _list(
        ctx.obj['access_token'], 'account/roles', params=params
    )
    output_result(ctx, result)
