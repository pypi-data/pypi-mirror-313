import typer
from csra import __version__

app = typer.Typer()

@app.command()
def version():
    typer.echo(__version__)

@app.command()
def query(query_text: str):
    typer.echo(f"Received query: {query_text}")

def main():
    app()

if __name__ == "__main__":
    app()
