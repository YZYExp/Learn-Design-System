"""Exact frames/crops of researched originals; no generated replacement artwork."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json
R=Path(__file__).resolve().parents[2];O=R/'assets/images';F=R/'assets/fonts/NotoSansSC-Regular.ttf';M=R/'references/revision-contemporary-history-images.json'
records=json.loads(M.read_text());records=[r for r in records if r.get('kind')!='original_analysis' and r.get('file')!='contemporary-spotify-font-rules.png']
im=Image.open(O/'contemporary-spotify-font-source.gif');im.seek(35);im.convert('RGB').save(O/'contemporary-spotify-font-rules.png')
r=next(r for r in records if r['file']=='contemporary-spotify-font-source.gif').copy();r.update({'file':'contemporary-spotify-font-rules.png','title':'Spotify官方字体动画第35帧（零起）','transformation':'原动画静态取帧，未重绘轮廓或加入字形','source_file':'contemporary-spotify-font-source.gif'});records.append(r)
font=lambda n:ImageFont.truetype(str(F),n)
def text(im,x,y,s,n=28):ImageDraw.Draw(im).text((x,y),s,font=font(n),fill='#202020')
def put(out,file,box,crop=None):
 im=Image.open(O/file).convert('RGB');im=im.crop(crop) if crop else im;im=ImageOps.contain(im,(box[2]-box[0],box[3]-box[1]));out.paste(im,(box[0]+(box[2]-box[0]-im.width)//2,box[1]+(box[3]-box[1]-im.height)//2))
def save(out,brand,title,sources,change):
 file=f'contemporary-{brand}-analysis.png';tmp=O/(file+'.tmp.png');out.save(tmp);tmp.replace(O/file);records.append({'file':file,'kind':'original_analysis','brand':brand,'creator':'本书原创分析编排；原图作者与权利人见对应原作记录','author':'本书','title':title,'date':'2026-10-22','primaryURL':sources,'source':sources,'rights':'中文标签与编排为本书原创；实际原作裁切/取帧保留原权利人归属，不声明整图开放许可。','transformation':change,'width':out.width,'height':out.height})
# Spotify: exact original cover versus real interface crop, no fake gray bars.
out=Image.new('RGB',(1600,1000),'#f4f4ef');text(out,55,25,'Spotify：让表达与检索分工',44);text(out,55,92,'左：官方歌单应用原图。右：官方手机界面上部实际裁切。标签是本书观察，未改写原界面。',24)
put(out,'contemporary-spotify-playlists.png',(45,175,1120,805));put(out,'contemporary-spotify-interface.jpg',(1170,175,1550,805),(0,0,390,650));text(out,60,850,'封面：字形、大小与人物裁切一起制造差别。',29);text(out,60,915,'界面：标题与导航回到稳定字阶；不能从成品图反推每个封面的字体参数。',26)
save(out,'spotify','Spotify歌单与界面实际原图对照',['https://newsroom.spotify.com/2024-05-22/introducing-spotify-mix-our-new-and-exclusive-font/'],'左图缩放不改内容，右图裁切原截图0,0,390,650；中文标签另加。')
# Config: exact original sign and actual type/arrow details.
out=Image.new('RGB',(1600,1000),'#f7f3e9');text(out,55,25,'Config 2025：先去哪里，再看品牌的表情',44);text(out,55,92,'实际导视照片与两处局部；框线、解释为本书分析，不是Figma官方规范值。',25)
put(out,'contemporary-figma-wayfinding.png',(55,150,690,930));put(out,'contemporary-figma-wayfinding.png',(780,190,1520,485),(100,120,1020,600));put(out,'contemporary-figma-wayfinding.png',(780,545,1520,805),(130,850,1020,1350));text(out,790,150,'方向在左侧；词组保持连贯。',28);text(out,790,850,'相同的紧凑字形，容纳长短不一的地点名。',26)
save(out,'figma','Config2025实际导视与层级细读',['https://www.figma.com/blog/how-we-shaped-the-visual-identity-for-config-2025/'],'全图加两处实际局部裁切；无生成形状或假指示牌。')
# Decathlon: actual type and product context, same marks perform different jobs.
out=Image.new('RGB',(1600,1000),'#f1f2f3');text(out,55,25,'Decathlon：大画面的动势，小尺度的识别',44);text(out,55,92,'文字实验、球衣与运动摄影均来自Wolff Olins官方项目图。',25)
put(out,'contemporary-decathlon-typography.jpg',(55,160,810,675));put(out,'contemporary-decathlon-jersey.jpg',(880,155,1525,900));text(out,60,730,'大字：角度、笔画和裁切承担表达。',28);text(out,60,795,'衣物：标记让位给身体与材料。',28);text(out,60,885,'这是一组可见应用的比较，不据图片宣布销量或识别率提升。',25)
save(out,'decathlon','Decathlon实际文字与球衣应用对照',['https://www.wolffolins.com/work/decathlon','https://www.decathlon-united.media/decathlon-new-identity'],'原图仅缩放并列，中文观察标签另加；不重画品牌符号。')
for r in records:
 r.setdefault('author',r.get('creator'))
 r.setdefault('articleAuthor',{'spotify':'Spotify Newsroom；访谈Rasmus Wängelin','figma':'Matt Alagiah','decathlon':'Wolff Olins官方机构案例页，未单署撰文者'}.get(r.get('brand'),''))
 if r.get('brand')=='decathlon':r['additionalPrimaryURL']='https://www.decathlon-united.media/decathlon-new-identity'
M.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print('Exact font frame and 3 analysis figures saved; manifest',len(records))
