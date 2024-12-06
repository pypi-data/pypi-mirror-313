import click

from .cli import cli
from ..api import _delete, _get, _list, _create, _update
from ..output import output_result, output_message
from ..types import JSON


@cli.group(help='User management.')
@click.pass_context
def user(ctx):
    pass

@user.command(name='list', help='List Users.')
@click.option('--query', '-q', 'query', type=str, required=False, help='Filter users')
@click.option('--limit', '-l', 'limit', type=str, required=False, help='Limit the number of objects to return.')
@click.option('--offset', '-o', 'offset', type=str, required=False, help='Offset the objects.')
@click.pass_context
def list_users(ctx, query, limit, offset):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query,
    }
    _, result = _list(
        ctx.obj['access_token'], 'users', params=params
    )
    output_result(ctx, result, no_wrap_columns=['user_id'])


@user.command(name='create', help='Create an User.')
@click.option('--email', 'email', type=str, required=True, help='Email of the user')
@click.option('--given-name', 'given_name', type=str, required=True, help='Given name.')
@click.option('--family-name', 'family_name', type=str, required=True, help='Family name.')
@click.option('--user-metadata', 'user_metadata', type=JSON, required=False, help='User metadata.')
@click.option('--app-metadata', 'app_metadata', type=JSON, required=False, help='App metadata.')
@click.option('--nickname', 'nickname', type=str, required=False, help='Nickname.')
@click.option('--blocked', 'blocked', type=bool, required=False, help='Boolean.')
@click.option('--password', 'password', type=str, required=False, help='Password. If password is not provided, one will be auto-generated.')
@click.option('--skip-email', 'skip_email', is_flag=True, show_default=True, default=False, help='Skip to send the reset password email after the account was created.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.pass_context
def create_user(ctx, email, given_name, family_name, user_metadata, app_metadata, nickname, blocked, password, skip_email, org_id):
    data = {
        "email": email,
        "given_name": given_name,
        "family_name": family_name,
        "user_metadata": user_metadata,
        "app_metadata": app_metadata,
        "nickname": nickname,
        "blocked": blocked,
        "password": password,
        "skip_email": skip_email
    }
    params = {'org_id': org_id}
    _, result = _create(ctx.obj['access_token'], 'user', data=data, params=params)
    output_result(ctx, result)


@user.command(name='update', help='Update an User.')
@click.option('--email', 'email', type=str, required=False, help='Email of the user')
@click.option('--given-name', 'given_name', type=str, required=False, help='Given name.')
@click.option('--family-name', 'family_name', type=str, required=False, help='Family name.')
@click.option('--user-metadata', 'user_metadata', type=JSON, required=False, help='User metadata.')
@click.option('--app-metadata', 'app_metadata', type=JSON, required=False, help='App metadata.')
@click.option('--nickname', 'nickname', type=str, required=False, help='Nickname.')
@click.option('--blocked', 'blocked', type=bool, required=False, help='Boolean.')
@click.option('--user-id', 'user_id', type=str, required=False, help='User id to update. This is the field user_id returned in the list method.')
@click.pass_context
def update_user(ctx, email, given_name, family_name, user_metadata, app_metadata, nickname, blocked, user_id):
    data = {
        "email": email,
        "given_name": given_name,
        "family_name": family_name,
        "user_metadata": user_metadata,
        "app_metadata": app_metadata,
        "nickname": nickname,
        "blocked": blocked,
    }
    _, result = _update(ctx.obj['access_token'], f'user/{user_id}', data=data)
    output_result(ctx, result)


@user.command(name='get', help='Get an User.')
@click.option('--user-id', 'user_id', type=str, required=True, help='The id of the user. This field is the user_id field from get/list')
@click.pass_context
def get_user(ctx, user_id):
    _, result = _get(ctx.obj['access_token'], f'user/{user_id}')
    output_result(ctx, result)


@user.command(name='delete', help='Delete an User.')
@click.option('--user-id', 'user_id', type=str, required=True, help='The id of the user. This field is the user_id field from get/list')
@click.pass_context
def delete_user(ctx, user_id):
    _delete(ctx.obj['access_token'], f'user/{user_id}')
    output_message('User deleted successfully!')


@user.command(name='reset-password', help='Reset password of an User.')
@click.option('--user-id', 'user_id', type=str, required=True, help='The id of the user. This field is the user_id field from get/list')
@click.pass_context
def reset_password(ctx, user_id):
    _update(ctx.obj['access_token'], f'user/{user_id}/reset-password')
    output_message('Reset password sent successfully!')

@user.group(help='User Role management.')
@click.pass_context
def role(ctx):
    pass

@role.command(name='add', help='Add roles to an User.')
@click.option('--user-id', 'user_id', type=str, required=True, help='The id of the user. This field is the user_id field from get/list')
@click.option('--role', 'roles', multiple=True, type=str, required=True, help='Role ids. Add this parameter multiple times for multiple roles.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.pass_context
def add_roles(ctx, roles, user_id, org_id):
    params = {'org_id': org_id}
    data = {'roles': roles}
    _create(ctx.obj['access_token'], f'user/{user_id}/roles', data=data, params=params)
    output_message('Roles added successfully!')


@role.command(name='remove', help='Remove roles from an User.')
@click.option('--user-id', 'user_id', type=str, required=True, help='The id of the user. This field is the user_id field from get/list')
@click.option('--role', 'roles', multiple=True, type=str, required=True, help='Role ids. Add this parameter multiple times for multiple roles.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.pass_context
def remove_roles(ctx, roles, user_id, org_id):
    params = {'org_id': org_id}
    data = {'roles': roles}
    _delete(ctx.obj['access_token'], f'user/{user_id}/roles', data=data, params=params)
    output_message('Roles removed successfully!')

@role.command(name='list', help='List roles of an User.')
@click.option('--user-id', 'user_id', type=str, required=True, help='The id of the user. This field is the user_id field from get/list')
@click.option('--query', '-q', 'query', type=str, required=False, help='Filter roles')
@click.option('--limit', '-l', 'limit', type=str, required=False, help='Limit the number of objects to return.')
@click.option('--offset', '-o', 'offset', type=str, required=False, help='Offset the objects.')
@click.pass_context
def list_roles(ctx, user_id, query, limit, offset):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query,
    }
    _, result = _list(
        ctx.obj['access_token'], f'user/{user_id}/roles', params=params
    )
    output_result(ctx, result)
