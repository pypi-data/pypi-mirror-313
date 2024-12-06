import click

from rich.text import Text
from rich.syntax import Syntax

from ..config import get_access_token, get_config
from ..output import output_message


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand not in ['auth', 'config', 'info']:
        access_token = get_access_token()
        if not access_token:
            raise Exception('No access token found. Use:\n\nvinz-cli auth login')

        ctx.obj['access_token'] = f'Bearer {access_token}'
    ctx.obj['config'] = get_config()

@cli.command(help="General info.")
@click.pass_context
def info(ctx):
    output_message(Text("Vinz CLI Tool", style="bold underline magenta"))
    output_message("Welcome to the User Management Service CLI!\n")

    output_message(
        "This command-line interface (CLI) tool allows you to efficiently manage the resources in your vinz service. "
        "With this tool, you can perform various operations related to user management, including creating, updating, "
        "deleting, and listing users.\n")

    output_message(Text("Features:", style="bold underline"))
    output_message(
        "• Manage Users: Easily add/edit/remove or view users with necessary attributes such as username, email, and role.")
    output_message(
        "• Manage Roles: Create and manage user roles and permissions to control access within your application.")
    output_message(
        "• Manage Organizations: Create and manage organizations to control access and support bulk operations within your application.")
    output_message(
        "• Manage Groups: Create and manage groups to control access and support bulk operations within your application.\n")

    output_message(Text("Configurations:", style="bold underline"))
    output_message("You can customize your output format using the config command.")
    output_message("The following example allows you to see the results in a table format.\n")

    output_message(Syntax("vinz-cli config set output:table", "bash"))

    output_message(Text("\nHelp:", style="bold underline"))
    output_message("For detailed information about each command, you can use the help option:\n")
    output_message(Syntax("vinz-cli --help", "bash"))

    output_message(Text("\nSupport:", style="bold underline"))
    output_message(
        "If you encounter any issues or have questions, please refer to the documentation or reach out to our support team.\n")

    output_message(Text("Happy Managing!\n", style="bold blue"))

if __name__ == "__main__":
    cli()
