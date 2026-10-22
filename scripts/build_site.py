#!/usr/bin/env python3
"""User-run-only MkDocs Material build. The book authoring workflow does not invoke this."""
import argparse,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--serve',action='store_true');args=ap.parse_args()
    docs=ROOT/'build/site-source';docs.mkdir(parents=True,exist_ok=True)
    for folder in ('chapters','appendices','assets'):
        shutil.copytree(ROOT/folder,docs/folder,dirs_exist_ok=True)
    # Copy native artwork referenced by chapters without copying editable projects into the site.
    for chapter in (ROOT/'chapters').glob('*.md'):
        for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',chapter.read_text()):
            if target.startswith(('http:','https:','data:')):continue
            source=(chapter.parent/target).resolve();relative=source.relative_to(ROOT)
            destination=docs/relative
            if not destination.exists():
                destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,destination)
    nav=[]; lines=['# 设计的语法\n\n从艺术秩序到设计系统。\n']
    for folder in ('chapters','appendices'):
        for p in sorted((ROOT/folder).glob('*.md')):
            title=next((x[2:] for x in p.read_text().splitlines() if x.startswith('# ')),p.stem)
            rel=f'{folder}/{p.name}'; nav.append({title:rel});lines.append(f'- [{title}]({rel})\n')
    (docs/'index.md').write_text(''.join(lines))
    config={'site_name':'设计的语法','docs_dir':str(docs),'site_dir':str(ROOT/'build/site'),
            'theme':{'name':'material','language':'zh','features':['navigation.sections','navigation.top','toc.follow']},
            'plugins':['search'],'markdown_extensions':['tables','fenced_code','footnotes','toc'],
            'nav':[{'阅读入口':'index.md'}]+nav}
    # JSON is a valid YAML document; no separate YAML writer required.
    cfg=ROOT/'build/mkdocs.yml';cfg.write_text(json.dumps(config,ensure_ascii=False,indent=2))
    subprocess.run([sys.executable,'-m','mkdocs','serve' if args.serve else 'build','-f',str(cfg)],check=True)
if __name__=='__main__':main()
