"""Fetch three Met Open Access images with full attribution; refuse non-public-domain records."""
from pathlib import Path
import json, urllib.request, concurrent.futures
ROOT=Path(__file__).resolve().parents[1]
ITEMS=[(384017,'reference-morris-daisy.jpg'),(39664,'reference-korin-yatsuhashi.jpg'),(30091,'reference-naomasa-tsuba.jpg')]
def fetch(item):
 oid,name=item
 req=urllib.request.Request(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}',headers={'User-Agent':'DesignGrammarEducationalBook/1.0'})
 with urllib.request.urlopen(req,timeout=45) as res: d=json.load(res)
 if not d['isPublicDomain'] or not d['primaryImage']: raise ValueError(f'No confirmed Open Access image: {oid}')
 with urllib.request.urlopen(d['primaryImage'],timeout=60) as res: image=res.read()
 dest=ROOT/'assets/images'/name;dest.write_bytes(image)
 return {'file':f'assets/images/{name}','artist':d['artistDisplayName'],'title':d['title'],'date':d['objectDate'],'institution':'The Metropolitan Museum of Art','objectID':d['objectID'],'accessionNumber':d['accessionNumber'],'medium':d['medium'],'objectURL':d['objectURL'],'imageURL':d['primaryImage'],'isPublicDomain':d['isPublicDomain'],'license':'Public Domain / The Met Open Access (CC0)','licenseURL':'https://www.metmuseum.org/about-the-met/policies-and-documents/open-access','retrieved':'2026-10-21'}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: records=list(pool.map(fetch,ITEMS))
 (ROOT/'references/history-image-sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
 for record in records: print(record['file'],record['title'],record['date'])
