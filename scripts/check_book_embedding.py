#!/usr/bin/env python3
"""Audit source-to-page embedding records against an existing PDF, without rebuilding.

Evidence links the build's source SHA256, a local source, a logged image bbox,
an actual displayed PDF image at that bbox, and a direct page rendering. It does
not assert equality between a source-file hash and a PDF image-stream hash.
Run after a build finishes. Output is excluded from the book's input manifests.
"""
from __future__ import annotations
import argparse,hashlib,json,os,tempfile
from datetime import datetime,timezone
from pathlib import Path
import fitz
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def relative(path):
 try:return str(path.resolve().relative_to(ROOT))
 except ValueError:return str(path)
def atomic_json(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 fd,temp=tempfile.mkstemp(prefix=path.stem+'-',suffix='.json',dir=path.parent)
 try:
  with os.fdopen(fd,'w') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
  os.replace(temp,path)
 finally:
  if os.path.exists(temp):os.unlink(temp)
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--pdf',type=Path,default=ROOT/'build/design-grammar.pdf')
 ap.add_argument('--build-report',type=Path,default=ROOT/'build/build-report.json')
 ap.add_argument('--output',type=Path,default=ROOT/'references/embedded-artwork-current-audit.json')
 ap.add_argument('--proof-dir',type=Path,default=ROOT/'build/embedding-proof-current')
 ap.add_argument('--proof-pages',help='Comma-separated 1-based pages; defaults to original-design and AI material pages')
 ap.add_argument('--dpi',type=int,default=120)
 args=ap.parse_args();pdf=args.pdf.resolve();buildpath=args.build_report.resolve();build=json.loads(buildpath.read_text());pdfhash=digest(pdf);buildhash=digest(buildpath);doc=fitz.open(pdf)
 errors=[];records=[];page_info={};source_records={}
 for figure in build.get('figures',[]):
  source=ROOT/figure['file'];page_number=figure.get('image_page');expected=build.get('input_sha256',{}).get(figure['file']);exists=source.is_file();actual=digest(source) if exists else None
  source_record={'file':figure['file'],'exists':exists,'build_input_sha256':expected,'local_sha256':actual,'matches_build_input':bool(expected and actual==expected)}
  source_records[figure['file']]=source_record
  if not exists:errors.append({'file':figure['file'],'error':'Source file missing'})
  elif not expected:errors.append({'file':figure['file'],'error':'No source hash recorded in build input_sha256'})
  elif actual!=expected:errors.append({'file':figure['file'],'error':'Local source differs from built input; PDF evidence remains a snapshot of the prior build'})
  valid_page=isinstance(page_number,int) and 1<=page_number<=len(doc)
  record={'source_file':figure['file'],'figure_id':figure.get('id'),'chapter':figure.get('chapter'),'kind':figure.get('kind'),'caption':figure.get('caption'),'page':page_number,'page_exists':valid_page,'source_sha256_matches_build':source_record['matches_build_input'],'logged_bbox_points':figure.get('image_bbox'),'logged_embedded_pixels':figure.get('embedded_pixels'),'caption_page':figure.get('caption_page')}
  if not valid_page:
   errors.append({'file':figure['file'],'error':'Logged PDF page does not exist'});records.append(record);continue
  if page_number not in page_info:
   page=doc[page_number-1];images=[]
   for info in page.get_image_info(xrefs=True):
    images.append({'xref':info.get('xref'),'bbox_points':[round(v,4) for v in info['bbox']],'embedded_pixels':[info['width'],info['height']],'has_mask':info.get('has-mask',False)})
   page_info[page_number]={'page':page_number,'displayed_image_count':len(images),'resource_image_count':len(page.get_images(full=True)),'actual_displayed_images':images}
  info=page_info[page_number];record['pdf_displayed_image_count']=info['displayed_image_count'];record['pdf_resource_image_count']=info['resource_image_count']
  bbox=figure.get('image_bbox');matches=[]
  if bbox and len(bbox)==4:
   for image in info['actual_displayed_images']:
    delta=max(abs(a-b) for a,b in zip(bbox,image['bbox_points']))
    if delta<=.05:matches.append({**image,'max_bbox_delta_points':round(delta,5),'embedded_pixels_match_log':image['embedded_pixels']==figure.get('embedded_pixels')})
  record['matching_displayed_pdf_images']=matches
  record['logged_placement_verified']=len(matches)==1 and matches[0]['embedded_pixels_match_log']
  if not record['logged_placement_verified']:errors.append({'file':figure['file'],'page':page_number,'error':'Expected one displayed image with matching bbox and embedded dimensions'})
  if figure.get('caption_page')!=page_number:errors.append({'file':figure['file'],'page':page_number,'error':'Caption is on a different page'})
  records.append(record)
 if args.proof_pages:proof_pages={int(v) for v in args.proof_pages.split(',') if v.strip()}
 else:proof_pages={r['page'] for r in records if r['page_exists'] and r['kind'] in ['original_design','ai_illustration']}
 args.proof_dir.mkdir(parents=True,exist_ok=True);proofs=[]
 for page_number in sorted(proof_pages):
  if not 1<=page_number<=len(doc):errors.append({'page':page_number,'error':'Requested proof page does not exist'});continue
  target=args.proof_dir/f'page-{page_number:03}.png';temp=target.with_suffix('.pending.png')
  doc[page_number-1].get_pixmap(matrix=fitz.Matrix(args.dpi/72,args.dpi/72),alpha=False).save(temp);os.replace(temp,target)
  with Image.open(target) as im:size=list(im.size);im.verify()
  proofs.append({'page':page_number,'file':relative(target),'sha256':digest(target),'pixels':size,'dpi':args.dpi,'method':'Direct full-page rendering from the audited PDF using PyMuPDF'})
  for r in records:
   if r['page']==page_number:r['page_render_proof']=relative(target)
 if digest(pdf)!=pdfhash:errors.append({'error':'PDF changed while auditing; rerun against stable input'})
 if digest(buildpath)!=buildhash:errors.append({'error':'Build report changed while auditing; rerun against stable input'})
 report={'audit_version':1,'created_utc':datetime.now(timezone.utc).isoformat(),'pdf':{'file':relative(pdf),'sha256':pdfhash,'bytes':pdf.stat().st_size,'pages':len(doc)},'build_report':{'file':relative(buildpath),'sha256':buildhash},'evidence_contract':{'checks':['Build input_sha256 equals local source SHA256','Recorded page exists in this exact PDF','Actual displayed PDF image matches logged bbox within 0.05pt and embedded pixel dimensions','Caption page equals image page','Selected page proofs are rendered directly from this exact PDF'],'limitation':'The source file may be resized or recompressed when embedded. Source-file SHA256 is not a PDF compressed-image-stream hash. Placement and rendering evidence does not establish byte identity between those files.'},'summary':{'image_uses':len(records),'unique_source_files':len(source_records),'verified_placements':sum(r.get('logged_placement_verified',False) for r in records),'source_hashes_matching_build':sum(r['matches_build_input'] for r in source_records.values()),'proof_pages':len(proofs),'errors':len(errors)},'source_files':[source_records[k] for k in sorted(source_records)],'image_uses':records,'pages':[page_info[k] for k in sorted(page_info)],'page_render_proofs':proofs,'errors':errors}
 atomic_json(args.output,report);print(json.dumps(report['summary'],ensure_ascii=False));print(args.output);raise SystemExit(bool(errors))
if __name__=='__main__':main()
