import os
import subprocess
from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def setup_project(
    project_name: str,
    include_release_please: bool = typer.Option(False, help="Include Release Please"),
    create_env: bool = typer.Option(True, help="Create a virtual environment"),
):
    """
    Set up a new project from the template.
    """
    typer.echo(f"Setting up your project '{project_name}'...")

    # Ensure project directory does not already exist
    project_dir = Path(project_name)
    if project_dir.exists():
        typer.echo(f"Error: Directory {project_name} already exists!", err=True)
        raise typer.Exit(code=1)

    # Path to the Copier template
    template_dir = Path(__file__).parent / "template"

    # Generate project using Copier
    typer.echo("Generating project files...")
    subprocess.run(
        [
            "copier",
            "copy",
            str(template_dir),
            str(project_dir),
            f"--data=project_name={project_name}",
        ],
        check=True,
    )

    os.chdir(project_dir)

    if create_env:
        typer.echo("Creating virtual environment...")
        subprocess.run(["poetry", "env", "use", "python"], check=True)

    typer.echo("Installing dependencies...")
    subprocess.run(["poetry", "install"], check=True)

    if include_release_please:
        typer.echo("Setting up Release Please...")
        subprocess.run(["npm", "install", "-g", "release-please"], check=True)

    typer.echo("Project setup completed!")


if __name__ == "__main__":
    app()
