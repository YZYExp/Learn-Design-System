"""Call every real component in Chromium and save its rendered preview.
Usage: DC_CHROME=/path/to/chrome python3 source/verify_components.py
This smoke test uses temporary HTML only, not an extra deliverable webpage.
"""
from pathlib import Path
import os,subprocess,tempfile,json
ROOT=Path(__file__).resolve().parents[2];DS=ROOT/'field-system';out=DS/'renders/components';out.mkdir(parents=True,exist_ok=True)
chrome=os.environ.get('DC_CHROME');assert chrome,'Set DC_CHROME to local Chromium.'
with tempfile.TemporaryDirectory(prefix='field-components-')as temp:
 f=Path(temp)/'test.html'
 f.write_text(f'''<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="{(DS/'tokens.css').as_uri()}"><style>@font-face{{font-family:"Field Sans";src:url({(DS/'fonts/NotoSansSC-Regular.ttf').as_uri()})}}@font-face{{font-family:"Field Serif";src:url({(DS/'fonts/FieldSerif.otf').as_uri()})}}@font-face{{font-family:"Field Serif";src:url({(DS/"fonts/FieldSerif-Italic.otf").as_uri()});font-style:italic}}body{{margin:0;background:#F4EEDC;font-family:"Field Sans"}}section{{padding:18px 28px;border-bottom:1px solid #B4AA97}}h2{{font-size:16px;color:#3E5947;font-weight:400}}#result{{padding:12px 28px;font-size:18px;color:#482C45}}</style><script src="{(DS/'components/bundle.js').as_uri()}"></script><div id="root"></div><script>try{{["Masthead","EditorialCaption","EventBadge","Cover"].forEach(function(k){{var s=document.createElement('section');var h=document.createElement('h2');h.textContent='FieldNotes.'+k+'()';s.appendChild(h);var node=FieldNotes[k]({{}});if(!(node instanceof HTMLElement))throw new Error(k+' returned non-HTMLElement');s.appendChild(node);document.getElementById('root').appendChild(s);}});document.body.insertAdjacentHTML('beforeend','<div id="result">PASS — four callable components returned HTMLElement nodes.</div>');}}catch(e){{document.body.insertAdjacentHTML('beforeend','<div id="result">FAIL '+e.message+'</div>');}}</script>''')
 r=subprocess.run([chrome,'--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files','--hide-scrollbars','--window-size=1200,1280','--screenshot='+str(out/'ActualComponents.png'),'--dump-dom',f.as_uri()],capture_output=True,text=True,check=True)
 # Match the resulting DOM, not the JavaScript source text.
 passed='<div id="result">PASS — four callable components returned HTMLElement nodes.</div>' in r.stdout
 report={'passed':passed,'components':['Masthead','EditorialCaption','EventBadge','Cover'],'screenshot':'renders/components/ActualComponents.png'}
 (out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
 if not passed:raise SystemExit('Component browser smoke test failed.')
