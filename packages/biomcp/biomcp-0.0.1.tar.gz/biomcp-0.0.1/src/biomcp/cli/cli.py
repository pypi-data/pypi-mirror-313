import typer

app = typer.Typer(
    name="biomcp",
    help="BioMCP development tools",
    add_completion=False,
    no_args_is_help=True,  # Show help if no args provided
)

@app.command()
def version() -> None:
    """Show the BioMCP version."""
    try:
        version = importlib.metadata.version("biomcp")
        print(f"BioMCP version {version}")
    except importlib.metadata.PackageNotFoundError:
        print("BioMCP version unknown (package not installed)")
        sys.exit(1)
