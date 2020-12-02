from uuid import uuid4
import os
import json
from glob import glob

from package.api.constants import NOTE_DIR

def get_notes():
    notes = []
    fichiers = glob(os.path.join(NOTE_DIR, "*.json"))
    for fichier in fichiers:
        with open(fichier, "r") as f:
            note_data = json.load(f)
            note_uuid = os.path.splitext(os.path.basename(fichier))[0]
            note_title = note_data.get("title")
            note_content = note_data.get("content")
            note = Note(uuid=note_uuid, title=note_title, content=note_content)
            notes.append(note)

    return notes

class Note:
    def __init__(self, title="", content="", uuid=None):
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = str(uuid4())

        self.title = title
        self.content = content

    def __repr__(self):
        return f"{self.title} ({self.uuid})"

    def __str__(self):
        return self.title


    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content = value
        else:
            raise TypeError("Valeur invalide (besoin de chaine de carractere).")

    def delete(self):
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return True

    @property
    def path(self):
        return os.path.join(NOTE_DIR, self.uuid + ".json")

    def save(self):
        if not os.path.exists(NOTE_DIR):
            os.makedirs(NOTE_DIR)

        date = {"title": self.title, "content": self.content}
        with open(self.path, "w") as f:
            json.dump(date, f, indent=4)


if __name__ == '__main__':
    notes = get_notes()
    print(notes)