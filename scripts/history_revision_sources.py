"""Verify saved museum references; optionally fetch missing public display files.
Usage: python scripts/history_revision_sources.py [--download]
The authoritative registry includes institution, creator, date, rights and source URLs.
A downloadable display image is NOT an open-license declaration.
"""
from pathlib import Path
from PIL import Image
import json,sys,urllib.request
R=Path(__file__).resolve().parents[1]
records=json.loads((R/'references/revision-history-images.json').read_text())
for x in records:
 p=R/'assets/images'/x['file']
 if not p.exists() and '--download' in sys.argv and x['kind']=='real_artwork':
  b=urllib.request.urlopen(urllib.request.Request(x['image_url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read()
  tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(b);tmp.replace(p)
 if not p.exists():raise FileNotFoundError(p)
 with Image.open(p) as im: im.verify()
 with Image.open(p) as im: im.load()
print(f'Verified {len(records)} attributed reference and analysis images.')
