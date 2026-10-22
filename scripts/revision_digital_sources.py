"""Re-download cited revision images without changing their provenance records.

Run from any directory: python scripts/revision_digital_sources.py
Network access is required; no API credentials are required.
"""
from pathlib import Path
from io import BytesIO
from PIL import Image
import concurrent.futures,json,urllib.request,fitz
R=Path(__file__).resolve().parents[1];D=R/'assets/images';B=R/'build/revision-digital'
D.mkdir(exist_ok=True);B.mkdir(parents=True,exist_ok=True)
meta=json.loads((R/'references/revision-digital-images.json').read_text())
def get(url):
 return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read()
def atomic(path,data):
 tmp=path.with_name(path.name+'.tmp');tmp.write_bytes(data);tmp.replace(path)
def download(m):
 f=R/m['file']
 if f.exists():
  with Image.open(f) as im:im.verify()
  return f.name,'verified existing'
 u=m.get('download_url')
 if not u:return f.name,'generated from official PDF by analysis script'
 data=get(u)
 with Image.open(BytesIO(data)) as im:im.verify()
 atomic(f,data)
 return f.name,'downloaded verified'
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for result in pool.map(download,[m for m in meta if m['kind']=='real_artwork']):print(*result)
pdf=B/'gov-report.pdf'
if not pdf.exists():
 atomic(pdf,get('https://assets.publishing.service.gov.uk/media/66e447b50d913026165c3e9b/Recommended_method_of_submission_guidance.pdf'))
doc=fitz.open(pdf);out=D/'revision-digital-gov-page13.png';tmp=out.with_name(out.stem+'.tmp.png')
doc[12].get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(tmp);tmp.replace(out)
print('official PDF input ready; run revision_digital_analysis.py for labelled reading plates')
