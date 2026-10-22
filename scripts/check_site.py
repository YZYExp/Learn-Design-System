#!/usr/bin/env python3
"""Check all generated pages, local assets and internal link fragments."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'build/site'
class Page(HTMLParser):
    def __init__(self,p):
        super().__init__();self.ids=set();self.links=[];self.feed(p.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        for key in ['src','href']:
            if a.get(key):self.links.append(a[key])
def main():
    pages={p:Page(p) for p in SITE.rglob('*.html')};errors=[];checked=0
    if len(pages)<38:errors.append('Expected homepage plus all 37 book sections')
    for p,info in pages.items():
        for link in info.links:
            u=urlsplit(link)
            if u.scheme or u.netloc:continue
            path=unquote(u.path)
            if path.startswith('/Learn-Design-System/'):target=SITE/path[len('/Learn-Design-System/'):]
            elif path.startswith('/'):target=SITE/path.lstrip('/')
            else:target=p.parent/path if path else p
            target=target.resolve()
            if target.is_dir():target=target/'index.html'
            if not target.exists():errors.append(f'{p.relative_to(SITE)}: missing {link}');continue
            checked+=1
            if u.fragment and target.suffix=='.html' and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{p.relative_to(SITE)}: missing anchor {link}')
    report={'pages':len(pages),'checked_links_and_assets':checked,'errors':errors}
    (ROOT/'build/site-link-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
if __name__=='__main__':main()
