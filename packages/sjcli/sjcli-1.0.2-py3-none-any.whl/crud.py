import click
from datetime import datetime
import json
import os

@click.command()
@click.argument('title')
# @click.option("--version","-t",default=1,type=int)
# @click.option("--tags","-t",default=1,type=int)
@click.option("--tags","-t",help="Comma-seperated list of tags")
@click.option("--content","-c",prompt=True,help="Content of the note")
@click.pass_context
def create(ctx:click.Context,title:str,content:str,tags:str)->None:
    """Create a new note."""
    print("NOTES DIRECTORU", ctx.obj['notes_directory'])
    notes_directory="/Users/sj652744/notes"
    note_name=f"{title}.txt"
    if os.path.exists(os.path.join(notes_directory,note_name)):
        click.echo(f"Note with title {title} already exist.")
        exit(1)
    
    note_data={
        "content":content,
        "tags":tags.split(",") if tags else [],
        "created_at":datetime.now().isoformat(),
    }
    file_path=os.path.join(notes_directory,note_name)
    with open(file_path, "w") as file:
        click.echo("Creating... file")
        json.dump(note_data,file)
    click.echo(f"Note {title} created")