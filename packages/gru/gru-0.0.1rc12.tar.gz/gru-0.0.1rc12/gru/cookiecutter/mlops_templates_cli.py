"""
This script defines a command-line interface (CLI) to generate standardised folder structures for ML problem statements.
The design is inspired from Cookiecutter and has been modified to adapt to Yugen's ML deployment stack.
"""
import click
import subprocess

EXPECTED_TEMPLATE_URL = "https://github.com/Yugen-ai/cookiecutter-mlops-templates.git"


@click.command()
@click.option(
    "--template",
    default="https://github.com/Yugen-ai/cookiecutter-mlops-templates.git",
    help="Cookiecutter template URL",
)
@click.option(
    "--output-dir", default=".", help="Output directory for the generated project"
)
def mlops_template_cli(template, output_dir):
    """
    Run Cookiecutter with the specified template.

    Args:
        template (str): Cookiecutter template URL.
        output_dir (str): Output directory for the generated project.
    """
    if template != EXPECTED_TEMPLATE_URL:
        click.echo(f'Error: Only the template "{EXPECTED_TEMPLATE_URL}" is supported.')
        return

    click.echo(f"Running Cookiecutter with template: {template}")
    click.echo(f"Output directory: {output_dir}")

    try:
        subprocess.run(
            ["cookiecutter", template, "--output-dir", output_dir], check=True
        )
        click.echo("Cookiecutter completed successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running Cookiecutter: {e}")


if __name__ == "__main__":
    mlops_template_cli()
