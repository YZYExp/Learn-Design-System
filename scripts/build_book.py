#!/usr/bin/env python3
"""Build the illustrated book directly from Markdown, without HTML intermediates."""
from __future__ import annotations
import argparse, hashlib, html, json, math, re
from pathlib import Path
from io import BytesIO
from urllib.parse import urlsplit
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
    Spacer, PageBreak, KeepTogether, Image, Table, TableStyle, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parents[1]
INK=colors.HexColor('#202725'); RED=colors.HexColor('#B64835')
TEAL=colors.HexColor('#235F59'); PAPER=colors.HexColor('#FBF8F0'); GREY=colors.HexColor('#65706B')
PAGE=(210*mm,297*mm); WIDTH=166*mm
FONT='BookSC'
LINK=re.compile(r'(?<!!)\[([^\]]+)\]\(([^)\s]+)\)')
IMAGE=re.compile(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$')
FIGURE_OPTION=re.compile(r'<!--\s*figure-(height|width)\s*:\s*(\d+(?:\.\d+)?)\s*(?:mm)?\s*-->',re.I)
IMAGE_METADATA={}
SOURCE_HASHES={}
PDF_RASTER_DPI=300


def image_metadata_catalog():
    """Read project provenance manifests without assuming a single nesting shape."""
    catalog={}
    manifests=sorted((ROOT/'references').glob('revision-*-images.json'))
    manifests=[ROOT/'references/history-image-sources.json',ROOT/'assets/images/prompts.json',ROOT/'assets/images/figures-manifest.json']+manifests
    def visit(node,manifest):
        if isinstance(node,list):
            for child in node:visit(child,manifest)
        elif isinstance(node,dict):
            for key in ('file','path','image_file','local_path','asset_file','image'):
                value=node.get(key)
                if not isinstance(value,str) or value.startswith(('http:','https:')):continue
                if Path(value).suffix.lower() not in ('.png','.jpg','.jpeg','.webp','.tif','.tiff'):continue
                rel=Path(value)
                if rel.is_absolute():
                    try:rel=rel.relative_to(ROOT)
                    except ValueError:continue
                if len(rel.parts)==1:rel=Path('assets/images')/rel
                record=dict(node);record['_manifest']=str(manifest.relative_to(ROOT))
                catalog[str(rel)]=dict(catalog.get(str(rel),{}),**record)
            for child in node.values():
                if isinstance(child,(dict,list)):visit(child,manifest)
    for path in manifests:
        if path.exists():
            try:visit(json.loads(path.read_text()),path)
            except (ValueError,TypeError) as exc:raise ValueError(f'Invalid image manifest {path}: {exc}')
    return catalog


def image_kind(path,caption='',metadata=None):
    metadata=metadata or {}
    explicit=' '.join(str(metadata.get(k,'')) for k in ('kind','type','category','image_type','classification')).lower()
    if metadata.get('kind')=='original_design':return 'original_design'
    if any(k in explicit for k in ('ai_','ai-','ai ','ai生成','generated','生成插画','生成图','aiillustration')) or explicit=='ai':return 'ai_illustration'
    if any(k in explicit for k in ('real_artwork','real_original','original_work','historic','real_reference','原作','真实')):return 'real_artwork'
    if any(k in explicit for k in ('analysis','分析','拆解')):return 'original_analysis'
    if any(k in explicit for k in ('teaching','diagram','原创','教学')):return 'original_teaching'
    if re.search(r'AI\s*教学|AI\s*生成|生成插画',caption,re.I) or path.name in ('materials-atlas.png','studio-systems.png','space-and-object.png','style-comparison.png'):return 'ai_illustration'
    if re.match(r'^\s*[*_ >]*(?:真实作品|原作|经典作品)',caption) or path.name.startswith(('reference-','real-','classic-')):return 'real_artwork'
    if re.search(r'原创分析|原创拆解|分析图|拆解图',caption) or 'analysis' in path.name:return 'original_analysis'
    if path.name.startswith(('fig-','example-')) or '原创' in caption:return 'original_teaching'
    return 'unclassified'


def caption_line(text):
    text=text.strip().lstrip('>*_ ')
    return bool(re.match(r'^(?:图(?:\s*\d|[一二三四五六七八九十导])|真实作品|原作|经典作品|经典案例|案例图|原创分析|原创拆解|分析图|拆解图|教学图|比较图|配图|图注[：:])',text))


def fonts():
    path=ROOT/'assets/fonts/NotoSansSC-Regular.ttf'
    if not path.exists(): raise FileNotFoundError('Missing bundled OFL font: '+str(path))
    if FONT not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(FONT,str(path)))
        pdfmetrics.registerFontFamily(FONT,normal=FONT,bold=FONT,italic=FONT,boldItalic=FONT)

styles={}
def init_styles():
    base=dict(fontName=FONT,textColor=INK,wordWrap='CJK',allowWidows=0,allowOrphans=0)
    styles.update({
        'body':ParagraphStyle('body',fontSize=10.7,leading=18.2,spaceAfter=7,**base),
        'h1':ParagraphStyle('h1',fontSize=23,leading=33,spaceAfter=20,keepWithNext=True,**base),
        'h2':ParagraphStyle('h2',fontSize=15,leading=23,spaceBefore=15,spaceAfter=9,keepWithNext=True,**base),
        'h3':ParagraphStyle('h3',fontSize=11.6,leading=19,spaceBefore=9,spaceAfter=6,keepWithNext=True,**base),
        'caption':ParagraphStyle('caption',fontSize=8.7,leading=14.2,spaceBefore=5,spaceAfter=12,textColor=GREY,fontName=FONT,wordWrap='CJK'),
        'source':ParagraphStyle('source',fontSize=7.7,leading=11.7,spaceAfter=7,textColor=TEAL,fontName=FONT,wordWrap='CJK',leftIndent=8,borderColor=TEAL,borderWidth=.5,borderPadding=5),
        'cell':ParagraphStyle('cell',fontSize=8.7,leading=14,spaceAfter=0,**base),
        'code':ParagraphStyle('code',fontSize=8.2,leading=13,spaceAfter=0,**base),
        'small':ParagraphStyle('small',fontSize=9,leading=15,spaceAfter=8,**base),
        'toc':ParagraphStyle('toc',fontSize=10.3,leading=18,spaceBefore=6,**base),
    })

def clean(s):
    s=re.sub(r'<!--(?!\s*figure-(?:height|width)\s*:).*?-->','',s,flags=re.S)
    return s.replace('\u2011','-').replace('\u00a0',' ')

def inline(s, refs=None):
    """Minimal safe Markdown formatting; all references remain clickable."""
    tokens=[]
    def link(m):
        label,url=m.groups()
        if refs is not None and url.startswith(('http://','https://')):
            refs.append((label,url)); n=len(refs)
            val=f'{html.escape(label)}<super><font size="7" color="#235F59">[{n}]</font></super>'
        else:
            # Internal links in exported chapter text remain readable; external are live.
            val=f'<link href="{html.escape(url,quote=True)}" color="#235F59">{html.escape(label)}</link>' if url.startswith(('http:','https:')) else html.escape(label)
        tokens.append(val); return f'ZZLINK{len(tokens)-1}ZZ'
    s=LINK.sub(link,s)
    s=html.escape(s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font color="#235F59">\1</font>',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
    for i,t in enumerate(tokens): s=s.replace(f'ZZLINK{i}ZZ',t)
    return s

class Book(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=PAGE,leftMargin=22*mm,rightMargin=22*mm,
                         topMargin=22*mm,bottomMargin=21*mm,title='设计的语法：从艺术秩序到设计系统',author='YZ · AI 辅助编写',pageCompression=1)
        frame=Frame(22*mm,21*mm,WIDTH,254*mm,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='book',frames=frame,onPage=self.page))
        self.current_chapter='设计的语法'; self.chapter_pages=[];self.figure_records={}
    def page(self,canv,doc):
        if doc.page==1:self.chapter_pages=[];self.figure_records={}
        canv.saveState(); canv.setFillColor(PAPER); canv.rect(0,0,*PAGE,fill=1,stroke=0)
        if doc.page>1:
            canv.setStrokeColor(colors.HexColor('#D9D6CC')); canv.setLineWidth(.5)
            canv.line(22*mm,282*mm,188*mm,282*mm)
            canv.setFont(FONT,8); canv.setFillColor(GREY)
            canv.drawString(22*mm,286*mm,'设计的语法  /  THE GRAMMAR OF DESIGN')
        canv.setFont(FONT,8); canv.setFillColor(GREY)
        canv.drawString(22*mm,12*mm,'图解知识读本  ·  2026')
        canv.drawRightString(188*mm,12*mm,str(doc.page))
        canv.restoreState()
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and getattr(f,'bookmark',None):
            title=getattr(f,'toc_title',f.getPlainText()); key=f.bookmark
            self.canv.bookmarkPage(key); self.canv.addOutlineEntry(title,key,0,False)
            self.notify('TOCEntry',(0,title,self.page,key)); self.chapter_pages.append({'title':title,'page':self.page})
        if isinstance(f,Paragraph) and getattr(f,'figure_id',None):
            record=self.figure_records.setdefault(f.figure_id,{})
            record['caption_page']=self.page

class CoverArt(Flowable):
    def __init__(self): Flowable.__init__(self); self.width=WIDTH; self.height=91*mm
    def draw(self):
        c=self.canv; c.setFillColor(TEAL); c.rect(0,12*mm,65*mm,65*mm,fill=1,stroke=0)
        c.setFillColor(RED); c.circle(100*mm,44*mm,33*mm,fill=1,stroke=0)
        c.setFillColor(PAPER); c.circle(100*mm,44*mm,20*mm,fill=1,stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(1)
        for y in range(6): c.line(0,(10+y*13)*mm,WIDTH,(10+y*13)*mm)
        for x in range(5): c.line(x*41.5*mm,10*mm,x*41.5*mm,78*mm)
        c.setFillColor(INK); c.rect(135*mm,12*mm,31*mm,12*mm,fill=1,stroke=0)

def source_block(refs):
    entries=[]
    for i,(label,url) in enumerate(refs,1):
        domain=urlsplit(url).netloc.removeprefix('www.')
        entries.append(f'[{i}] <link href="{html.escape(url,quote=True)}" color="#235F59">{html.escape(label)} · {html.escape(domain)}</link>')
    return Paragraph('本段资料：'+ '<br/>'.join(entries),styles['source'])

def paragraph_block(text,style='body'):
    refs=[]; p=Paragraph(inline(text,refs),styles[style])
    return KeepTogether([p,source_block(refs)]) if refs else p

def raster_for_pdf(path,width,height,kind):
    """Freeze each embedding as bytes; cache writes are atomic and originals are untouched."""
    with PILImage.open(path) as image:
        original=image.size
        target=(max(1,round(width/72*PDF_RASTER_DPI)),max(1,round(height/72*PDF_RASTER_DPI)))
        if image.width<=target[0]*1.12 and image.height<=target[1]*1.12:return BytesIO(path.read_bytes()),original
        digest=SOURCE_HASHES.get(str(path.relative_to(ROOT))) or hashlib.sha256(path.read_bytes()).hexdigest()
        photographic=kind=='real_artwork' or path.suffix.lower() in ('.jpg','.jpeg','.webp')
        extension='.jpg' if photographic else '.png'
        key=hashlib.sha256(f'{digest}:{target}:{extension}:dpi300-v2'.encode()).hexdigest()[:24]
        cache=ROOT/'build/raster-cache';cache.mkdir(parents=True,exist_ok=True);out=cache/(key+extension)
        if out.exists():
            data=out.read_bytes()
            try:
                with PILImage.open(BytesIO(data)) as check:check.verify()
                with PILImage.open(BytesIO(data)) as check:size=check.size
                return BytesIO(data),size
            except (OSError,ValueError):pass
        image.thumbnail(target,PILImage.Resampling.LANCZOS)
        stream=BytesIO()
        if photographic:
            if image.mode not in ('RGB','L'):
                if 'A' in image.getbands():
                    background=PILImage.new('RGB',image.size,(251,248,240));background.paste(image,mask=image.getchannel('A'));image=background
                else:image=image.convert('RGB')
            image.save(stream,'JPEG',quality=95,optimize=True,subsampling=0)
        else:image.save(stream,'PNG',optimize=True)
        data=stream.getvalue();size=image.size
        temporary=out.with_name(out.name+'.pending');temporary.write_bytes(data);temporary.replace(out)
        return BytesIO(data),size


class TrackedImage(Image):
    def drawOn(self,canv,x,y,_sW=0):
        actual_x=x+(_sW/2 if self.hAlign=='CENTER' else _sW if self.hAlign=='RIGHT' else 0)
        canv.saveState();canv.setFillColor(PAPER);canv.setStrokeColor(colors.HexColor('#DAD6CD'));canv.setLineWidth(.35)
        canv.rect(actual_x-1.5,y-1.5,self.drawWidth+3,self.drawHeight+3,fill=1,stroke=1);canv.restoreState()
        super().drawOn(canv,x,y,_sW)
        doc=canv._doctemplate
        record=dict(self.figure_record)
        record.update({'image_page':canv.getPageNumber(),'width_mm':round(self.drawWidth/mm,2),'height_mm':round(self.drawHeight/mm,2),
                       'image_bbox':[round(v,2) for v in (actual_x,PAGE[1]-y-self.drawHeight,actual_x+self.drawWidth,PAGE[1]-y)]})
        doc.figure_records[self.figure_id]=record


def image_block(path,alt,caption='',options=None,figure_id=None,chapter=None,heading=None):
    if not path.is_file(): raise FileNotFoundError(f'Missing image: {path}')
    options=options or {}
    with PILImage.open(path) as im:w,h=im.size
    metadata=IMAGE_METADATA.get(str(path.relative_to(ROOT)),{})
    kind=image_kind(path,caption,metadata)
    # Give source works room to be inspected. Explicit dimensions are maximum bounds,
    # retain aspect ratio, and are expressed in millimetres in editable Markdown.
    default_height=140 if h>w*1.05 else 100
    maxh=float(options.get('height',default_height))*mm
    maxw=min(WIDTH,float(options.get('width',WIDTH/mm))*mm)
    if not 25*mm<=maxh<=225*mm or not 25*mm<=maxw<=WIDTH:raise ValueError(f'Unsafe figure dimensions: {path.name} {options}')
    cap=Paragraph(inline(caption or alt),styles['caption']);cap.figure_id=figure_id
    _,capheight=cap.wrap(WIDTH,1000*mm)
    available=254*mm-capheight-cap.getSpaceBefore()-cap.getSpaceAfter()-14
    if available<30*mm:raise ValueError(f'Caption is too long for one page: {path.name}; move analysis into prose')
    maxh=min(maxh,available)
    scale=min(maxw/w,maxh/h)
    embedded,embedded_pixels=raster_for_pdf(path,w*scale,h*scale,kind)
    picture=TrackedImage(embedded,width=w*scale,height=h*scale,hAlign='CENTER')
    picture.figure_id=figure_id
    picture.figure_record={'id':figure_id,'file':str(path.relative_to(ROOT)),'chapter':chapter,'kind':kind,
                           'caption':caption or alt,'explicit_caption':bool(caption),'layout_options_mm':options,
                           'source_pixels':[w,h],'embedded_pixels':list(embedded_pixels),
                           'source_effective_dpi':round(min(w/(w*scale/72),h/(h*scale/72)),1),
                           'metadata_manifest':metadata.get('_manifest')}
    return KeepTogether(([heading] if heading is not None else [])+[Spacer(1,7),picture,cap])


def balanced_title(text,style):
    """Balance a long heading without splitting Latin words or leaving a single CJK tail."""
    plain=re.sub(r'[*`_]','',text)
    if pdfmetrics.stringWidth(plain,FONT,style.fontSize)<=WIDTH:return inline(text)
    total=pdfmetrics.stringWidth(plain,FONT,style.fontSize)
    if total>WIDTH*2:return inline(text)
    candidates=[]
    forbidden='，。；：！？、）》】』」,.;:!?)]}'
    for i in range(1,len(plain)):
        if plain[i] in forbidden or (plain[i-1].isascii() and plain[i].isascii() and plain[i-1].isalnum() and plain[i].isalnum()):continue
        left,right=plain[:i].rstrip(),plain[i:].lstrip()
        wl=pdfmetrics.stringWidth(left,FONT,style.fontSize);wr=pdfmetrics.stringWidth(right,FONT,style.fontSize)
        if max(wl,wr)>WIDTH or min(len(left),len(right))<4:continue
        punctuation_bonus=20 if plain[i-1] in '：，、；: ' else 0
        candidates.append((abs(wl-wr)-punctuation_bonus,left,right))
    if not candidates:return inline(text)
    _,left,right=min(candidates)
    return inline(left)+'<br/>'+inline(right)


def chapter_heading(text,path):
    match=re.match(r'^(第\s*\d+\s*章|第[一二三四五六七八九十百]+章|附录[一二三四五六七八九十]+|导读)[｜|：:　 ]+(.*)$',text)
    out=[]
    if match:
        kicker,title=match.groups()
        kstyle=ParagraphStyle('chapter-kicker',fontName=FONT,fontSize=10.5,leading=16,textColor=TEAL,spaceAfter=7,keepWithNext=True)
        out.append(Paragraph(html.escape(kicker),kstyle))
    else:title=text
    p=Paragraph(balanced_title(title,styles['h1']),styles['h1']);p.bookmark='chapter-'+path.stem;p.toc_title=text
    out.append(p);return out


def table_block(lines):
    rows=[]
    for line in lines:
        cells=[x.strip() for x in line.strip().strip('|').split('|')]
        if all(re.match(r'^:?-{2,}:?$',x) for x in cells): continue
        rows.append([Paragraph(inline(x),styles['cell']) for x in cells])
    if not rows:return Spacer(1,0)
    n=max(map(len,rows)); rows=[r+[Paragraph('',styles['cell'])]*(n-len(r)) for r in rows]
    padding=4.5 if styles['cell'].fontSize<8.5 else 7
    t=Table(rows,colWidths=[WIDTH/n]*n,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E6ECE6')),
        ('LINEBELOW',(0,0),(-1,0),.7,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#DADBD3')),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),padding),('BOTTOMPADDING',(0,0),(-1,-1),padding)]))
    return [t,Spacer(1,9)]

def parse_file(path):
    raw=clean(path.read_text()); saved_styles=dict(styles)
    # A short closing essay should fit naturally on one page rather than create a tiny tail page.
    if len(re.findall(r'[\u3400-\u9fff]',raw))<1350 and '![' not in raw:
        styles['body']=ParagraphStyle('compact-body',parent=styles['body'],fontSize=10.3,leading=17,spaceAfter=5)
        styles['h1']=ParagraphStyle('compact-h1',parent=styles['h1'],fontSize=20,leading=28,spaceAfter=14)
        styles['h2']=ParagraphStyle('compact-h2',parent=styles['h2'],fontSize=13.5,leading=21,spaceBefore=11,spaceAfter=7)
    if path.stem.startswith('33-') and '![' not in raw:
        styles['body']=ParagraphStyle('closing-body',parent=styles['body'],leading=16.4,spaceAfter=4.5)
        styles['h2']=ParagraphStyle('closing-h2',parent=styles['h2'],spaceBefore=10)
    if path.parent.name=='appendices' and path.stem.startswith('B-'):
        styles['cell']=ParagraphStyle('compact-source-cell',parent=styles['cell'],fontSize=8.3,leading=13)
    lines=raw.splitlines(); result=[]; i=0; reference_section=False; pending_figure_options={}
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1;continue
        option=FIGURE_OPTION.fullmatch(line)
        if option:
            pending_figure_options[option.group(1).lower()]=float(option.group(2));i+=1;continue
        if line.startswith('```'):
            i+=1; code=[]
            while i<len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i]); i+=1
            ps=[Paragraph(html.escape(s).replace(' ','&#160;') or '&#160;',styles['code']) for s in code]
            t=Table([[p] for p in ps],colWidths=[WIDTH],hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#ECEDE5')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),1.5),('BOTTOMPADDING',(0,0),(-1,-1),1.5)]))
            result.extend([Spacer(1,5),t,Spacer(1,10)]); i+=1;continue
        m=IMAGE.match(line)
        if m:
            alt,rel=m.groups();caption='';j=i+1;figure_line=i+1;options=dict(pending_figure_options);pending_figure_options={}
            while j<len(lines):
                following=lines[j].strip();option=FIGURE_OPTION.fullmatch(following)
                if not following:j+=1;continue
                if option:options[option.group(1).lower()]=float(option.group(2));j+=1;continue
                break
            if j<len(lines) and caption_line(lines[j]):
                parts=[lines[j].strip().lstrip('> ')];k=j+1
                while k<len(lines) and lines[k].strip() and not lines[k].strip().startswith(('#','!','|','```','<!--')) and not caption_line(lines[k]):
                    parts.append(lines[k].strip());k+=1
                caption=' '.join(parts);i=k-1
            else:i=j-1
            figure_id=path.stem+'-'+str(figure_line)
            heading=result.pop() if result and isinstance(result[-1],Paragraph) and result[-1].style.name=='h3' else None
            result.append(image_block((path.parent/rel).resolve(),alt,caption,options,figure_id,str(path.relative_to(ROOT)),heading));i+=1;continue
        if line.startswith('|'):
            block=[]
            while i<len(lines) and lines[i].strip().startswith('|'):block.append(lines[i]);i+=1
            tb=table_block(block); result.extend(tb if isinstance(tb,list) else [tb]);continue
        if line.startswith('# '):
            result.extend(chapter_heading(line[2:],path));i+=1;continue
        if line.startswith('## '):result.append(Paragraph(inline(line[3:]),styles['h2']));i+=1;continue
        if line.startswith('### '):result.append(Paragraph(inline(line[4:]),styles['h3']));i+=1;continue
        if re.match(r'^[-*_]{3,}$',line):result.append(Spacer(1,10));i+=1;continue
        if line.startswith(('本章来源','本章资料','本节来源')): reference_section=True
        if re.match(r'^[-*+]\s|^\d+[.)、]\s?',line):
            line=re.sub(r'^[-*+]\s','• ',line)
            result.append(Paragraph(inline(line),styles['small']) if reference_section else paragraph_block(line));i+=1;continue
        if line.startswith('>'):line=line.lstrip('> ')
        block=[line];i+=1
        while i<len(lines):
            n=lines[i].strip()
            if not n or n.startswith(('#','!','|','```','>','<!--')) or re.match(r'^[-*+]\s|^\d+[.)、]\s?',n):break
            block.append(n);i+=1
        text=' '.join(block)
        # Keep source attribution with the paragraph that uses it. Split only very long prose blocks.
        if len(text)>1100:
            chunks=re.split(r'(?<=[。！？])',text); part=''
            for c in chunks:
                if len(part)+len(c)>650 and part:result.append(paragraph_block(part));part=''
                part+=c
            if part:result.append(paragraph_block(part))
        else:result.append(Paragraph(inline(text),styles['small']) if reference_section else paragraph_block(text))
    styles.clear(); styles.update(saved_styles)
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='build/design-grammar.pdf');args=ap.parse_args()
    fonts(); init_styles();IMAGE_METADATA.clear();IMAGE_METADATA.update(image_metadata_catalog()); out=ROOT/args.output;out.parent.mkdir(parents=True,exist_ok=True)
    files=sorted((ROOT/'chapters').glob('*.md'))+sorted((ROOT/'appendices').glob('*.md'))
    if not files:raise RuntimeError('No Markdown chapter sources')
    inputs=set(files)
    for source in files:
        for _alt, rel in re.findall(r'!\[([^\]]*)\]\(([^)]+)\)',source.read_text()):
            inputs.add((source.parent/rel).resolve())
    inputs.add(ROOT/'assets/fonts/NotoSansSC-Regular.ttf')
    lab=ROOT/'examples/creative-lab'
    if lab.exists():
        inputs.update(p for p in lab.rglob('*') if p.is_file() and not any(x in ('renders','__pycache__','node_modules') for x in p.relative_to(lab).parts) and not p.name.startswith('.'))
    inputs.update((ROOT/'references').glob('revision-*-images.json'))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)}
    SOURCE_HASHES.clear();SOURCE_HASHES.update(hashes)
    story=[Spacer(1,20*mm),Paragraph('设计的语法',ParagraphStyle('cover',fontName=FONT,fontSize=39,leading=52,textColor=INK)),
        Spacer(1,6*mm),Paragraph('从艺术秩序到设计系统',ParagraphStyle('subtitle',fontName=FONT,fontSize=17,leading=28,textColor=TEAL)),Spacer(1,14*mm),CoverArt(),
        Spacer(1,10*mm),Paragraph('从纹样、版式、器物与空间，走向可以学习、制作和维护的设计规则。',styles['small']),
        Paragraph('图解知识读本 · 5.0折光视觉提案与原生重建版 · 2026年10月',styles['small']),PageBreak(),Paragraph('目录与阅读顺序',styles['h1'])]
    toc=TableOfContents();toc.levelStyles=[styles['toc']];toc.dotsMinLevel=0
    story.extend([toc,PageBreak()])
    for index,path in enumerate(files):
        if index:story.append(PageBreak())
        story.extend(parse_file(path))
    temporary=out.with_name(out.stem+'.pending.pdf')
    doc=Book(temporary);doc.multiBuild(story)
    changed=[rel for rel,digest in hashes.items() if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest]
    if changed:raise RuntimeError('Sources changed during build; rebuild after editing: '+', '.join(changed))
    temporary.replace(out)
    record={'pdf':str(out.relative_to(ROOT)),'source_files':[str(p.relative_to(ROOT)) for p in files],
            'chapter_starts':doc.chapter_pages[-len(files):], 'figures':list(doc.figure_records.values()), 'font':'Noto Sans SC Regular (SIL OFL 1.1)',
            'citations':'Inline reference markers plus linked source blocks are kept with the prose that uses them.',
            'html_generated':False,'raster_embedding_dpi_limit':PDF_RASTER_DPI,'input_sha256':hashes}
    (ROOT/'build/build-report.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
    print(json.dumps({'pdf':str(out),'chapters':len(files),'bytes':out.stat().st_size},ensure_ascii=False))
if __name__=='__main__':main()
