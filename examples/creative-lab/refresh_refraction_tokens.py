"""Trigger the official Tingly Design token compiler; never hand-write tokens.css.
Run after build_refraction_v5.py. Optional TINGLY_DESIGN_CLI points at native cli.mjs.
"""
from pathlib import Path
import subprocess,urllib.request,json,os
BASE=Path(__file__).resolve().parent
cli=os.environ.get('TINGLY_DESIGN_CLI');cmd=['node',cli] if cli else ['npx','--yes','tingly-design@0.26.1021']
p=subprocess.Popen(cmd+['serve','--projects',str(BASE),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
try:
 port=None
 for s in p.stdout:
  if 'TINGLY_DESIGN_READY ' in s:port=json.loads(s.split('TINGLY_DESIGN_READY ')[1])['port'];break
 if not port:raise RuntimeError('Native service did not start.')
 origin=f'http://127.0.0.1:{port}'
 d=json.load(urllib.request.urlopen(origin+'/api/projects/refraction-system/files'))['files']['tokens.json']
 # Whitespace changes content without changing token values; same-content PUT returns early.
 content=d['content'].rstrip()+('\n\n' if not d['content'].endswith('\n\n') else '\n')
 data=json.dumps({'content':content,'baseVersion':d['version'],'actor':'claude','summary':'Refresh generated CSS from final custom tokens'}).encode()
 req=urllib.request.Request(origin+'/api/projects/refraction-system/file?path=tokens.json',data=data,method='PUT',headers={'Content-Type':'application/json'})
 json.load(urllib.request.urlopen(req))
 assert '--surface: #F2EDDF;' in (BASE/'refraction-system/tokens.css').read_text()
 print('Native token CSS refreshed; generated CSS was not hand-written.')
finally:
 p.terminate()
 try:p.wait(timeout=10)
 except subprocess.TimeoutExpired:p.kill();p.wait()
