"""Read the shared, validated chapter order without PDF or website dependencies."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load_book():
    book = json.loads((ROOT / 'book.json').read_text())
    chapters = [entry for part in book['parts'] for entry in part['chapters']]
    if [entry['number'] for entry in chapters] != list(range(1, len(chapters) + 1)):
        raise ValueError('Chapter numbers must be continuous in reading order')
    entries = [book['introduction'], *chapters, *book['appendices']]
    paths = []
    for entry in entries:
        relative = Path(entry['source'])
        source = (ROOT / relative).resolve()
        if relative.is_absolute() or '..' in relative.parts or not source.is_relative_to(ROOT) or not source.is_file():
            raise ValueError('Missing or unsafe source: ' + str(relative))
        paths.append(str(relative))
    expected = {str(p.relative_to(ROOT)) for folder in ('chapters', 'appendices') for p in (ROOT / folder).glob('*.md')}
    if len(paths) != len(set(paths)) or set(paths) != expected:
        raise ValueError('Manifest must cover every source exactly once')
    return book

def ordered_sources(book=None):
    book = book or load_book()
    return [ROOT / entry['source'] for entry in [book['introduction'], *(entry for part in book['parts'] for entry in part['chapters']), *book['appendices']]]

def part_starts(book=None):
    book = book or load_book()
    return {ROOT / part['chapters'][0]['source']: part for part in book['parts']}
