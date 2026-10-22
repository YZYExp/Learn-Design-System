"""Download only the specific primary-source brand images used in these research drafts."""
from pathlib import Path
import urllib.request,concurrent.futures,json
from PIL import Image
R=Path(__file__).resolve().parents[2];O=R/'assets/images';records=[]
PRIMARY={'spotify':'https://newsroom.spotify.com/2024-05-22/introducing-spotify-mix-our-new-and-exclusive-font/','figma':'https://www.figma.com/blog/how-we-shaped-the-visual-identity-for-config-2025/','decathlon':'https://www.wolffolins.com/work/decathlon'}
DATA=[
('spotify','font-source','https://storage.googleapis.com/pr-newsroom-wp/1/2024/05/FTR-header-SPOTIFY-1.gif','Spotify Mix字体动态展示','gif'),
('spotify','playlists','https://storage.googleapis.com/pr-newsroom-wp/1/2024/05/updated-playlists.png','不同歌单封面中的字体组织','png'),
('spotify','interface','https://storage.googleapis.com/pr-newsroom-wp/1/2024/05/iOS-Home.jpg','Spotify手机首页界面','jpg'),
('figma','wayfinding','https://cdn.sanity.io/images/599r6htc/regionalized/770ed1c40f5906b86c0c5f45a7267dded60382ab-1056x1408.png','Config2025现场导视','png'),
('figma','inflatables','https://cdn.sanity.io/images/599r6htc/regionalized/46066c76cc168a04eee14a7e8a04df9587a3a865-2160x1213.png','Config2025充气glyph与空间','png'),
('figma','posters','https://cdn.sanity.io/images/599r6htc/regionalized/9f9fc00fd8cd8668b0b0ed849b60984e91c47d1a-1608x1608.png','Config2025海报墙','png'),
('figma','badge-type','https://cdn.sanity.io/images/599r6htc/regionalized/a9c97fbd0f4d82ca9ecd5fc4d3f3772e0367649f-1884x1058.png','Config2025字体贴纸','png'),
('decathlon','campaign','https://images.ctfassets.net/4rnblstkg79m/76vSqlHWC5fU8QN9mu9hy6/2ec48a9ff89d362befb03e23e08951f7/DKT_CS_04_Walkers_KV_3000x2000.jpeg','Decathlon户外行走主视觉','jpg'),
('decathlon','jersey','https://images.ctfassets.net/4rnblstkg79m/6w1r9TioXMAV105cAeL2Zq/137036bb0ad5d99a4a38dd444cb52595/DKT_CS_06_Jersey_Orbit_1500x2000.jpg','Decathlon球衣上的Orbit应用','jpg'),
('decathlon','typography','https://images.ctfassets.net/4rnblstkg79m/4AqdPGJ7u0RRku5REjRe11/e976c3f161f9df1da50d7d89b19fa1d4/DKT_CS_14_Move_Type_3000x2000.jpg','Decathlon Sans文字构成','jpg'),
('decathlon','cycling','https://images.ctfassets.net/4rnblstkg79m/5kVe6nzYc8UiY4yGMYC3xh/060503949fe2ed821f55731d0e152718/DKT_CS_27_Cyclist_Orbit_3000x2000-2.jpg','Decathlon骑行广告构成','jpg')]
def fetch(x):
 b,n,u,title,ext=x;f=f'contemporary-{b}-{n}.{ext}';p=O/f
 if not p.exists():p.write_bytes(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read())
 with Image.open(p) as im:im.verify()
 with Image.open(p) as im:wh=im.size
 creator={'spotify':'Spotify Brand and Creative team；Dinamo Typefaces（字体）','figma':'Figma Brand Studio；Leandro Castelao（Config 2025创意主导）。摄影按官方文章总署名Desmond Studio、VTProDesign、STMNT Studios、Maria Chimishkyan；单图未逐一指派。','decathlon':'Decathlon × Wolff Olins；Decathlon Sans由Grilli Type设计。案例页总署名含FourOneNine、Jamie Mourn摄影及Studio PIC三维，未擅自将总署名分配到单张。'}[b]
 return {'file':f,'kind':'real_artwork','brand':b,'creator':creator,'title':title,'date':{'spotify':'2024-05-22 官方发布','figma':'2025项目；官方文章2025-07-03','decathlon':'2024品牌发布；官方发布2024-03-12，案例页未逐图标注制作日'}[b],'primaryURL':PRIMARY[b],'source':PRIMARY[b],'image_url':u,'downloadURL':u,'rights':f'© {b.title()}及相应设计/摄影权利人；官方案例公开展示图，本书研究分析引图，未声明开放许可。','width':wh[0],'height':wh[1],'retrieved':'2026-10-22'}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for r in pool.map(fetch,DATA):records.append(r);print(r['file'],r['width'],r['height'])
(R/'references/revision-contemporary-history-images.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
