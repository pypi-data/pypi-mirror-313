from http import HTTPStatus

import click

from .cli import cli
from ..api import _delete, _get, _list, _create, _update, _poll_response
from ..output import output_result, output_message
from ..types import JSON

@cli.group(help="Group management.")
@click.pass_context
def group(ctx):
    pass

@group.command(name='create', help='Create a Group.')
@click.option('--display-name', 'display_name', type=str, required=True, help='Friendly name of the group.')
@click.option('--name', 'name', type=str, required=True, help='The name of this group.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.pass_context
def create_group(ctx, display_name, name, org_id):
    data = {'display_name': display_name, 'name': name}
    params = {'org_id': org_id}
    _, result = _create(ctx.obj['access_token'], 'group', data=data, params=params)
    output_result(ctx, result)


@group.command(name='update', help='Update a Group.')
@click.option('--display-name', 'display_name', type=str, required=False, help='Friendly name of the group.')
@click.option('--name', 'name', type=str, required=False, help='The name of this group.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.pass_context
def update_group(ctx, display_name, name, org_id, group_id):
    data = {'display_name': display_name, 'name': name}
    params = {'org_id': org_id}
    _, result = _update(ctx.obj['access_token'], f'group/{group_id}', data=data, params=params)
    output_result(ctx, result)


@group.command(name='get', help='Get a Group.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.pass_context
def get_group(ctx, org_id, group_id):
    params = {'org_id': org_id}
    _, result = _get(ctx.obj['access_token'], f'group/{group_id}', params=params)
    output_result(ctx, result)

@group.command(name='delete', help='Delete a Group.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.pass_context
def delete_group(ctx, org_id, group_id):
    params = {'org_id': org_id}
    _delete(ctx.obj['access_token'], f'group/{group_id}', params=params)
    output_message('Group deleted successfully!')


@group.command(name='list', help='List Groups.')
@click.option('--query', '-q', 'query', type=str, required=False, help='Filter Groups')
@click.option('--limit', '-l', 'limit', type=str, required=False, help='Limit the number of objects to return.')
@click.option('--offset', '-o', 'offset', type=str, required=False, help='Offset the objects.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.pass_context
def list_groups(ctx, query, limit, offset, org_id):
    params = {
        'limit': limit,
        'offset': offset,
        'search': query,
        'org_id': org_id
    }
    _, result = _list(
        ctx.obj['access_token'], 'groups', params=params
    )
    output_result(ctx, result)


@group.group(help='User bulk operations')
@click.pass_context
def users(ctx):
    pass


@users.command(name='list', help='Retrieve users from a group.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.option('--query', '-q', 'query', type=str, required=False, help='Filter Organizations')
@click.option('--limit', '-l', 'limit', type=str, required=False, help='Limit the number of objects to return.')
@click.option('--offset', '-o', 'offset', type=str, required=False, help='Offset the objects.')
@click.pass_context
def list_users(ctx, org_id, group_id, limit, offset, query):
    params = {
        'org_id': org_id,
        'limit': limit,
        'offset': offset,
        'search': query
    }

    _, result = _list(
        ctx.obj['access_token'], f'group/{group_id}/users', params=params
    )
    output_result(ctx, result)


@users.command(name='add', help='Add users to a group.')
@click.option('--user', 'user_ids', multiple=True, type=str, required=True, help='Users to add. Pass this parameter multiple times for more than one user. ')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.pass_context
def add_users(ctx, user_ids, org_id, group_id):
    params = {'org_id': org_id}

    data = {'users': [u for u in user_ids]}
    _create(ctx.obj['access_token'], f'group/{group_id}/users', data=data, params=params)
    output_message('Users added to group successfully!')

@users.command(name='remove', help='Remove users from a group.')
@click.option('--user', 'user_ids', multiple=True, type=str, required=True, help='Users to add. Pass this parameter multiple times for more than one user. ')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.pass_context
def remove_users(ctx, user_ids, org_id, group_id):
    params = {'org_id': org_id}

    data = {'users': [u for u in user_ids]}
    _delete(ctx.obj['access_token'], f'group/{group_id}/users', data=data, params=params)
    output_message('Users removed from group successfully!')


@users.command(name='update', help='Update users in a group.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.option('--user-metadata', 'user_metadata', type=JSON, required=False, help='User metadata json.')
@click.option('--app-metadata', 'app_metadata', type=JSON, required=False, help='App metadata json.')
@click.option('--blocked', 'blocked', type=bool, required=False, help='Block status.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.pass_context
def update_users(ctx, app_metadata, user_metadata, blocked, org_id, group_id):
    data = {'action': 'group_update_users', 'data': {}}
    params = {'org_id': org_id}

    data['data'].update(
        {k: v for k, v in [('app_metadata', app_metadata), ('user_metadata', user_metadata), ('blocked', blocked)] if v})
    status_code, data = _update(ctx.obj['access_token'], f'group/{group_id}/users', data=data, params=params)
    if status_code == HTTPStatus.ACCEPTED:
        data = _poll_response(ctx.obj['access_token'], job_id=data)
    if data.get('status') == 'Finished':
        output_message('Users updated successfully!')
    else:
        output_message('Users failed to update!')


@users.command(name='add-roles', help='Add roles to all users of a group.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.option('--role', 'roles', multiple=True, type=str, required=True, help='Role ids. Add this parameter multiple times for multiple roles.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.pass_context
def add_roles(ctx, roles, org_id, group_id):
    data = {'action': 'group_add_roles', 'roles': roles}
    params = {'org_id': org_id}

    status_code, data = _update(ctx.obj['access_token'], f'group/{group_id}/users', data=data, params=params)
    if status_code == HTTPStatus.ACCEPTED:
        data = _poll_response(ctx.obj['access_token'], job_id=data)
    if data.get('status') == 'Finished':
        output_message('Roles added successfully!')
    else:
        output_message('Failed to add roles!')


@users.command(name='remove-roles', help='Remove roles from all users of a group.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.option('--role', 'roles', multiple=True, type=str, required=True, help='Role ids. Add this parameter multiple times for multiple roles.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.pass_context
def remove_roles(ctx, roles, org_id, group_id):
    data = {'action': 'group_remove_roles', 'roles': roles}
    params = {'org_id': org_id}

    status_code, data = _update(ctx.obj['access_token'], f'group/{group_id}/users', data=data, params=params)
    if status_code == HTTPStatus.ACCEPTED:
        data = _poll_response(ctx.obj['access_token'], job_id=data)
    if data.get('status') == 'Finished':
        output_message('Roles removed successfully!')
    else:
        output_message('Failed to remove roles!')


@users.command(name='reset-password', help='Reset password to all users of a group.')
@click.option('--org-id', 'org_id', type=str, required=False, help='Organization id to use. If not specified, it will return your own organization. This is the field org_id returned in the list method.')
@click.option('--group-id', 'group_id', type=str, required=True, help='The id of the group.')
@click.pass_context
def reset_password(ctx, org_id, group_id):
    data = {'action': 'group_reset_password'}
    params = {'org_id': org_id}

    status_code, data = _update(ctx.obj['access_token'], f'group/{group_id}/users', data=data, params=params)
    if status_code == HTTPStatus.ACCEPTED:
        data = _poll_response(ctx.obj['access_token'], job_id=data)
    if data.get('status') == 'Finished':
        output_message('Passwords reset successfully!')
    else:
        output_message('Failed to reset passwords!')
