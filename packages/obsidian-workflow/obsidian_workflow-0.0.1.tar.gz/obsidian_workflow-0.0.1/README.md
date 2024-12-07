# Obsidian Workflow

Obsidian Workflow is a command line application to automate my obsidian workflows. This application is specific to my workflow and might not fit yours. See each command for more details.

## Commands

### Daily

The daily note in Obsidian serves as a scratchpad for capturing ideas and information throughout the day. Each train of thought is organized under a top-level heading and linked to relevant indexes, maps of content (MOCs), projects, and other atomic notes. This flexible approach allows for quick note-taking without worrying about where in the hierarchy to create a one. However, keeping content in the daily note creates an issue with backlinks, as references show the date (e.g., 2025-01-01-Monday) rather than descriptive titles, making them harder to recognize in linked mentions or unmapped backlink views. To resolve this, each top-level heading is extracted into its own standalone note with a meaningful name. This improves backlink readability and prepares the notes for migration to a folder in the permanent hierarchy when necessary during gardening.

Daily Note Format: YYYY/MM-MMMM/YYYY-MM-DD-dddd

See (Python Scripter Plugin directory)[./plugins/python scripter/README.md] for how to use this within the Obsidian application.

#### Process a Single File

```bash
obsidian-workflow daily --file /path/to/note.md
```

#### Process the Last `N` Days

To process the last 7 days of notes (excluding today):

```bash
obsidian-workflow daily --days 7 --root-dir /path/to/notes
```

#### Include Today in Processing

To include today’s note in the processing:

```bash
obsidian-workflow daily --days 7 --include-today --root-dir /path/to/notes
```

#### Default Behavior

Running the `daily` workflow without arguments processes today’s daily note:

```bash
obsidian-workflow daily
```

---

#### Examples

##### Input:

Daily note contains:

```markdown
# Header 1

Content A

# Header 1

Content B

# Header 2

Content C
```

##### Output:

**File: `header 1.md`**

```markdown
# Header 1

Content A

Extracted from: [[2024-12-05-Thursday]]

---

# Header 1

Content B

Extracted from: [[2024-12-05-Thursday]]
```

**File: `header 2.md`**

```markdown
# Header 2

Content C

Extracted from: [[2024-12-05-Thursday]]
```

**Daily Note After Processing**

```markdown
# Header 1

![[header 1.md]]

# Header 1

![[header 1.md]]

# Header 2

![[header 2.md]]
```

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/obsidian-workflow.git
   cd obsidian-workflow
   ```

2. Install the package:
   ```bash
   uv install .
   ```

## Development commands

After cloning

### Install packages

```sh
uv sync
```

### Run Tests

```sh
uv run pytest
```
