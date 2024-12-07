import tempfile

from freezegun import freeze_time
from obsidian_workflow.daily import process_daily_note, sanitize_filename
from pathlib import Path


def test_sanitize_filename():
    assert sanitize_filename("Header: Example | Test") == "header - example - test"
    assert sanitize_filename("Invalid/Characters<>") == "invalidcharacters"
    assert sanitize_filename("Leading and trailing  ") == "leading and trailing"


@freeze_time("2024-12-05")
def test_process_single_daily_note_with_heading():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up a mock daily note
        daily_note_path = Path(temp_dir) / "2024" / "12-December" / "2024-12-05-Thursday.md"
        daily_note_path.parent.mkdir(parents=True)
        daily_note_path.write_text("# Header 1\nContent A\n\n")

        # Process the note
        process_daily_note(daily_note_path)

        # Validate generated files
        header1_path = daily_note_path.parent / "header 1.md"

        assert header1_path.exists()

        assert header1_path.read_text() == ("# Header 1\n\nContent A\n\nExtracted from: [[2024-12-05-Thursday]]\n")


@freeze_time("2024-12-05")
def test_process_single_daily_note_with_headings():
    # Tests a file with two different headings
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up a mock daily note
        daily_note_path = Path(temp_dir) / "2024" / "12-December" / "2024-12-05-Thursday.md"
        daily_note_path.parent.mkdir(parents=True)
        daily_note_path.write_text("# Header 1\nContent A\n\n# Header 2\nContent C\n")

        # Process the note
        process_daily_note(daily_note_path)

        # Validate generated files
        header1_path = daily_note_path.parent / "header 1.md"
        header2_path = daily_note_path.parent / "header 2.md"

        assert header1_path.exists()

        assert header1_path.read_text() == ("# Header 1\n\nContent A\n\nExtracted from: [[2024-12-05-Thursday]]\n")

        assert header2_path.read_text() == ("# Header 2\n\nContent C\n\nExtracted from: [[2024-12-05-Thursday]]\n")


@freeze_time("2024-12-05")
def test_process_daily_note_with_front_matter():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up a mock daily note
        daily_note_path = Path(temp_dir) / "2024" / "12-December" / "2024-12-05-Thursday.md"
        daily_note_path.parent.mkdir(parents=True)
        daily_note_path.write_text("# Header 1\n---\ntitle: titleA\n---\nContent A\n")

        # Process the note
        process_daily_note(daily_note_path)

        # Validate generated files
        header1_path = daily_note_path.parent / "header 1.md"

        assert header1_path.exists()

        assert header1_path.read_text() == (
            "---\ntitle: titleA\n---\n\n" "# Header 1\n\nContent A\n\nExtracted from: [[2024-12-05-Thursday]]\n"
        )


@freeze_time("2024-12-05")
def test_process_single_daily_note_complex():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up a mock daily note
        daily_note_path = Path(temp_dir) / "2024" / "12-December" / "2024-12-05-Thursday.md"
        daily_note_path.parent.mkdir(parents=True)
        daily_note_path.write_text("# Header 1\nContent A\n\n# Header 1\nContent B\n\n# Header 2\nContent C\n")

        # Process the note
        process_daily_note(daily_note_path)

        # Validate generated files
        header1_path = daily_note_path.parent / "header 1.md"
        header2_path = daily_note_path.parent / "header 2.md"

        assert header1_path.exists()
        assert header2_path.exists()
        print(header1_path.read_text())
        assert header1_path.read_text() == (
            "# Header 1\n\nContent A\n\nExtracted from: [[2024-12-05-Thursday]]\n\n"
            "---\n\n"
            "Content B\n\n"
            "Extracted from: [[2024-12-05-Thursday]]\n"
        )

        assert header2_path.read_text() == ("# Header 2\n\nContent C\n\nExtracted from: [[2024-12-05-Thursday]]\n")

        # Process the note again to test idempotency
        process_daily_note(daily_note_path)

        assert header1_path.read_text() == (
            "# Header 1\n\nContent A\n\nExtracted from: [[2024-12-05-Thursday]]\n\n"
            "---\n\n"
            "Content B\n\n"
            "Extracted from: [[2024-12-05-Thursday]]\n"
        )

        assert header2_path.read_text() == ("# Header 2\n\nContent C\n\nExtracted from: [[2024-12-05-Thursday]]\n")
