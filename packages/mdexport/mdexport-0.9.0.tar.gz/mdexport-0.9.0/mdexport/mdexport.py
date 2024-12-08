import click
from pathlib import Path

from mdexport.cli import (
    validate_md_file,
    validate_output_file,
    generate_template_help,
    validate_template,
    validate_output_md,
)
from mdexport.markdown import read_md_file, convert_md_to_html, extract_md_metadata
from mdexport.templates import (
    fill_template,
    match_metadata_to_template,
    ExpectedMoreMetaDataException,
)
from mdexport.markdown import generate_empty_md
from mdexport.exporter import write_template_to_pdf
from mdexport.config import config, CONFIG_HELP


@click.group()
def cli():
    pass


@click.command()
@click.argument("markdown_file", type=str, callback=validate_md_file)
@click.option("--output", "-o", required=True, type=str, callback=validate_output_file)
@click.option(
    "--template",
    "-t",
    required=False,
    help=generate_template_help(),
    callback=validate_template,
)
def publish(markdown_file: str, output: str, template: str) -> None:
    """Publish Markdown files to PDF."""
    config.pre_publish_config_check()
    md_path = Path(markdown_file)
    md_content = read_md_file(md_path)
    html_content = convert_md_to_html(md_content, md_path)
    metadata = extract_md_metadata(Path(markdown_file))
    if template:
        try:
            match_metadata_to_template(template, metadata.keys())
        except ExpectedMoreMetaDataException as e:
            click.echo(f"!!!!! WARNING: {e}")
    filled_template = (
        fill_template(template, html_content, metadata) if template else html_content
    )
    write_template_to_pdf(template, filled_template, Path(output))


@click.command()
@click.argument(
    "output_file",
    required=True,
    type=str,
    callback=validate_output_md,
)
@click.option(
    "--template",
    "-t",
    help=generate_template_help(),
    required=True,
    callback=validate_template,
)
def empty_markdown(output_file: Path, template: str):
    """Create empty markdown files with the metadata fields in template."""
    generate_empty_md(output_file, template)


@click.group()
def options():
    """Manage MDExport options."""
    pass


@options.command()
def list():
    """List all available options."""
    click.echo("Available options:")
    for key, value in config.config.items():
        click.echo("")
        click.echo(f"   {key}: {value}")
        click.echo("")
        click.echo(CONFIG_HELP[key])


@options.command()
@click.argument("key")
@click.argument("value")
def set(key: str, value: str):
    """Set an option value."""
    config.set(key, value)
    config.save()
    click.echo(f"Succesfully set {key}: {value}")


cli.add_command(options)
cli.add_command(empty_markdown, "emptymd")
cli.add_command(publish)


if __name__ == "__main__":
    cli()
