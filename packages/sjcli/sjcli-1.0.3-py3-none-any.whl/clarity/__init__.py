import click
from .enums import ClarityFiles
from .parsers import parse_app_access

__all__=[
    "parse_app_access"
]

@click.command(name="parse-app")
@click.argument("filename",type=click.Path(exists=True))
@click.argument("output",type=click.Path(exists=True,file_okay=False))
@click.option(
    "-p",
    "--prefix",
    default="app-access",
    help="The file prefix to search if the filename is path to directory"
)
@click.option(
    "-i",
    "--ignore",
    default=".csv",
    help="The file extension to be ignore while searching directory matching criteria defined in 'prefix'"
)
def parse(filename:str,output:str,prefix:str, ignore:str):
    """Parse the app-access file/ files into csv.
    It removes all the lines which are without any HTTP operations
    
    filename: Path to app-access.*.log or directory containing app-access.*.log.
    output: Path to the output directory.
    prefix: File prefix to search in directory. Example app-access
    ignore: The extension to ignore. Example .csv
    """
    click.echo(filename)
    click.echo(output)
    click.echo(prefix)
    click.echo(ignore)
    parse_app_access(filepath=filename,output_dir=output,file_prefix=prefix,ignore_extension=ignore)


@click.command(name="sessions")
def sessions():
    """Get session details from csv file parsed by 'access'
    """

@click.group
def clarity()->None:
    """ Clarity CLI commands
    
    """

clarity.add_command(parse)
clarity.add_command(sessions)