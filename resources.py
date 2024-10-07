import os
import json


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries == None:
            self.entries = []
        self.title = title
        self.parent = parent

    def __str__(self):
        return f"{self.title}"

    def add_entry(self, entry):
        entry.parent = self
        self.entries.append(entry)

    def print_entries(self, indent=0):
        self.print_with_indent(indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def print_with_indent(value, indent=0):
        spaces = '\t' * indent
        print(f"{spaces}{value}")

    def json(self):
        res = {
            "title": self.title,
            "entries": [x.json() for x in self.entries]
        }
        return res

    @classmethod
    def from_json(cls, value):
        new_entry = Entry(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    def save(self, path):
        fullpath = os.path.join(path, f'{self.title}.json')
        with open(fullpath, 'w', encoding='utf-8') as file:
            json.dump(self.json(), file)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            content = json.load(file)
        return cls.from_json(content)


class EntryManager:
    def __init__(self, data_path: str):
        self.entries = []
        self.data_path = data_path

    def add_entry(self, title: str):
        self.entries.append(Entry(title))

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for file in os.listdir(self.data_path):
            if file.endswith('json'):
                self.entries.append(Entry.load(os.path.join(self.data_path, file)))
