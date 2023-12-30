from datetime import datetime

import click
from click import Context

from spot_archive.cli.backups.liked_songs import backup_liked_songs
from spot_archive.cli.backups.playlists import backup_playlists
from spot_archive.constants import BACKUP_FOLDER_PREFIX


@click.group(chain=True, invoke_without_command=True)
@click.option(
    "--output",
    default=f"{BACKUP_FOLDER_PREFIX}-{datetime.now().strftime('%d-%m-%Y')}",
    help="Output folder to write backup files.",
)
@click.pass_context
def spot_archive_cli(ctx: Context, output: str):
    """Run spot-archive CLI."""

    click.echo(f"Backing up spotify data to '{output}'")

    if ctx.invoked_subcommand is None:
        available_subcommands = ctx.command.list_commands(ctx)
        for subcommand in available_subcommands:
            ctx.invoke(ctx.command.get_command(ctx, subcommand))


@spot_archive_cli.command()
@click.pass_context
def liked_songs(ctx: Context):
    backup_liked_songs(output_folder=ctx.parent.params["output"])


@spot_archive_cli.command()
@click.pass_context
def playlists(ctx: Context):
    backup_playlists(output_folder=ctx.parent.params["output"])


if __name__ == "__main__":
    spot_archive_cli()
