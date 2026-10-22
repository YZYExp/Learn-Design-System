"""Install FIELD NOTES with the native API and generate native tokens.css.

Usage: python3 source/install_field.py --cli /path/to/tingly-design/cli.mjs
The server and the HTTP call live in one process network namespace, which is
necessary in managed workspaces. Only the two field projects are written.
"""
from pathlib import Path
import argparse,json,subprocess,urllib.request,socket
p=argparse.ArgumentParser();p.add_argument('--cli',required=True);args=p.parse_args()
ROOT=Path(__file__).resolve().parents[2]
with socket.socket()as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
server=subprocess.Popen(['node',args.cli,'serve','--projects',str(ROOT),'--port',str(port),'--json'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
def call(path,body=None,method='GET'):
 req=urllib.request.Request(f'http://127.0.0.1:{port}'+path,data=json.dumps(body).encode()if body is not None else None,headers={'Content-Type':'application/json'},method=method)
 return json.loads(urllib.request.urlopen(req,timeout=30).read())
try:
 for line in server.stdout:
  if 'TINGLY_DESIGN_READY' in line:break
 files=call('/api/projects/field-system/files')['files']
 cur=files['tokens.json']if isinstance(files,dict)else next(x for x in files if x.get('path')=='tokens.json')
 # An actual native write triggers the editor's token stylesheet compiler.
 content=cur['content'];content=content.rstrip()+'\n' if content.endswith('\n\n')else content+'\n'
 compiled=call('/api/projects/field-system/file?path=tokens.json',{'content':content,'baseVersion':cur['version'],'actor':'ai','summary':'Compile authored tokens with native design-system compiler.'},'PUT')
 installed=call('/api/projects/field-canvas/design-systems',{'from':'field-system'},'POST')
 print(json.dumps({'token_compilation':compiled,'native_installation':installed},ensure_ascii=False,indent=2))
finally:
 server.terminate();server.wait(timeout=15)
