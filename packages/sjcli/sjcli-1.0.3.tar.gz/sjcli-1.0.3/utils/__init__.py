import click
from .decorators import pprint
from .enums import TableFormat
from .file_helpers import write_csv_data,write_log, preview_json,preview_csv
from .helpers import build_filename_from_path,get_files_path,get_timestamp_stats_from_csv
__all__=[
    "pprint",
    "write_csv_data",
    "write_log",
    "build_filename_from_path",
    "get_files_path",
    "get_timestamp_stats_from_csv"
]

# JSON viewer
@click.command(name="json")
@click.argument("file_name",type=click.Path(exists=True,dir_okay=False))
@click.option("-n","--numlines",default=None,type=click.IntRange(1),help="Number of lines to display. Omit to view the entire file")
@click.option("-i","--indent",type=click.IntRange(0),default=4,help="Specifies the indentation level to view JSON object")
def view_json(file_name,numlines,indent):
    """Use FILE_NAME to specify path to JSON file to preview"""
    result = preview_json(file_name=file_name,first_n=numlines,indent=indent)
    click.echo(result)

@click.command(name="csv")
@click.argument("file_name",type=click.Path(exists=True,dir_okay=False))
@click.option("-n","--numlines",default=None,type=click.IntRange(1),help="Number of lines to display. Omit to view the entire file")
@click.option("--has-header","hasheader",is_flag=True,help="Specify this flag is CSV file has header",default=False)
@click.option("--format","-f","format_",default=TableFormat.fancy_outline.name,type=click.Choice([e.name for e in TableFormat],case_sensitive=True), help="The formatting style")
def view_csv(file_name,numlines,hasheader,format_):
    """Use FILE_NAME to specify path to CSV file to preview"""
    format_=TableFormat[format_]
    result=preview_csv(file_name=file_name,first_n=numlines,has_header_row=hasheader,table_format=format_)
    click.echo(result)

# Group name utils
@click.group
def utils():
    """Collections of utility functionsl like -> view_csv,view_json
    
    view_csv: To view CSV
    view_json: to view JSON object
    """
# adding command to groups i.e. view_json and view_csv
utils.add_command(view_json)
utils.add_command(view_csv)

