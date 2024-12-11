# ResTrack

Python application for results tracking

## Scope of MVP/PoC

### Logic

1. Identify user (admin)
2. Users create or subsrcibe to worklists
3. worklists can contain 0 or more orders
4. Orders can belong to 0 or more worklists
5. Link patient MRN to all investigations ordered - then choose test and add to worklist
6. Remove orders from worklist

### UI

1. Display list of orders and status - filter by worklist and other criteria

## Setup

_ToDo: Improve this section with better instructions on using [uv](https://docs.astral.sh/uv/) for managing all project dependencies._

1. Clone this repository
2. Create a new python environment e.g. `uv venv --python 3.12`
3. Activate the environment with `.venv/Scripts/activate`
4. Install project dependencies with `uv sync` (and use `uv add <package> to add any dependencies)
5. Install restrack as an editable project with `uv pip install -e .[dev]`
6. Install pre-commit using `pre-commit install`
7. Copy the `sample.env` file to a new file called `.env` and setup the environment variables here.


__IMPORTANT:__ DO NOT SAVE ANY SENSITIVE INFORMATION TO VERSION CONTROL

## Development

The application is split into two distinct components.

The _backend_ that interacts with OMOP and the application database is implemented using [FastAPI](https://fastapi.tiangolo.com/) and [SQLModel](https://sqlmodel.tiangolo.com/) and the code for this resides in `restrack/api/`.

The _user interface_ that displays the data and handles user interaction is implemented in [Panel](https://panel.holoviz.org/).

While this introduces some additional overhead during the development process, the clear separation of concerns lends itself to better maintainability and the ability to replace Panel with an alternate UI framework if required.

### Application Database

Restrack uses SQLite for ease of development but this can be easily replaced with any other SQLAlchemy-supported database. Sample data for populating the database is provided in `tests/synthetic_data`. A new SQLite database called `restrack.db` is created at first

### Development servers

During development, start the FastAPI server first. This will create the database. _(ToDo: Automate populating the database with sample data)_.

These are configured as [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks) in `.vscode/tasks.json`. If using a different IDE, run the commands in separate terminal sessions.

```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Panel Development Server",
            "type": "shell",
            "command": "panel serve ./restrack/ui/ui.py --global-loading-spinner --basic-auth ./data/users.json --cookie-secret restrack_secret --dev ",
            "problemMatcher": [
                "$python"
            ]
        },
        {
            "label": "FastAPI Development Server",
            "type": "shell",
            "command": "fastapi dev ./restrack/api/api.py",
            "problemMatcher": [
                "$python"
            ]
        },
    ]
}
```
