from http import HTTPStatus
import click

from .cli import cli
from ..api import _create, _poll_response
from ..output import output_message


@cli.command(name='run', help='Run script management.')
@click.option('--script', 'script', type=str, required=True, help='Script to run')
@click.option('--api-key', 'api_key', type=str, required=True, help='Api key to use')
def run(script, api_key):
    data = {'action': script}
    status_code, result = _create(api_key, 'run', method='post', data=data)
    output_message('Script started...')
    if status_code == HTTPStatus.ACCEPTED:
        data = _poll_response(api_key, path='run', job_id=result)
        if data.get('status') == 'Finished':
            output_message('Script run successfully!')
        else:
            output_message('Script failed!')
