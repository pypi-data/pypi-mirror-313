from PatchTool.sos import sso
from PatchTool.acllm import full_file,Query
from PatchTool.acllm import AddComments,modif,extract_raw_code
import typer

app = typer.Typer()

@app.command()
def searcherr(filepath:str):
    sso(filepath=filepath)

@app.command()
def fix(filepath:str):
    full_file(filepath=filepath)

@app.command()
def modify(filepath:str):
    modif(filepath=filepath)

@app.command()
def query(filetype:str):
    Query(filetype)

@app.command()
def addComments(filepath:str):
    AddComments(filepath)

if __name__ == "__main__":
    app()



