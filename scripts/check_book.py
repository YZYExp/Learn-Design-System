#!/usr/bin/env python3
"""Check source integrity and the finished reading PDF; never generates HTML."""
from __future__ import annotations
import argparse,hashlib,json,re,sys
from pathlib import Path
from book_manifest import ordered_sources
ROOT=Path(__file__).resolve().parents[1]
from collections import Counter
from build_book import image_metadata_catalog, image_kind, caption_line, FIGURE_OPTION, fonts, FONT, pdfmetrics
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-only',action='store_true');ap.add_argument('--render',action='store_true',help='Render every page into contact sheets and key full-page PNGs');args=ap.parse_args()
    files=ordered_sources()
    errors=[];warnings=[];image_refs=[];urls=set();chars=0;catalog=image_metadata_catalog();image_kinds={};caption_records=[];all_characters=set()
    for p in files:
        s=p.read_text();all_characters.update(s);chars+=len(re.findall(r'[\u3400-\u9fff]',s))
        if len(re.findall(r'^# ',s,re.M))!=1:errors.append(f'{p.name}: expected one chapter title')
        if re.search(r'\b(?:TODO|TBD|PLACEHOLDER)\b|待补正文|占位图',s,re.I):errors.append(f'{p.name}: unresolved placeholder marker')
        for match in re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)',s):
            alt,rel=match.groups()
            im=(p.parent/rel).resolve();image_refs.append(str(im.relative_to(ROOT)))
            if not im.is_file():errors.append(f'{p.name}: missing {rel}')
            following=s[match.end():].splitlines();caption='';options={}
            for line_index,line in enumerate(following):
                line=line.strip()
                if not line:continue
                option=FIGURE_OPTION.fullmatch(line)
                if option:options[option.group(1)]=float(option.group(2));continue
                if caption_line(line):
                    parts=[line]
                    for more in following[line_index+1:]:
                        if not more.strip() or more.strip().startswith(('#','!','|','```','<!--')):break
                        parts.append(more.strip())
                    caption=' '.join(parts)
                break
            relative=str(im.relative_to(ROOT));metadata=catalog.get(relative,{})
            kind=image_kind(im,caption,metadata);image_kinds[relative]=kind
            caption_records.append({'chapter':p.name,'file':relative,'kind':kind,'caption':caption})
            if not caption:warnings.append(f'{p.name}: image has no explicit caption: {rel}')
            if kind=='real_artwork' and not re.search(r'https?://',caption):
                warnings.append(f'{p.name}: original artwork caption has no direct source link: {rel}')

        for label,url in re.findall(r'(?<!!)\[([^\]]+)\]\(([^)\s]+)\)',s):
            if url.startswith(('http://','https://')):urls.add(url)
            elif url.startswith('#'):continue
            elif not (p.parent/url.split('#')[0]).exists():errors.append(f'{p.name}: missing link target {url}')
    fonts();font_cmap=pdfmetrics.getFont(FONT).face.charToGlyph
    missing_glyphs=sorted(x for x in all_characters if ord(x)>31 and ord(x) not in font_cmap)
    if missing_glyphs:errors.append('Characters not covered by embedded font: '+''.join(missing_glyphs))
    real_source_records=set()
    for rel,kind in image_kinds.items():
        if kind!='real_artwork':continue
        metadata=catalog.get(rel,{})
        source=next((metadata[k] for k in ('objectURL','object_url','source_url','source','primary_source_url') if isinstance(metadata.get(k),str) and metadata[k].startswith(('http:','https:'))),None)
        real_source_records.add(source.split('#')[0] if source else rel)
    report={'source_files':len(files),'chinese_characters':chars,'image_uses':len(image_refs),'unique_images':len(set(image_refs)),
            'external_source_links':len(urls),'image_kinds_unique':dict(Counter(image_kinds.values())),'image_kinds_uses':dict(Counter(x['kind'] for x in caption_records)),
            'image_manifest_records':len(catalog),'real_artwork_primary_records':len(real_source_records),'font_missing_characters':missing_glyphs,'image_classification':image_kinds,'warnings':warnings,'errors':errors}
    pdf=ROOT/'build/design-grammar.pdf'
    if not args.source_only:
        if not pdf.exists():errors.append('Missing reading PDF')
        else:
            build_data={};build_record=ROOT/'build/build-report.json'
            if build_record.exists():
                build_data=json.loads(build_record.read_text());hashes=build_data.get('input_sha256',{})
                figures=build_data.get('figures',[])
                if figures:
                    detached=[f for f in figures if f.get('image_page')!=f.get('caption_page')]
                    if detached:errors.append('Figure/caption page separation: '+', '.join(f.get('file','?') for f in detached))
                    if len(figures)!=len(image_refs):errors.append('Figure layout log count differs from Markdown image uses')
                    report['figure_caption_pairs_checked']=len(figures)
                    low_resolution=[f for f in figures if f.get('kind')=='real_artwork' and f.get('source_effective_dpi',999)<120]
                    report['real_artwork_below_120dpi']=[{'file':f['file'],'dpi':f.get('source_effective_dpi')} for f in low_resolution]
                    if low_resolution:warnings.append('Some real artworks have source resolution below 120 dpi at printed size; inspect the listed images')
                    report['figure_caption_page_mismatches']=detached
                    report['figure_dimensions_mm']=[{'file':f['file'],'width_mm':f.get('width_mm'),'height_mm':f.get('height_mm'),'page':f.get('image_page')} for f in figures]
                changed=[rel for rel,h in hashes.items() if not (ROOT/rel).exists() or hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=h]
                if changed:errors.append('Sources changed after PDF build: '+', '.join(changed))
            import fitz
            from pypdf import PdfReader
            d=fitz.open(pdf); outside=[];empty=[];replacement=[]
            for i,page in enumerate(d):
                text=page.get_text()
                if len(text.strip())<15:empty.append(i+1)
                if '\ufffd' in text:replacement.append(i+1)
                for block in page.get_text('dict')['blocks']:
                    if block.get('type')!=0:continue
                    for line in block['lines']:
                        x0,y0,x1,y1=line['bbox']
                        if x0<45 or x1>550 or y0<15 or y1>833:outside.append({'page':i+1,'bbox':[round(v,1) for v in (x0,y0,x1,y1)],'text':''.join(x['text'] for x in line['spans'])[:90]})
            reader=PdfReader(pdf)
            def count(nodes):
                return sum(count(x) if isinstance(x,list) else 1 for x in nodes)
            bookmarks=count(reader.outline); links=sum(len(p.get_links()) for p in d)
            report.update({'pdf_pages':len(d),'bookmarks':bookmarks,'pdf_links':links,'empty_pages':empty,
                           'text_replacement_pages':replacement,'text_outside_safe_page':outside,'pdf_bytes':pdf.stat().st_size})
            if empty:errors.append('Empty PDF pages: '+str(empty))
            if outside:errors.append('Text outside safe page bounds: '+str(len(outside)))
            if replacement:errors.append('Replacement characters in PDF text')
            if bookmarks<len(files):errors.append('Missing PDF chapter bookmarks')
            if links<10:errors.append('PDF navigation/citations are not clickable')
            if len(d)<len(files)+2:errors.append('Chapter start pagination missing')
            if args.render:
                from PIL import Image as PILImage, ImageDraw
                qa=ROOT/'build/qa';qa.mkdir(parents=True,exist_ok=True)
                for old in qa.glob('overview-*.png'):old.unlink()
                for old in qa.glob('page-*.png'):old.unlink()
                for page_number,page in enumerate(d):
                    pix=page.get_pixmap(matrix=fitz.Matrix(.4,.4),alpha=False)
                    thumb=PILImage.frombytes('RGB',(pix.width,pix.height),pix.samples);thumb.thumbnail((238,337))
                    tile=PILImage.new('RGB',(250,362),'#DDDDDD');tile.paste(thumb,((250-thumb.width)//2,4));ImageDraw.Draw(tile).text((7,345),str(page_number+1),fill='black')
                    if page_number%24==0:sheet=PILImage.new('RGB',(1500,1448),'white')
                    j=page_number%24;sheet.paste(tile,((j%6)*250,(j//6)*362))
                    if j==23 or page_number==len(d)-1:sheet.save(qa/f'overview-{page_number//24+1}.png')
                full_pages={0,1,2,len(d)-1}
                full_pages.update(x['page']-1 for x in build_data.get('chapter_starts',[]))
                full_pages.update(x['image_page']-1 for x in build_data.get('figures',[]) if x.get('image_page'))
                for n in sorted(full_pages):
                    if 0<=n<len(d):d[n].get_pixmap(matrix=fitz.Matrix(1.15,1.15),alpha=False).save(qa/f'page-{n+1:03}.png')
                rendering={'all_pages_rendered':len(d),'thumbnail_size':[238,337],'contact_sheets':(len(d)+23)//24,'full_pages':[n+1 for n in sorted(full_pages)]}
                (qa/'render-report.json').write_text(json.dumps(rendering,ensure_ascii=False,indent=2));report['rendering']=rendering

    report['errors']=errors
    (ROOT/'build').mkdir(exist_ok=True)
    (ROOT/'build/check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    display={k:v for k,v in report.items() if k not in ('image_classification','figure_dimensions_mm')}
    print(json.dumps(display,ensure_ascii=False,indent=2))
    if errors:sys.exit(1)
if __name__=='__main__':main()
