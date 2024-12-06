# Main executable
import typer
import sys

app = typer.Typer(name="Sep")


@app.command()
def main(delimiter: str = ":"):
    # We want to take the standard input as a string then split it
    input_data = sys.stdin.read().strip()
    split_data = input_data.split(delimiter)
    # Then print
    for s in split_data:
        print(s)


if __name__ == "__main__":
    app()
