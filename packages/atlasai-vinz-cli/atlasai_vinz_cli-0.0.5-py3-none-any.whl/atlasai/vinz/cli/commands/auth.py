from .cli import cli
from ..auth import login as user_login
from ..config import write_access_token
from ..output import output_message


@cli.group(help='Authentication management.')
def auth():
    pass

@auth.command(name='login', help='Login method.')
def login():
    access_token = user_login()
    if access_token:
        write_access_token(access_token)
    else:
        output_message('Failed to login!')

@auth.command(name='logout', help='Logout method.')
def logout():
    write_access_token('')
    output_message('Finished logout!')
