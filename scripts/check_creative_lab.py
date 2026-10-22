#!/usr/bin/env python3
"""Independently audit editable Tingly Design projects; does not rewrite sources.
Set DC_CHROME to a local Chrome/Chromium executable. Run after source freeze.
"""
import argparse, hashlib, html, json, os, re, shutil, subprocess, tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/'examples/creative-lab'
CHROME=os.environ.get('DC_CHROME') or next((shutil.which(n) for n in ['chrome-headless-shell','chromium','chromium-browser','google-chrome','chrome'] if shutil.which(n)),None)
R={'projects':[],'ai_assets':[],'errors':[],'warnings':[]}
def rel(p):
 try:return str(Path(p).relative_to(ROOT))
 except ValueError:return str(p)
def fail(p,message):R['errors'].append({'where':rel(p),'message':message})
def need(p,what):
 if not p.is_file():fail(p,'Missing '+what);return False
 return True
def js(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Markup(HTMLParser):
 def __init__(self,text):
  super().__init__();self.stack=[];self.dc=False;self.root=None;self.props=[];self.texts=[];self.sources=[];self.styles=[];self.scripts=[];self.nodes=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='x-dc':self.dc=True
  if self.dc and tag not in ['x-dc','helmet','style','script'] and not any(x in ['helmet','style','script'] for x in self.stack):
   self.nodes+=1
   if self.root is None:self.root=(tag,a)
  if tag=='script':
   self.scripts.append(a)
   if a.get('type')=='text/x-dc' and 'data-props' in a:
    try:self.props.append(json.loads(a['data-props']))
    except ValueError:self.props.append(None)
  if tag in ['img','source'] and a.get('src'):self.sources.append(a['src'])
  if a.get('style'):self.styles.append(a['style'])
  if tag not in ['img','br','hr','input','meta','link','source','wbr','area','embed']:self.stack.append(tag)
 def handle_endtag(self,tag):
  if tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
  if tag=='x-dc':self.dc=False
 def handle_data(self,data):
  if self.stack and self.stack[-1]=='style':self.styles.append(data)
  if self.dc and not any(x in ['helmet','style','script'] for x in self.stack) and data.strip():self.texts.append(data.strip())
def refs(p,m):
 for ref in m.sources+re.findall(r'''url\(\s*["']?([^\)"']+)''','\n'.join(m.styles)):
  if ref.startswith(('data:','http:','https:','#','blob:')):continue
  need((p.parent/unquote(urlparse(ref).path)).resolve(),'local image/font '+ref)
 for script in m.scripts:
  src=script.get('src','')
  if src and not src.startswith(('http:','https:','data:')) and Path(src).name!='support.js':need(p.parent/src,'local script')
def dimensions(p):
 try:
  with Image.open(p) as im:size=im.size;im.verify()
  return size
 except Exception as exc:fail(p,'Unreadable image: '+str(exc))
def board_renders(project,name,size):
 stem=name.removesuffix('.dc.html');result=[]
 for p in list((project/'renders/check').glob(stem+'.png'))+list((project/'renders/export').glob(stem+'*.png')):
  actual=dimensions(p)
  if actual and actual[0]*size[1]==actual[1]*size[0] and actual[0]>=size[0] and actual[1]>=size[1]:result.append(rel(p))
  elif actual:fail(p,f'Render {actual} disagrees with board ratio/minimum {size}')
 if not result:fail(project,'Missing valid rendered preview '+stem)
 return result
def canvas(project):
 index=js(project/'canvas.json');boards=index.get('boards',{});out={'path':rel(project),'kind':'canvas','boards':[],'snapshots':[]}
 declared=set(boards);actual={str(p.relative_to(project)) for p in project.rglob('*.dc.html') if not any(part in ('ds','renders','restore-backup') for part in p.relative_to(project).parts)}
 if declared!=actual:fail(project,f'Board index/files differ: missing={sorted(declared-actual)}, unindexed={sorted(actual-declared)}')
 for name,b in boards.items():
  p=project/name
  if not need(p,'indexed board'):continue
  m=Markup(p.read_text());refs(p,m);size=(b.get('w'),b.get('h'));record={'file':name,'size':size,'editable_text_nodes':len(m.texts),'native_nodes':m.nodes,'hidden':bool(b.get('hidden'))}
  if not m.root:fail(p,'No editable x-dc root')
  else:
   style=m.root[1].get('style','');dims=[]
   for axis in ['width','height']:
    match=re.search(r'(?:^|;)\s*'+axis+r'\s*:\s*([\d.]+)px',style);dims.append(float(match[1]) if match else None)
   if tuple(dims)!=size:fail(p,f'ROOT {dims} disagrees with canvas index {size}')
  previews=[v['$preview'] for v in m.props if isinstance(v,dict) and '$preview' in v]
  if not previews:fail(p,'Missing $preview dimensions')
  for preview in previews:
   dims=(preview.get('width',preview.get('w')),preview.get('height',preview.get('h')))
   if dims!=size:fail(p,f'$preview {dims} disagrees with canvas index {size}')
  for text in m.texts:
   bad=re.findall(r'(?<!\{)\{\s*[A-Za-z_$][\w$]*(?:\.[\w$]+)*\s*\}(?!\})',text)
   if bad:fail(p,'Unresolved single-brace template text: '+', '.join(bad))
  if not m.texts or m.nodes<2:fail(p,'Board lacks editable text/structure; possible flattened page')
  if not b.get('hidden'):record['renders']=board_renders(project,name,size)
  out['boards'].append(record)
 for snap in index.get('designSystems',[]):
  installed=project/'ds'/snap.get('namespace','');artifact=snap.get('artifact','');source=(project/artifact).resolve() if artifact.startswith('.') else LAB/Path(artifact).name
  if not need(source/'tokens.json','upstream tokens') or not need(installed/'tokens.json','snapshot tokens'):continue
  tokens=js(source/'tokens.json')
  if tokens!=js(installed/'tokens.json'):fail(installed,'Installed tokens differ from declared upstream '+rel(source))
  for font in tokens.get('type',{}).get('fonts',[]):
   if not font.get('file'):continue
   a=source/font['file'];b=installed/font['file']
   if need(a,'source font') and need(b,'snapshot font') and sha(a)!=sha(b):fail(b,'Snapshot font differs from upstream')
  out['snapshots'].append({'namespace':snap.get('namespace'),'upstream':rel(source),'tokens_sha256':sha(installed/'tokens.json')})
 if not out['snapshots']:fail(project,'No traceable installed design-system snapshot')
 return out
def runtime(project,name,namespace,names):
 preview=project/'components'/name/'preview.html'
 if not need(preview,'component preview'):return
 original=preview.read_text();refs(preview,Markup(original))
 setup="<script>window.__audit={calls:{},errors:[]};window.__returned=[];window.addEventListener('error',e=>__audit.errors.push(e.message));</script>"
 setup+=''.join('<link rel="stylesheet" href="'+(project/p).as_uri()+'">' for p in ['tokens.css','components/bundle.css'])
 setup+='<script src="'+(project/'components/bundle.js').as_uri()+'"></script>'
 setup+='<script>(()=>{const n=window['+json.dumps(namespace)+'];for(const k of '+json.dumps(names)+'){if(typeof n?.[k]!=="function"){__audit.errors.push("Missing function "+k);continue;}const old=n[k];n[k]=function(...a){__audit.calls[k]=(__audit.calls[k]||0)+1;const v=old.apply(this,a);if(!(v instanceof Node))__audit.errors.push(k+" did not return a DOM node");__returned.push(v);return v;};}})();</script>'
 end="<script>setTimeout(()=>{const p=document.createElement('pre');p.id='native-audit-result';p.textContent=JSON.stringify({...__audit,nodes:document.body.querySelectorAll('*').length,connected_returns:__returned.filter(n=>n?.isConnected).length});document.body.appendChild(p);},300);</script>"
 with tempfile.TemporaryDirectory(prefix='dc-audit-') as temp:
  page=Path(temp)/'preview.html';page.write_text('<base href="'+preview.parent.as_uri()+'/">'+setup+original+end)
  run=subprocess.run([CHROME,'--headless','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--virtual-time-budget=1200','--dump-dom',page.as_uri()],capture_output=True,text=True,timeout=30)
 match=re.search(r'<pre id="native-audit-result">(.*?)</pre>',run.stdout,re.S)
 if not match:fail(preview,'Actual browser execution returned no audit result');return
 data=json.loads(html.unescape(match[1]))
 for message in data['errors']:fail(preview,'Browser preview: '+message)
 if not data['calls'].get(name):fail(preview,'Preview never invokes its exported component function')
 if not data['connected_returns']:fail(preview,'No returned component node attached to preview DOM')
 return {'component':name,'calls':data['calls'],'rendered_nodes':data['nodes'],'connected_returns':data['connected_returns']}
def system(project):
 index=js(project/'design-system.json');tokens=js(project/'tokens.json');out={'path':rel(project),'kind':'design-system','components':[],'renders':[]}
 for name in ['tokens.css','components/bundle.js','components/bundle.css','components/index.d.ts']:need(project/name,'native component contract file')
 for font in tokens.get('type',{}).get('fonts',[]):
  if font.get('file'):need(project/font['file'],'declared font')
 bundle=(project/'components/bundle.js').read_text();match=re.search(r'@ds-bundle:\s*(\{.*?\})\s*\*/',bundle,re.S)
 if not match:fail(project,'Missing @ds-bundle metadata');return out
 meta=json.loads(match[1]);namespace=meta.get('namespace');names=[c['name'] for c in meta.get('components',[])];primary=[n for n in names if n!='Cover'];out['namespace']=namespace
 if len(primary)<3:fail(project,'Fewer than three exported reusable components')
 for name in primary:
  need(project/'components'/name/'README.md','component documentation')
  if CHROME:
   data=runtime(project,name,namespace,names)
   if data:out['components'].append(data)
 for view in ['overview','colors','type','space','components','assets']:
  images=list((project/'renders/check').glob('*-'+view+'.png'))+list((project/'renders/export').glob('*-'+view+'*.png'))
  if not images:fail(project,'Missing native rendered design-system view '+view)
  for p in images:
   size=dimensions(p)
   if size and (size[0]<800 or size[1]<500):fail(p,'Design-system render too small')
   if size:out['renders'].append({'file':rel(p),'size':size})
 return out
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,default=ROOT/'build/creative-lab-audit.json');args=ap.parse_args()
 if not CHROME:fail('environment','Set DC_CHROME or install Chrome/Chromium on PATH for actual component execution')
 for prefix in ['refraction','field','still']:
  for suffix,fn in [('system',system),('canvas',canvas)]:
   project=LAB/(prefix+'-'+suffix)
   try:R['projects'].append(fn(project))
   except Exception as exc:fail(project,type(exc).__name__+': '+str(exc))
 logpath=LAB/'shared-assets/generation-log-v5.json'
 try:
  for asset in js(logpath)['assets']:
   p=logpath.parent/asset['file']
   if not need(p,'logged AI asset'):continue
   size=dimensions(p);checksum=sha(p)
   if checksum!=asset['sha256']:fail(p,'AI material hash differs from generation log')
   if size!=(asset['width'],asset['height']):fail(p,'AI material dimensions differ from generation log')
   if p.stat().st_size!=asset['size_bytes']:fail(p,'AI material byte length differs from generation log')
   copies=[]
   for copy in LAB.rglob(asset['file']):
    if copy==p:continue
    if sha(copy)!=checksum:fail(copy,'Project material differs from logged AI original')
    copies.append(rel(copy))
   book_copy=asset.get('book_copy')
   if book_copy:
    book_path=ROOT/book_copy
    if need(book_path,'book copy of full AI proposal') and sha(book_path)!=checksum:fail(book_path,'Book proposal differs from generation log')
   project_name=asset.get('project') if asset.get('role')=='text_free_material' else None
   if project_name:
    current=LAB/(project_name+'-canvas');idx=js(current/'canvas.json')
    if not any(asset['file'] in (current/name).read_text() for name in idx['boards']):fail(current,'New AI material is not referenced by any current editable board')
   R['ai_assets'].append({'file':rel(p),'sha256':checksum,'size':size,'verified_project_copies':copies})
  if len(R['ai_assets'])!=4:fail(logpath,'Expected one complete AI visual proposal and three text-free materials with provenance')
  concept=next((a for a in js(logpath)['assets'] if a.get('role')=='full_visual_proposal'),None)
  if not concept:fail(logpath,'Missing complete AI visual proposal provenance')
  elif concept['file'] in (LAB/'refraction-canvas/Main.dc.html').read_text():fail(LAB/'refraction-canvas/Main.dc.html','Complete proposal bitmap used in the native rebuild; use the text-free material')
 except Exception as exc:fail(logpath,str(exc))
 R['summary']={'projects':len(R['projects']),'canvas_boards':sum(len(p.get('boards',[])) for p in R['projects']),'component_previews_executed':sum(len(p.get('components',[])) for p in R['projects']),'errors':len(R['errors']),'warnings':len(R['warnings'])}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(R,ensure_ascii=False,indent=2)+'\n');print(json.dumps(R['summary']));print(args.output);raise SystemExit(bool(R['errors']))
if __name__=='__main__':main()
