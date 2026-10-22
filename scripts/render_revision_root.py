#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json,fitz
R=Path(__file__).resolve().parents[1];O=R/'assets/images';FONT=R/'assets/fonts/NotoSansSC-Regular.ttf';entries=[]
def ft(n):return ImageFont.truetype(str(FONT),n)
def tx(d,x,y,s,n=30,c='#222222'):d.text((x,y),s,font=ft(n),fill=c)
def fit(im,box):
 im=im.copy().convert('RGB');im.thumbnail((box[2]-box[0],box[3]-box[1]));return im,(box[0]+(box[2]-box[0]-im.width)//2,box[1]+(box[3]-box[1]-im.height)//2)
def paste(im,p,box):
 q,xy=fit(p,box);im.paste(q,xy);return q,xy

def board(title,w=1800,h=1120):
 im=Image.new('RGB',(w,h),'#FBF8F0');d=ImageDraw.Draw(im);tx(d,65,45,title,44);return im,d

def save(im,name,title,source):
 dest=O/name;tmp=O/(name+'.tmp.png');im.save(tmp,format='PNG',optimize=True);tmp.replace(dest);entries.append({'file':name,'kind':'original_analysis','title':title,'source':source,'method':'原创标注/对照；原作处理方式见图注，不伪称原作'})
# Hokusai - retain actual print, mark regions and read down to labels.
im,d=board('《神奈川冲浪里》：把主次放在不同的尺度上')
src=Image.open(O/'revision-root-hokusai.jpg');q,xy=paste(im,src,(70,140,1730,850))
for n,box,c in [(1,(.03,.05,.57,.70),'#B75C16'),(2,(.15,.65,.88,.94),'#2A5687'),(3,(.56,.61,.67,.79),'#A43148')]:
 b=(xy[0]+q.width*box[0],xy[1]+q.height*box[1],xy[0]+q.width*box[2],xy[1]+q.height*box[3]);d.rectangle(b,outline=c,width=7);d.ellipse((b[0],b[1],b[0]+48,b[1]+48),fill=c);tx(d,b[0]+13,b[1],str(n),32,'#fff')
for i,(a,b) in enumerate([('1 巨浪：大轮廓先抓注意','弧形向内卷，包围天空与远山'),('2 船身：长线带出方向','细长浅面与水线交错，暗示处境'),('3 富士：小形仍有身份','三角轮廓、空隙和重复视图提供辨认')]):
 x=70+i*570;tx(d,x,900,a,29);tx(d,x,955,b,24,'#4D5254')
save(im,'revision-root-hokusai-analysis.png','Hokusai构图三层标注','https://www.metmuseum.org/art/collection/search/45434')
# Van Gogh actual and grayscale, no claim historical pigment measurement.
im,d=board('颜色与明暗要分开看：原作 / 灰度分析 / 近似角色色')
src=Image.open(O/'revision-root-vangogh.jpg').convert('RGB');paste(im,src,(60,160,870,790));paste(im,ImageOps.grayscale(src),(930,160,1740,790))
tx(d,65,825,'原作：暖黄麦田、冷蓝天空、深绿柏树',31);tx(d,930,825,'灰度处理：检查深浅骨架，不能评判原作色相',29)
for x,c,l in [(65,'#B99E4F','大面积暖色'),(340,'#8EB3B7','大面积冷色'),(615,'#244B41','小面积深色')]:d.rectangle((x,915,x+175,1010),fill=c);tx(d,x,1025,l,25)
save(im,'revision-root-vangogh-analysis.png','Van Gogh色彩与灰度分析','https://www.metmuseum.org/art/collection/search/436535')
# Tschichold region map; uses the exact actual version.
im,d=board('《先锋派海报展》：空白把信息分为三次阅读')
src=Image.open(O/'revision-root-tschichold.jpg');q,xy=paste(im,src,(70,160,1120,1010))
for n,b,c in [(1,(.01,.01,.96,.25),'#25627A'),(2,(.01,.26,.99,.44),'#9B3042'),(3,(.68,.43,.99,.82),'#76632D'),(4,(.01,.86,.99,.99),'#4D6560')]:
 box=(xy[0]+q.width*b[0],xy[1]+q.height*b[1],xy[0]+q.width*b[2],xy[1]+q.height*b[3]);d.rectangle(box,outline=c,width=5)
 tx(d,box[0]+6,box[1]+2,str(n),27,c)
for i,t in enumerate(['1 顶部：场所与组织身份','2 红色大标题：主题入口','3 右侧名单：密度集中成块','4 底部细线：日期与到访条件','空白：让这些角色互不挤压']):tx(d,1180,235+i*130,t,29)
save(im,'revision-root-tschichold-analysis.png','Tschichold展览海报的阅读角色标注','https://www.moma.org/collection/works/7292')
# Full practical redesign exercise using a public domain Hokusai artwork.
im,d=board('同一场版画讲座：从堆信息，到安排观看',1800,1380)
for i,l in enumerate(['A：所有信息同样强烈','B：主题与参加条件分层','C：图像参与主题与节奏']):
 x=55+i*590;d.rectangle((x,140,x+550,1260),fill='#FFFDF7',outline='#D9D5CC',width=3);tx(d,x+20,160,l,26)
 if i==0:
  for k,t in enumerate(['版画中的海与山','公众讲座','11月15日 19:00','市美术馆教育厅','葛饰北斋与系列图像']):tx(d,x+25,250+k*95,t,31,'#143F6C')
  paste(im,Image.open(O/'revision-root-hokusai.jpg'),(x+20,790,x+530,1140))
 elif i==1:
  tx(d,x+32,250,'版画中的',51,'#173F68');tx(d,x+32,330,'海与山',73,'#173F68');tx(d,x+34,465,'葛饰北斋与系列图像',30)
  paste(im,Image.open(O/'revision-root-hokusai.jpg'),(x+25,570,x+525,950));tx(d,x+34,1030,'11月15日 19:00',32);tx(d,x+34,1090,'市美术馆教育厅',29)
 else:
  tx(d,x+32,250,'海',104,'#173F68');tx(d,x+185,330,'与山',77,'#173F68');paste(im,Image.open(O/'revision-root-hokusai.jpg'),(x+20,490,x+530,940));tx(d,x+32,990,'版画中的尺度与系列',30);tx(d,x+32,1070,'11月15日 19:00',32);tx(d,x+32,1130,'市美术馆教育厅 · 公众讲座',26)
 tx(d,x+25,1205,'虚构教学活动，不提供预约/导览功能',20,'#6A6A65')
save(im,'revision-root-poster-rewrite.png','公众讲座海报的三步原创改稿','https://www.metmuseum.org/art/collection/search/45434')
# Packaging: bottle silhouette inference separated from exact original.
im,d=board('包装有三个观察层：轮廓 / 字面 / 使用路径')
src=Image.open(O/'revision-root-coke-timeline.jpg');paste(im,src,(60,150,1740,750))
for i,(t,sub) in enumerate([('轮廓层','遮住标签，比较肩、腰、底与纵向沟纹'),('图文层','字标和标签能变；不把某种红当全部身份'),('任务层','握持、开启、倒出、回收分别提出要求')]):
 x=70+i*570;tx(d,x,820,t,36);tx(d,x,895,sub,25)
save(im,'revision-root-packaging-analysis.png','Coca-Cola瓶型演变的三层观察','https://www.coca-colacompany.com/about-us/history/the-history-of-the-coca-cola-contour-bottle')
# Exact annotated information-design comparison with declared teaching data.
im,d=board('改稿不能只换颜色：同一组虚构客流数据',1800,1150)
vals=[120,150,210,180];labs=['周四','周五','周六','周日']
tx(d,70,140,'A 错误：截断纵轴放大差距',34,'#A53E35');tx(d,940,140,'B 修订：从零起画并直接标值',34,'#224C77')
for panel,x,ymin,scale in [(0,90,100,3.8),(1,950,0,2.2)]:
 base=850
 for j,(v,l) in enumerate(zip(vals,labs)):
  bx=x+60+j*170;bh=(v-ymin)*scale;d.rectangle((bx,base-bh,bx+100,base),fill='#D98138' if j==2 else '#7297B0');tx(d,bx+7,base-bh-48,str(v),30);tx(d,bx+3,880,l,30)
 d.line((x+20,base,x+740,base),fill='#303D43',width=4);tx(d,x+10,base+65,'纵轴起点 '+str(ymin),29)
tx(d,70,1020,'数据为教学虚构：120 / 150 / 210 / 180 人，不代表真实调查。',29)
save(im,'revision-root-data-rewrite.png','虚构客流条形图的轴线修订','本书原创教学数据')
f=R/'references/revision-root-images.json';s=json.loads(f.read_text());s=[a for a in s if a.get('kind')!='original_analysis'];s.extend(entries);f.write_text(json.dumps(s,ensure_ascii=False,indent=2));print('Rendered',len(entries),'root analysis plates')
# Packaging exercise, full realistic content in three related paper-bag panels.
im,d=board('一组咖啡包装：共用查找位置，用名称与图形双重区分',1800,1400)
for i,(name,profile,col,sign) in enumerate([('北坡','明亮果香','#9A4D2F','山线'),('暖谷','坚果可可','#354F77','谷线'),('夜航','深烘浓郁','#5B493D','星点')]):
 x=100+i*565;d.polygon([(x+40,200),(x+455,200),(x+490,1180),(x,1180)],fill='#E9D7B8',outline='#5E5146');d.line((x+55,250,x+440,250),fill='#6D594A',width=8)
 d.rectangle((x+35,365,x+455,1030),fill='#FFFDF8');tx(d,x+65,395,'山间烘焙 / FICTIONAL',23,col);tx(d,x+60,485,name,91,col);tx(d,x+65,625,profile,35)
 if i==0:d.line([(x+75,815),(x+185,700),(x+290,830),(x+365,755),(x+420,815)],fill=col,width=15)
 elif i==1:d.line([(x+75,735),(x+185,840),(x+290,740),(x+420,830)],fill=col,width=15)
 else:
  for a,b in [(130,750),(330,790),(230,850)]:d.ellipse((x+a-12,b-12,x+a+12,b+12),fill=col)
 tx(d,x+65,920,'全豆咖啡  /  200 g',29);tx(d,x+65,1090,'名称、风味、规格位置固定',22)
tx(d,100,1270,'本图是原创虚构包装练习，非真实商品；图形不是可生产的刀模。',29)
save(im,'revision-root-coffee-family.png','虚构咖啡包装的名称图形与字段结构','本书原创教学示例')
# Structured label flat map, not a manufacturable dieline.
im,d=board('展开以后，哪些内容必须在同一面？',1800,1080)
xs=[70,390,1010,1330,1730]
for i,(l,col) in enumerate([('侧面 A','#E9DFC9'),('正面','#FFFDF8'),('侧面 B','#E9DFC9'),('背面','#F0ECE2')]):
 d.rectangle((xs[i],185,xs[i+1],850),fill=col,outline='#7D796D',width=3);tx(d,xs[i]+25,215,l,32)
tx(d,425,340,'山间烘焙',47);tx(d,425,430,'北坡',95,'#9A4D2F');tx(d,425,605,'明亮果香',37);tx(d,425,720,'全豆咖啡 / 200 g',31)
for j,t in enumerate(['产品信息','冲煮建议','批次与日期','联系与储存']):tx(d,1360,340+j*105,t,33)
for j,t in enumerate(['折边区','避免主标题','跨过折线']):tx(d,90,390+j*80,t,28)
for j,t in enumerate(['次要图形','可延续','不靠细字']):tx(d,1040,390+j*80,t,27)
tx(d,70,930,'虚构标签内容关系图：不含缝份、热封参数与制造公差，不能直接生产。',29)
save(im,'revision-root-packaging-map.png','虚构咖啡包装正侧背面信息分工','本书原创教学示例')
# Write all records after late additions as well.
f=R/'references/revision-root-images.json';s=json.loads(f.read_text());s=[a for a in s if a.get('kind')!='original_analysis'];s.extend(entries);f.write_text(json.dumps(s,ensure_ascii=False,indent=2))
