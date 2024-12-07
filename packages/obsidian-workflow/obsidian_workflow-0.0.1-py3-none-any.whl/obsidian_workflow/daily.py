import argparse
import click
import os
import re

from datetime import datetime, timedelta
from pathlib import Path


def sanitize_filename(file_name: str) -> str:
    """
    Sanitize a file name to ensure cross-platform compatibility.

    - Preserves spaces.
    - Replaces `:` and `|` with ` -`.
    - Replaces other reserved characters with an empty space.
    - Limits the file name to 255 characters.

    Args:
        file_name (str): The input file name to sanitize.

    Returns:
        str: The sanitized file name.
    """
    # Define reserved characters to replace with empty space
    reserved_chars = r'[\\/*?"<>]'
    # Replace `:` and `|` with ` -`
    file_name = re.sub(r"[:]", " -", file_name)
    file_name = re.sub(r"[|]", "-", file_name)
    # Replace other reserved characters with an empty space
    file_name = re.sub(reserved_chars, "", file_name)
    # Trim to a maximum of 255 characters
    return file_name[:255].lower().strip()


def process_daily_note(filepath):
    """Processes a daily note file to extract sections into separate files."""
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # Find all top-level headings
    sections = re.split(r"(?m)^# ", content)
    processed_sections = []
    daily_note_path = Path(filepath)
    daily_note_name = daily_note_path.stem

    if sections[0].strip():
        # Preserve content before the first header, if any
        processed_sections.append(sections[0])

    new_content = []
    files_written = set()  # Track files written during this processing pass

    for section in sections[1:]:
        # Split the section into title and body
        if "\n" in section:
            title, body = section.split("\n", 1)
        else:
            title, body = section, ""

        title = title.strip()
        body = body.strip()

        # Detect YAML front matter
        front_matter = ""
        if body.startswith("---"):
            front_matter_end = body.find("\n---", 4)
            if front_matter_end != -1:
                front_matter = body[: front_matter_end + 4].strip()
                body = body[front_matter_end + 4 :].strip()

        # Create the sanitized filename
        filename = sanitize_filename(title) + ".md"
        extracted_path = daily_note_path.parent / filename

        if extracted_path.exists():
            # If the file exists and we've already written to it in this pass, append the content
            if extracted_path in files_written:
                with open(extracted_path, "a", encoding="utf-8") as extracted_file:
                    extracted_file.write("\n---\n\n")
                    if front_matter:
                        extracted_file.write(f"{front_matter}\n\n")
                    extracted_file.write(f"{body}\n\n")
                    extracted_file.write(f"Extracted from: [[{daily_note_name}]]\n")
            else:
                # Skip processing if the file exists but wasn't written in this pass
                with open(extracted_path, "r", encoding="utf-8") as extracted_file:
                    existing_content = extracted_file.read()
                    if f"Extracted from: [[{daily_note_name}]]" in existing_content:
                        new_content.append(f"# {title}\n\n![[{filename}]]\n")
                        continue
        else:
            # Write the section to its own file
            with open(extracted_path, "w", encoding="utf-8") as extracted_file:
                if front_matter:
                    extracted_file.write(f"{front_matter}\n\n")
                extracted_file.write(f"# {title}\n\n")
                extracted_file.write(f"{body}\n\n")
                extracted_file.write(f"Extracted from: [[{daily_note_name}]]\n")

            # Mark the file as written during this pass
            files_written.add(extracted_path)

        # Add a newline between the header and the backlink
        new_content.append(f"# {title}\n\n![[{filename}]]\n")

    # Write back to the daily file with backlinks
    with open(filepath, "w", encoding="utf-8") as file:
        file.write("\n".join(processed_sections + new_content))
        file.write("\n".join(processed_sections + new_content))


def process_days(root_dir, days, include_today):
    """Processes multiple days of daily notes."""
    today = datetime.today()
    for i in range(days + (1 if include_today else 0)):
        target_date = today - timedelta(days=i)
        path = Path(root_dir) / target_date.strftime("%Y/%m-%B/%Y-%m-%d-%A.md")
        if path.exists():
            process_daily_note(path)


@click.command("daily", short_help="Extracts sections from daily notes into separate files.")
@click.option(
    "--file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Single file path to process (e.g., <daily_note_path>/YYYY/MM-MMMM/YYYY-MM-DD-dddd.md).",
)
@click.option(
    "--days",
    type=int,
    help="Number of days back to process (excluding today).",
)
@click.option(
    "--include-today",
    is_flag=True,
    help="Include today in processing.",
)
@click.option(
    "--root-dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path("."),
    help="Root directory for daily notes.",
)
def daily_cli(file, days, include_today, root_dir):
    """Process daily notes based on the provided options."""
    if file:
        process_daily_note(file)
    elif days is not None:
        process_days(root_dir, days, include_today)
    else:
        # Default behavior: process today's file
        today_path = root_dir / datetime.today().strftime("%Y/%m-%B/%Y-%m-%d-%A.md")
        if today_path.exists():
            process_daily_note(today_path)
        else:
            click.echo(f"Today's file does not exist: {today_path}")
