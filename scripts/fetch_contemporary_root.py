from pathlib import Path
import urllib.request,re,html,json
from PIL import Image,ImageOps,ImageDraw
r=Path(__file__).resolve().parents[1]; out=r/'assets/images'; rec=[]
cache=r/'build/contemporary';cache.mkdir(parents=True,exist_ok=True)
for name,url in [('reddit','https://www.pentagram.com/work/reddit')]:
 if not (cache/(name+'.html')).exists():
  (cache/(name+'.html')).write_bytes(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read())
def get(name,url,page):
 try:
  b=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read();p=out/name;p.write_bytes(b)
  with Image.open(p) as im: print(name,im.size)
  rec.append({'file':str(p.relative_to(r)),'kind':'real_artwork','source_url':page,'image_url':url,'creator':'品牌及其设计合作团队','rights':'品牌与原作者保留权利；用于教学评论，非本书原创'})
 except Exception as e: print(name,str(e))
base='https://digitalassets.pepsico.com/transform/'
for k,(u,n) in enumerate([('528ba772-b67a-4e5c-8ec8-13ccc101136b','pepsi-global-redesign_image_912x592_9'),('c00a495a-fbc7-4ee5-86a8-435af166dc2c','Innovation-Design-Merchandising-Bento'),('f0467448-e353-49cb-84ed-b7476b9a0869','pepsi-global-redesign_image_912x592_10'),('bc6427f4-57ce-48a7-a41d-9100901e6b81','Pepsi-immersive-wall')]):get(f'contemporary-pepsi-{k+1}.jpg',base+u+'/'+n+'?w=1800&q=90','https://www.pepsico.com/en/innovation/case-studies/2023/pepsi-global-redesign')
s=(r/'build/contemporary/reddit.html').read_text();urls=html.unescape(s).replace('\\u0026','&');urls=re.findall(r'https://pentagram-production.imgix.net/[^\s"<>]+',urls)
for k,stem in enumerate(['Reddit_Thumbnail.jpg','06_Reddit_CaseStudy_Patches.jpg','15_Reddit_CaseStudy_PhoneCase.jpg','04_Reddit_CaseStudy_TypeSequencecopy.jpg']):
 cand=[x.split(',https://')[0] for x in urls if stem in x];u=cand[0].split(' ')[0] if cand else ''
 if u:get(f'contemporary-reddit-{k+1}.jpg',u,'https://www.pentagram.com/work/reddit')
for k,u in enumerate(['https://wise.com/imaginary-v2/3496b05316968ddca00dd679c2a11b14.png','https://wise.com/imaginary/00f24d7b0ebca6298f098eb3a8d4e548.png','https://wise.com/imaginary/4d3177232f398caf4327b7d2fec822fb.png']):get(f'contemporary-wise-{k+1}.png',u,'https://wise.com/gb/blog/a-brand-for-everywhere-wise-unveils-bold-new-look')
rec=[a for a in rec if not a['file'].endswith(('pepsi-3.jpg','reddit-4.jpg'))]
(r/'references/revision-contemporary-root-images.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2))
ims=[]
for a in rec:
 with Image.open(r/a['file']) as im: ims.append((Path(a['file']).name,ImageOps.contain(im.convert('RGB'),(440,260))))
sheet=Image.new('RGB',(1320,310*((len(ims)+2)//3)),'white');d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(ims):x=i%3*440;y=i//3*310;sheet.paste(im,(x,y+30));d.text((x+10,y+5),name,fill='black')
sheet.save(r/'build/contemporary/contact.jpg')
