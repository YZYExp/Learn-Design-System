#!/usr/bin/env python3
"""Package the writing repository and native creative lab without the reading PDF.

Use --dry-run before the final source freeze. Never deletes or changes sources.
All Markdown chapter image targets override regenerable-image exclusions.
The writing archive preserves the complete Git repository; the native archive
records that repository's commit identity and includes its editable projects.
"""
from __future__ import annotations
import argparse,hashlib,json,os,re,subprocess,tempfile,zlib
from collections import Counter
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
LIMIT=512*1024*1024
LAB=ROOT/'examples/creative-lab'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def chapter_images():
 result=set()
 for p in list((ROOT/'chapters').glob('*.md'))+list((ROOT/'appendices').glob('*.md')):
  for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('http:','https:','data:')):continue
   image=(p.parent/target).resolve()
   if not image.is_file():raise ValueError(f'Missing chapter image: {p.name}: {target}')
   image.relative_to(ROOT);result.add(image)
 return result

def exclusion(p,protected,omit_exports=False):
 if p in protected:return None
 parts=p.relative_to(ROOT).parts
 if p.suffix.lower()=='.pdf':return 'PDF delivered separately'
 if p.name=='.server.json':return 'runtime server discovery'
 if any(v in parts for v in ['node_modules','__pycache__','.venv','restore-backup']):return 'dependencies/cache/recovery backup'
 if any(v.startswith('.tmp-') for v in parts) or p.name.endswith(('.pyc','.pending','.tmp','.tmp.png','.png.tmp')):return 'temporary file'
 if 'output' in parts or p.suffix.lower()=='.zip':return 'existing package'
 if parts[0]=='build':return 'build cache / previews (selected reports added separately)'
 if 'renders' in parts and p.suffix.lower()=='.png':
  at=parts.index('renders');tail=parts[at+1:]
  if 'check' in tail:return 'regenerable native check PNG'
  if 'v3' in tail:return 'unreferenced regenerable V3 PNG; editable V3 sources retained'
  if omit_exports and 'export' in tail:return 'unreferenced native export PNG; native sources retained'
 if '.git' in parts and (p.name.endswith('.lock') or p.name=='COMMIT_EDITMSG'):return 'transient Git state'
 return None

def collect(protected,omit_exports=False,separate_git=False):
 writing={};native={};excluded=Counter();excluded_bytes=Counter()
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file():continue
  if separate_git and '.git' in p.relative_to(ROOT).parts:
   excluded['Git history delivered as separate complete bundle']+=1;excluded_bytes['Git history delivered as separate complete bundle']+=p.stat().st_size;continue
  p=p.resolve();reason=exclusion(p,protected,omit_exports)
  if reason:excluded[reason]+=1;excluded_bytes[reason]+=p.stat().st_size;continue
  rel=p.relative_to(ROOT);writing['design-grammar/'+str(rel)]=p
  if p.is_relative_to(LAB):native['creative-lab/'+str(p.relative_to(LAB))]=p
 reports=list((ROOT/'build').glob('*.json'))+[ROOT/'build/qa/render-report.json']
 for p in reports:
  if p.is_file() and p.name!='package-plan.json':
   writing['design-grammar/'+str(p.relative_to(ROOT))]=p
   native['creative-lab/validation/'+p.name]=p
 for name in ['revision-creative-lab-images.json','embedded-artwork-v3-audit.json','embedded-artwork-current-audit.json']:
  p=ROOT/'references'/name
  if p.is_file():native['creative-lab/validation/'+name]=p
 missing=protected-set(writing.values())
 if missing:raise ValueError('Referenced chapter images excluded: '+', '.join(str(p) for p in missing))
 return writing,native,{'files':dict(excluded),'raw_bytes':dict(excluded_bytes)}

def compressed_size(p):
 compressor=zlib.compressobj(6,zlib.DEFLATED,-15);total=0
 with p.open('rb') as stream:
  for chunk in iter(lambda:stream.read(1024*1024),b''):total+=len(compressor.compress(chunk))
 return total+len(compressor.flush())

def package_notes(kind,head,separate_git=False):
 history=('Complete Git history is delivered separately as 设计的语法-版本历史.bundle.\nRestore it with: git clone 设计的语法-版本历史.bundle design-grammar-history\nThe source ZIP remains complete for reading, editing and PDF rebuilds.' if separate_git else 'The writing archive includes the complete .git history and current source files.')
 return f'''# Design Grammar source package\n\nPackage: {kind}\nSource Git HEAD: {head}\n\n{history}\nThe native archive contains six editable Tingly Design projects, local fonts,\nAI material provenance, authoring scripts, rendered exports, and validation reports.\nIts commit identity refers to the complete accompanying Git history.\nThe reading PDF is delivered separately and intentionally omitted from both ZIPs.\n\nThe writing archive preserves every image referenced by book chapters; the native
archive preserves the referenced artwork within creative-lab. Generated check PNGs, caches,\nrecovery backups and V3 PNGs not referenced by the book are omitted. V3 editable\nsource files and fonts are preserved so before/after comparisons can be regenerated.
Unreferenced export PNGs may also be omitted when the explicit packaging option is selected.\nNo source file was deleted to produce these archives. Native previews may be\nregenerated with Tingly Design 0.26.1021 and a local Chromium via DC_CHROME.\n\nThe embedded-artwork audit relates source hashes, logged placement and actual PDF\nrenderings. A source-file hash is not the compressed PDF image-stream hash.\n'''

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--dry-run',action='store_true');ap.add_argument('--output-dir',type=Path,default=ROOT.parent/'output');ap.add_argument('--report',type=Path,default=ROOT/'build/package-plan.json');ap.add_argument('--omit-unreferenced-export-pngs',action='store_true',help='Omit regenerated export PNGs unless a book chapter references them; preserve all native source/fonts');ap.add_argument('--separate-git-history',action='store_true',help='Deliver full history in an accompanying Git bundle; preserve all current writing source files');args=ap.parse_args()
 protected=chapter_images();writing,native,excluded=collect(protected,args.omit_unreferenced_export_pngs,args.separate_git_history);head=git('rev-parse','HEAD');refs=git('show-ref');initial={p:(p.stat().st_size,p.stat().st_mtime_ns) for p in set(writing.values())|set(native.values())}
 # Estimate actual deflate size, reuse compression results for byte-identical files.
 hashes={};compressed={};content_cache={}
 for p in initial:
  h=sha(p);hashes[p]=h
  if h not in content_cache:content_cache[h]=compressed_size(p)
  compressed[p]=content_cache[h]
 report={'dry_run':args.dry_run,'advisory_size_threshold_bytes':LIMIT,'size_policy':'Observed server limit: each file must not exceed 512MiB; complete Git history may be delivered as a separate bundle','warnings':[],'git_head':head,'git_refs':refs.splitlines(),'chapter_image_targets_preserved':len(protected),'exclusions':excluded,'omit_unreferenced_export_pngs':args.omit_unreferenced_export_pngs,'archives':[]}
 for name,kind,files in [('设计的语法-写作工程.zip','writing-source',writing),('设计系统-原创创作工程.zip','native-creative-lab',native)]:
  estimate=22+sum(compressed[p]+100+2*len(n.encode('utf-8')) for n,p in files.items())+1024*1024
  record={'file':str(args.output_dir/name),'kind':kind,'files':len(files),'raw_bytes':sum(p.stat().st_size for p in files.values()),'estimated_zip_bytes_including_1MiB_metadata_margin':estimate,'below_512MiB_estimate':estimate<LIMIT,'largest_20_by_compressed_bytes':[{'path':n,'raw_bytes':p.stat().st_size,'estimated_compressed_bytes':compressed[p]} for n,p in sorted(files.items(),key=lambda item:compressed[item[1]],reverse=True)[:20]]}
  report['archives'].append(record)
  if estimate>=LIMIT:raise RuntimeError(f'{name} exceeds 512MiB; use --separate-git-history and deliver a complete Git bundle')
  if args.dry_run:continue
  # Only build after freeze. Atomically replace delivery archives after integrity check.
  args.output_dir.mkdir(parents=True,exist_ok=True);fd,temp=tempfile.mkstemp(prefix='revision-',suffix='.zip',dir=args.output_dir);os.close(fd)
  try:
   manifest={'kind':kind,'git_head':head,'git_refs':refs.splitlines(),'files':[{'path':n,'source':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashes[p]} for n,p in sorted(files.items())]}
   prefix='design-grammar/' if kind=='writing-source' else 'creative-lab/'
   with ZipFile(temp,'w',ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for n,p in sorted(files.items()):
     if (p.stat().st_size,p.stat().st_mtime_ns)!=initial[p] or sha(p)!=hashes[p]:raise RuntimeError(f'Source changed during packaging: {p}')
     z.write(p,n)
    z.writestr(prefix+'PACKAGE-README.md',package_notes(kind,head,args.separate_git_history));z.writestr(prefix+'package-manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
   if Path(temp).stat().st_size>LIMIT:raise RuntimeError(f'{name} exceeds the observed 512MiB per-file limit')
   with ZipFile(temp) as z:
    bad=z.testzip()
    if bad:raise RuntimeError('ZIP CRC verification failed: '+bad)
    if any(n.lower().endswith('.pdf') for n in z.namelist()):raise RuntimeError('PDF unexpectedly present in source package')
   if git('rev-parse','HEAD')!=head or git('show-ref')!=refs:raise RuntimeError('Git identity changed during packaging')
   target=args.output_dir/name;os.replace(temp,target);record.update({'actual_zip_bytes':target.stat().st_size,'sha256':sha(target),'crc_verified':True})
  finally:
   if os.path.exists(temp):os.unlink(temp)
 changed=[str(p.relative_to(ROOT)) for p in initial if not p.is_file() or (p.stat().st_size,p.stat().st_mtime_ns)!=initial[p]]
 if changed and not args.dry_run:raise RuntimeError('Inputs changed during packaging: '+', '.join(changed))
 if changed:report['dry_run_inputs_changed_while_estimating']=changed
 args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
