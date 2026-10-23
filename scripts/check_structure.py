#!/usr/bin/env python3
"""Validate the shared reading order, chapter headings, case locations and images."""
import json
import re
from pathlib import Path
from book_manifest import ROOT, load_book, ordered_sources

def main():
    book = load_book()
    errors = []
    chapters = [entry for part in book['parts'] for entry in part['chapters']]
    for entry in chapters:
        actual = (ROOT / entry['source']).read_text().splitlines()[0]
        expected = f"# 第{entry['number']:02}章｜{entry['title']}"
        if actual != expected:
            errors.append({'source': entry['source'], 'expected_heading': expected, 'actual_heading': actual})
    cases = {'reddit':'11-brand','spotify':'12-editorial','pepsi':'29-packaging','decathlon':'24-fashion','config':'13-wayfinding','wise':'18-digital'}
    for brand, stem in cases.items():
        source = ROOT / 'chapters' / (stem + '.md')
        if '{#case-' + brand + '}' not in source.read_text():
            errors.append({'source': str(source.relative_to(ROOT)), 'missing_case_anchor': brand})
    images = []
    for source in ordered_sources(book):
        for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', source.read_text()):
            if target.startswith(('https:', 'http:', 'data:')):
                continue
            image = (source.parent / target).resolve()
            if not image.is_relative_to(ROOT) or not image.is_file():
                errors.append({'source': str(source.relative_to(ROOT)), 'missing_image': target})
            else:
                images.append(str(image.relative_to(ROOT)))
    report = {'edition': book['edition'], 'parts': len(book['parts']), 'chapters': len(chapters), 'source_sections': len(ordered_sources(book)), 'ordered_sources': [str(p.relative_to(ROOT)) for p in ordered_sources(book)], 'image_uses': len(images), 'unique_image_sources': len(set(images)), 'case_destinations': cases, 'errors': errors}
    (ROOT / 'build').mkdir(exist_ok=True)
    (ROOT / 'build/structure-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))

if __name__ == '__main__':
    main()
