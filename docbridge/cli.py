"""
Command-line interface for DocBridge
"""
import sys
import os
from pathlib import Path
from typing import Optional, List

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from . import __version__
from .converters.word import WordConverter
from .converters.excel import ExcelConverter
from .converters.powerpoint import PowerPointConverter
from .styles.default import DefaultStyle
from .utils import format_file_size, count_markdown_elements

console = Console()


def print_banner():
    """Print application banner."""
    banner = Text()
    banner.append("🚀 ", style="bold yellow")
    banner.append("DocBridge", style="bold cyan")
    banner.append(f" v{__version__}", style="dim")
    console.print(banner)
    console.print("   Convert Markdown to Office documents with AI dialog support\n", style="dim")


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="docbridge")
@click.pass_context
def main(ctx):
    """DocBridge - Markdown to Office Document Converter"""
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("[yellow]Usage:[/yellow] docbridge [COMMAND] [OPTIONS]")
        console.print("\n[green]Commands:[/green]")
        console.print("  convert    Convert Markdown file to Office document")
        console.print("  batch      Batch convert multiple files")
        console.print("  analyze    Analyze Markdown file structure")
        console.print("\n[blue]Run 'docbridge --help' for more information.[/blue]")


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file', type=click.Path(),
              help='Output file path')
@click.option('-f', '--format', 'output_format',
              type=click.Choice(['docx', 'xlsx', 'pptx', 'auto'], case_sensitive=False),
              default='auto',
              help='Output format (default: auto-detect from extension)')
@click.option('--style', 'style_file', type=click.Path(exists=True),
              help='Custom style configuration file (YAML)')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
def convert(input_file: str, output_file: Optional[str], output_format: str,
            style_file: Optional[str], verbose: bool):
    """Convert Markdown file to Office document"""
    print_banner()

    input_path = Path(input_file)

    # Determine output format
    if output_format == 'auto':
        if output_file:
            ext = Path(output_file).suffix.lower()
            if ext in ['.docx', '.xlsx', '.pptx']:
                output_format = ext[1:]
            else:
                output_format = 'docx'  # Default
        else:
            output_format = 'docx'

    # Load custom style if provided
    style = DefaultStyle()
    if style_file:
        import yaml
        with open(style_file, 'r') as f:
            style_data = yaml.safe_load(f)
            style = DefaultStyle.from_dict(style_data)

    # Create converter
    converters = {
        'docx': WordConverter,
        'xlsx': ExcelConverter,
        'pptx': PowerPointConverter,
    }

    converter_class = converters.get(output_format, WordConverter)
    converter = converter_class(style)

    # Determine output path
    if not output_file:
        output_file = str(input_path.with_suffix(f'.{output_format}'))

    # Show conversion info
    console.print(f"[green]Input:[/green]  {input_path}")
    console.print(f"[green]Output:[/green] {output_file}")
    console.print(f"[green]Format:[/green] {output_format.upper()}")
    console.print()

    # Perform conversion
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Converting...", total=None)

            result_path = converter.convert_file(input_path, output_file)

            progress.update(task, completed=True)

        # Show result
        output_path = Path(result_path)
        file_size = output_path.stat().st_size

        console.print(f"\n[green]✓ Conversion successful![/green]")
        console.print(f"[dim]Output:[/dim] {output_path}")
        console.print(f"[dim]Size:[/dim]   {format_file_size(file_size)}")

    except Exception as e:
        console.print(f"\n[red]✗ Conversion failed:[/red] {str(e)}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


@main.command()
@click.argument('input_files', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('-o', '--output-dir', 'output_dir', type=click.Path(),
              help='Output directory')
@click.option('-f', '--format', 'output_format',
              type=click.Choice(['docx', 'xlsx', 'pptx'], case_sensitive=False),
              default='docx',
              help='Output format (default: docx)')
@click.option('--style', 'style_file', type=click.Path(exists=True),
              help='Custom style configuration file (YAML)')
def batch(input_files: List[str], output_dir: Optional[str], output_format: str,
          style_file: Optional[str]):
    """Batch convert multiple Markdown files"""
    print_banner()

    # Setup output directory
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    # Load custom style if provided
    style = DefaultStyle()
    if style_file:
        import yaml
        with open(style_file, 'r') as f:
            style_data = yaml.safe_load(f)
            style = DefaultStyle.from_dict(style_data)

    # Create converter
    converters = {
        'docx': WordConverter,
        'xlsx': ExcelConverter,
        'pptx': PowerPointConverter,
    }
    converter_class = converters.get(output_format, WordConverter)
    converter = converter_class(style)

    # Process files
    console.print(f"[green]Batch converting {len(input_files)} files...[/green]\n")

    results = []
    with Progress(console=console) as progress:
        task = progress.add_task("Converting...", total=len(input_files))

        for input_file in input_files:
            input_path = Path(input_file)
            output_file = output_path / input_path.with_suffix(f'.{output_format}').name

            try:
                result = converter.convert_file(input_path, output_file)
                file_size = Path(result).stat().st_size
                results.append({
                    'input': input_path.name,
                    'output': output_file.name,
                    'status': 'success',
                    'size': file_size
                })
            except Exception as e:
                results.append({
                    'input': input_path.name,
                    'output': output_file.name,
                    'status': 'failed',
                    'error': str(e)
                })

            progress.advance(task)

    # Show results
    table = Table(title="Batch Conversion Results")
    table.add_column("Input", style="cyan")
    table.add_column("Output", style="green")
    table.add_column("Status", style="bold")
    table.add_column("Size", justify="right")

    for result in results:
        status_color = "green" if result['status'] == 'success' else "red"
        status_text = "✓" if result['status'] == 'success' else "✗"
        size_text = format_file_size(result['size']) if result['status'] == 'success' else "-"

        table.add_row(
            result['input'],
            result['output'],
            f"[{status_color}]{status_text}[/{status_color}]",
            size_text
        )

    console.print()
    console.print(table)

    # Summary
    success_count = sum(1 for r in results if r['status'] == 'success')
    console.print(f"\n[green]Success:[/green] {success_count}/{len(input_files)}")


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
def analyze(input_file: str):
    """Analyze Markdown file structure"""
    print_banner()

    input_path = Path(input_file)

    # Read file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Analyze
    stats = count_markdown_elements(content)

    # Display
    console.print(f"[green]File:[/green] {input_path}")
    console.print(f"[green]Size:[/green] {format_file_size(input_path.stat().st_size)}")
    console.print()

    table = Table(title="Markdown Structure Analysis")
    table.add_column("Element", style="cyan")
    table.add_column("Count", justify="right", style="green")

    element_names = {
        'headings': 'Headings',
        'code_blocks': 'Code Blocks',
        'inline_code': 'Inline Code',
        'tables': 'Tables',
        'links': 'Links',
        'images': 'Images',
        'bold': 'Bold Text',
        'italic': 'Italic Text',
    }

    for key, name in element_names.items():
        table.add_row(name, str(stats.get(key, 0)))

    console.print(table)


if __name__ == '__main__':
    main()
