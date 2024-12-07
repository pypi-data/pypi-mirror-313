import json
from pathlib import Path

from neosctl.services.gateway import schema


def get_journal_note_filepath(tmp_path: Path):
    fp = tmp_path / "journal_note.json"
    with fp.open("w") as f:
        json.dump(
            schema.UpdateJournalNote(note="new note", owner="new owner").model_dump(),
            f,
        )

    return str(fp.resolve())
