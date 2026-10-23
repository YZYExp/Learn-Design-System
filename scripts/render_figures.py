#!/usr/bin/env python3
"""Rebuild original, deterministic teaching figures. No historical works reproduced."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, random, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'; OUT.mkdir(parents=True,exist_ok=True)
FONT=ROOT/'assets/fonts/NotoSansSC-Regular.ttf'
if not FONT.exists(): FONT=ROOT/'assets/fonts/NotoSansSC-VF.ttf'
BG='#F6F2E9'; INK='#202621'; RED='#B94432'; GREEN='#28665E'; GRAY='#7A8179'; PALE='#D9DDD4'; PAPER='#FFFDFA'
W,H=1800,1100
FONTS={}
def font(n):
 if n not in FONTS:FONTS[n]=ImageFont.truetype(str(FONT),n)
 return FONTS[n]
def new(num,title,sub):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 d.rectangle((70,60,84,124),fill=RED);d.text((110,56),title,font=font(48),fill=INK)
 d.text((110,135),sub,font=font(28),fill=GRAY)
 d.line((70,1018,1730,1018),fill=PALE,width=2)
 d.text((75,1037),'设计的语法 · 原创教学示意 / 非历史作品复刻',font=font(25),fill=GRAY)
 return im,d
def txt(d,xy,s,size=30,color=INK):d.text(xy,s,font=font(size),fill=color)
def center(d,xy,s,size=30,color=INK):
 b=d.textbbox((0,0),s,font=font(size));txt(d,(xy[0]-(b[2]-b[0])/2,xy[1]),s,size,color)
def panel(d,box,label=None):
 d.rounded_rectangle(box,radius=18,fill=PAPER,outline=PALE,width=2)
 if label:txt(d,(box[0]+25,box[1]+20),label,32)
def line(d,pts,fill=INK,width=5):d.line(pts,fill=fill,width=width,joint='curve')
def arrow(d,a,b,color=GREEN,width=6):
 line(d,[a,b],color,width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);s=18
 d.polygon([b,(b[0]-s*math.cos(ang-.5),b[1]-s*math.sin(ang-.5)),(b[0]-s*math.cos(ang+.5),b[1]-s*math.sin(ang+.5))],fill=color)
def motif(d,x,y,s=140,color=GREEN):
 d.arc((x,y,x+s,y+s),0,300,fill=color,width=max(6,int(s*.16)))
 d.ellipse((x+s*.63,y+s*.63,x+s*.89,y+s*.89),fill=RED)
def leaf(d,x,y,s=55,color=GREEN,mirror=False):
 pts=[(x,y+s*.55),(x+s*.35,y),(x+s,y-s*.1),(x+s*.8,y+s*.6),(x+s*.35,y+s*.8)]
 if mirror:pts=[(2*x+s-px,py) for px,py in pts]
 d.polygon(pts,fill=color)
def grid(d,box,cols=4,rows=5):
 x0,y0,x1,y1=box
 for j in range(cols+1):x=x0+(x1-x0)*j/cols;line(d,[(x,y0),(x,y1)],PALE,2)
 for j in range(rows+1):y=y0+(y1-y0)*j/rows;line(d,[(x0,y),(x1,y)],PALE,2)
def bars(d,x,y,w,n=4,color=GRAY,gap=22):
 for i in range(n):d.rectangle((x,y+i*gap,x+w*(1 if i<n-1 else .65),y+i*gap+5),fill=color)
def save(im,n):
 dest=OUT/f'fig-{n:02}.png';tmp=OUT/f'.fig-{n:02}.tmp.png';im.save(tmp,optimize=True);tmp.replace(dest)

# 01: same vocabulary, three outputs
im,d=new(1,'从一件作品，到一组有关系的作品','不变的是母题与关系；画幅、信息与阅读距离允许变化。')
for box,l in [((100,220,590,925),'海报'),((655,220,1145,925),'票券'),((1210,220,1700,925),'杯套')]:panel(d,box,l)
d.rectangle((180,310,510,835),fill=BG);motif(d,220,440,240);txt(d,(210,335),'岸线',56);bars(d,215,750,230,2)
d.rectangle((700,425,1100,665),fill=BG);motif(d,735,460,140);txt(d,(905,475),'岸线',44);bars(d,905,570,140,2)
d.polygon([(1270,400),(1640,400),(1600,760),(1310,760)],fill=BG,outline=INK);motif(d,1345,470,210);line(d,[(1290,430),(1620,430)],GREEN,5)
center(d,(900,950),'圆弧 + 圆点 + 对齐关系，在三种载体上保持可辨认',30,GREEN);save(im,1)
# 02
im,d=new(2,'点、线、面如何组织注意力','三组使用相同类型的元素，改变关系便改变阅读。')
for i,l in enumerate(['对齐：形成共同边界','疏密：把相关内容靠近','层级：先看哪里？']):
 x=90+i*570;panel(d,(x,230,x+530,930),l)
 if i==0:
  for k in range(4):d.ellipse((x+60,365+k*100,x+94,399+k*100),fill=RED);line(d,[(x+130,382+k*100),(x+430,382+k*100)],INK,9)
  line(d,[(x+130,330),(x+130,800)],GREEN,3)
 elif i==1:
  for y in [370,430,490,690,750]:d.ellipse((x+65,y,x+100,y+35),fill=RED);line(d,[(x+135,y+18),(x+440,y+18)],INK,8)
  txt(d,(x+60,835),'近 = 同组；远 = 分段',28,GREEN)
 else:
  d.rectangle((x+60,355,x+380,470),fill=RED);d.ellipse((x+380,620,x+450,690),fill=GREEN);bars(d,x+60,550,300,5)
  txt(d,(x+60,835),'大小、对比共同产生重点',28,GREEN)
save(im,2)
# 03
im,d=new(3,'颜色从来不是孤立存在','上排中心色块 RGB 完全相同；下排只改变色彩面积。')
for x,bg in [(120,'#15382F'),(660,'#D3D8AD'),(1200,'#603D47')]:
 d.rectangle((x,245,x+480,605),fill=bg);d.rectangle((x+160,345,x+320,505),fill='#B94432')
 center(d,(x+240,625),'中心色：#B94432',29)
for i,ratio in enumerate([.1,.3,.6]):
 x=120+i*540;d.rectangle((x,735,x+480,885),fill=GREEN);d.rectangle((x,735,x+480*ratio,885),fill=RED);center(d,(x+240,905),f'朱红面积 {int(ratio*100)}%',30)
save(im,3)
# 04
im,d=new(4,'网格把信息关系变得可重复','同一组内容：先决定层级与分组，再决定栏与间距。')
for x,l in [(150,'自由摆放，关系不稳定'),(980,'四栏骨架，关系可追踪')]:panel(d,(x,225,x+670,945),l)
# left
for x,y,w in [(220,365,400),(300,455,390),(240,560,320),(420,680,260)]:bars(d,x,y,w,2)
d.ellipse((260,730,420,890),fill=GREEN);txt(d,(400,320),'岸线',54);txt(d,(600,840),'设计周',33,RED)
# right
grid(d,(1040,325,1590,870),4,6);txt(d,(1040,337),'岸线设计周',52);d.rectangle((1040,465,1590,680),fill=GREEN);motif(d,1230,485,180,PALE);bars(d,1040,735,230,4);bars(d,1335,735,230,4)
save(im,4)
# 05
im,d=new(5,'装饰不是堆满：重复也有语法','同一叶片，在平移、镜像、隔行错位中产生不同节奏。')
for i,l in enumerate(['平移重复','镜像成对','隔行错位']):
 x=90+i*570;panel(d,(x,230,x+530,930),l)
 for r in range(4):
  for c in range(4):
   xx=x+55+c*110+(50 if i==2 and r%2 else 0)
   if xx+70<x+510:leaf(d,xx,380+r*120,70, GREEN if r%2==0 else RED, i==1 and c%2==1)
 line(d,[(x+30,825),(x+500,825)],PALE,2);txt(d,(x+35,850),'母题不变，变换规则不同',28,GRAY)
save(im,5)
# 06
im,d=new(6,'从构成练习，到模块思维','圆、方、三角是练习材料；它们本身不等于某个历史流派。')
for x,l in [(130,'平面：张力、平衡与重心'),(980,'模块：重复、接口与组合')]:panel(d,(x,230,x+690,925),l)
d.ellipse((220,420,500,700),fill=RED);d.rectangle((540,340,700,500),fill=GREEN);d.polygon([(520,790),(730,580),(750,810)],fill=INK)
for r in range(3):
 for c in range(3):
  x=1055+c*170;y=355+r*170;d.rectangle((x,y,x+145,y+145),outline=INK,width=4)
  if (r+c)%3==0:d.ellipse((x+30,y+30,x+115,y+115),fill=RED)
  elif (r+c)%3==1:d.polygon([(x+73,y+25),(x+120,y+120),(x+25,y+120)],fill=GREEN)
  else:d.rectangle((x+35,y+35,x+110,y+110),fill=INK)
save(im,6)
# 07
im,d=new(7,'系列海报：同一骨架，容纳不同内容','六栏关系保持；标题长度、图片位置和强调色可以变化。')
for i in range(3):
 x=110+i*560;panel(d,(x,230,x+500,940));grid(d,(x+40,280,x+460,875),6,7)
 txt(d,(x+40,295),['岸线','潮汐研究','设计的距离'][i],42)
 if i==0:d.ellipse((x+110,430,x+390,710),fill=RED)
 elif i==1:
  for j in range(4):line(d,[(x+60,450+j*70),(x+420,450+j*70)],GREEN,24)
 else:d.polygon([(x+70,450),(x+420,450),(x+420,730)],fill=INK)
 bars(d,x+40,790,190,3);bars(d,x+275,790,180,3)
 center(d,(x+250,950),f'方案 {i+1}',28,GREEN)
save(im,7)
# 08
im,d=new(8,'打破规则，也要保留可读的支点','破格需要能被察觉的秩序；随机不自动产生表达。')
for x,l in [(130,'有意越界：保留信息锚点'),(980,'无约束混乱：锚点同时丢失')]:panel(d,(x,230,x+690,940),l)
grid(d,(190,330,760,860),4,6);txt(d,(190,345),'岸线设计周',49);bars(d,190,760,220,4);d.polygon([(390,400),(800,660),(710,800),(300,540)],fill=RED);txt(d,(475,530),'突破',55,PAPER)
rng=random.Random(80)
for j in range(22):
 x=rng.randint(1030,1510);y=rng.randint(340,800);w=rng.randint(35,180);h=rng.randint(25,110);d.rectangle((x,y,x+w,y+h),fill=rng.choice([RED,GREEN,INK,PALE]))
for j,(x,y) in enumerate([(1050,380),(1370,550),(1110,740)]):txt(d,(x,y),['设计','岸线','周'][j],rng.randint(32,65),PAPER)
save(im,8)
# 09
im,d=new(9,'中文阅读方向，与留白的重心','同一句“岸线设计周”：横排与竖排需要不同的关系安排。')
for x,l in [(130,'横排：从左到右形成入口'),(980,'竖排：从上到下形成路径')]:panel(d,(x,230,x+690,940),l)
txt(d,(200,360),'岸线设计周',68);bars(d,200,510,490,5);d.ellipse((560,710,730,880),fill=RED)
for j,c in enumerate('岸线设计周'):txt(d,(1480,330+j*95),c,64)
for col in range(5):
 x=1360-col*75
 for r in range(7):d.rectangle((x,365+r*50,x+12,390+r*50),fill=GRAY)
d.ellipse((1050,740,1190,880),fill=RED)
center(d,(490,880),'横向行长与段落间距',28,GREEN);center(d,(1320,880),'列序、字距与空白',28,GREEN);save(im,9)
#10
im,d=new(10,'材料改变了可用的设计语言','同一弧叶母题：精细线条、像素阶梯、厚实轮廓各有条件。')
for i,l in enumerate(['纸印：保留细线','织造：8 × 8 单元','陶瓷：加粗、留缝']):
 x=90+i*570;panel(d,(x,230,x+530,940),l)
 if i==0:
  leaf(d,x+130,480,280,GREEN);line(d,[(x+165,660),(x+370,470)],BG,8)
  for j in range(5):line(d,[(x+200+j*30,620-j*28),(x+195+j*26,500-j*7)],BG,4)
 elif i==1:
  for r in range(8):
   for c in range(8):
    xx=x+65+c*50;yy=355+r*50;fill=GREEN if abs((7-r)-c)<3 and 1<=c<=6 else BG
    d.rectangle((xx,yy,xx+47,yy+47),fill=fill,outline=PALE,width=1)
 else:
  pts=[(x+130,630),(x+225,460),(x+410,430),(x+355,630),(x+230,710),(x+130,630)]
  line(d,pts,GREEN,28);line(d,[(x+150,675),(x+355,480)],GREEN,23)
  txt(d,(x+55,825),'缩小后，缝隙仍应看得见',28,GREEN)
save(im,10)
#11
im,d=new(11,'品牌家族：固定锚点，可变表达','固定位置与标志，承载不同图形和内容。')
for i in range(3):
 x=110+i*560;panel(d,(x,230,x+500,940));d.rectangle((x+35,270,x+110,345),fill=INK);motif(d,x+45,280,55,PAPER);txt(d,(x+140,282),'岸线',42)
 if i==0:
  for j in range(4):d.ellipse((x+75+j*25,460+j*25,x+360-j*25,745-j*25),outline=GREEN,width=13)
 elif i==1:
  for j in range(4):d.rectangle((x+70,450+j*75,x+430,480+j*75),fill=RED)
 else:d.polygon([(x+70,450),(x+430,450),(x+70,760)],fill=GREEN);d.ellipse((x+280,650,x+440,810),fill=RED)
 bars(d,x+40,850,280,2)
save(im,11)
#12
im,d=new(12,'书刊跨页：连续规则与阅读节奏','标题、图像、正文分层；跨页一致不等于两页完全相同。')
d.rectangle((110,235,1690,940),fill=PAPER,outline=INK,width=3);line(d,[(900,235),(900,940)],GRAY,3)
for x in [170,960]:grid(d,(x,300,x+660,870),3,7)
txt(d,(170,315),'看见一条岸线',58);txt(d,(170,400),'标题 28 pt / 正文 11 pt',29,GREEN)
d.rectangle((170,480,830,735),fill=GREEN);motif(d,380,495,220,PALE);bars(d,170,785,300,4);bars(d,530,785,300,4)
for x in [960,1190,1420]:bars(d,x,340,200,11)
d.rectangle((960,665,1620,860),fill=RED);txt(d,(990,730),'图像区',44,PAPER)
txt(d,(170,950),'同一基线与边距；栏沟、段间距分别承担不同关系。',30)
save(im,12)
#13
im,d=new(13,'图形既能计数，也能帮助找路','数量用等大单位重复；导视把颜色、形状与文字组合。')
panel(d,(100,230,900,940),'等大单位，才便于比较')
for r,n in enumerate([3,5,7]):
 txt(d,(140,360+r*150),['甲区','乙区','丙区'][r],32)
 for c in range(n):
  x=265+c*75;y=350+r*150;d.ellipse((x,y,x+30,y+30),fill=GREEN);d.rounded_rectangle((x-5,y+35,x+35,y+90),radius=10,fill=GREEN)
 txt(d,(800,370+r*150),str(n),36,RED)
panel(d,(960,230,1700,940),'冗余编码：不同线索互相补充')
d.rectangle((1010,360,1645,475),fill=GREEN);txt(d,(1040,385),'●  A 展区  →',38,PAPER)
d.rectangle((1010,520,1645,635),fill=RED);txt(d,(1040,545),'▲  B 展区  →',38,PAPER)
d.rectangle((1010,680,1645,795),fill=INK);txt(d,(1040,705),'■  C 展区  →',38,PAPER)
center(d,(1330,840),'转为灰阶，文字与形状仍保留',28,GREEN);save(im,13)
#14
im,d=new(14,'模块化产品：接口先于组合','同一孔距与连接关系，让不同布局共享零件。')
for i in range(3):
 x=100+i*555;panel(d,(x,230,x+510,800),['低柜','高架','长架'][i])
 rows=[2,3,1][i];cols=[2,1,3][i];cw=120 if i==2 else 155;ch=115
 bx=x+70;by=370
 for r in range(rows):
  for c in range(cols):
   xx=bx+c*cw;yy=by+r*ch;d.rectangle((xx,yy,xx+cw,yy+ch),outline=INK,width=6)
   for px in [xx+12,xx+cw-12]:
    for py in [yy+12,yy+ch-12]:d.ellipse((px-5,py-5,px+5,py+5),fill=RED)
 txt(d,(x+35,720),'连接孔与板厚保持一致',28,GREEN)
line(d,[(160,870),(800,870)],GREEN,8)
for x in [210,340,470,600,730]:d.ellipse((x-9,861,x+9,879),fill=RED)
txt(d,(160,910),'统一孔距',29,GREEN)
line(d,[(1050,870),(1650,870)],GRAY,8)
for x in [1100,1230,1360,1520]:d.ellipse((x-9,861,x+9,879),fill=RED)
line(d,[(1480,835),(1550,905)],RED,6);line(d,[(1550,835),(1480,905)],RED,6);txt(d,(1050,910),'孔距改变，旧接口无法接合',29,RED);save(im,14)
#15
im,d=new(15,'展厅中的秩序：先走得通，再看得清','平面只表达关系，不是建筑施工或消防设计。')
d.rectangle((150,250,1650,930),fill=PAPER,outline=INK,width=10)
for box in [(350,360,620,610),(850,350,1150,580),(1280,500,1510,750)]:d.rectangle(box,fill=PALE,outline=GRAY,width=3)
txt(d,(420,440),'展区 A',38);txt(d,(915,430),'展区 B',38);txt(d,(1320,590),'展区 C',34)
d.rectangle((720,720,1110,860),fill='#E8D9C6');txt(d,(800,765),'休息区',36)
d.rectangle((150,700,165,840),fill=BG);d.rectangle((1635,800,1650,910),fill=BG)
txt(d,(180,745),'入口',34,GREEN);txt(d,(1520,835),'出口',34,RED)
pts=[(260,790),(285,670),(700,670),(700,290),(1205,290),(1205,805),(1550,805)]
for a,b in zip(pts,pts[1:]):arrow(d,a,b,GREEN,8)
center(d,(900,955),'展品之间留出观看与通行空间；分岔前设置方向信息。',30)
save(im,15)
#16
im,d=new(16,'动效是一套时间关系','同样的总时长与终点，可以有不同的速度分配。')
for row,label,xs in [(0,'匀速：每段位移相同',[230,650,1070,1490]),(1,'缓出：开始快，接近终点时慢',[230,990,1350,1490])]:
 y=390+row*350;txt(d,(130,y-105),label,36);line(d,[(230,y),(1490,y)],PALE,4)
 for i,x in enumerate(xs):
  d.ellipse((x-36,y-36,x+36,y+36),fill=RED if i==0 else GREEN);center(d,(x,y+65),f'{i*100} ms',30)
 for a,b in zip(xs,xs[1:]):arrow(d,(a+50,y),(b-50,y),GRAY,3)
center(d,(900,950),'先定义目的与节奏，再讨论动画曲线；避免仅为装饰而持续运动。',30)
save(im,16)
#17
im,d=new(17,'生成设计：只改变一个参数','同一随机种子、同一 6 × 6 网格，逐步放大旋转扰动。')
for i,amp in enumerate([0,3,12]):
 x=90+i*570;panel(d,(x,230,x+530,940),f'角度范围：±{amp}°')
 rng=random.Random(17)
 for r in range(6):
  for c in range(6):
   cx=x+85+c*72;cy=385+r*72;a=math.radians(rng.uniform(-1,1)*amp);s=27
   pts=[(cx+u*math.cos(a)-v*math.sin(a),cy+u*math.sin(a)+v*math.cos(a)) for u,v in [(-s,-s),(s,-s),(s,s),(-s,s)]]
   d.polygon(pts,outline=INK,width=3)
 txt(d,(x+35,865),'seed = 17；其他条件固定',28,GREEN)
save(im,17)
#18
im,d=new(18,'数字设计系统，包含哪些层？','外观提供词汇，组件提供行为，模式解决任务，维护保障延续。')
for i,(t,sub) in enumerate([('视觉样式','色彩 / 字体 / 间距'),('组件','按钮 / 输入 / 反馈'),('任务模式','预约 / 支付 / 查询'),('维护反馈','贡献 / 版本 / 测试')]):
 x=90+i*430;panel(d,(x,250,x+390,920),t);center(d,(x+195,835),sub,27,GREEN)
 if i==0:
  for j,c in enumerate([INK,RED,GREEN]):d.rectangle((x+50+j*95,390,x+120+j*95,470),fill=c)
  txt(d,(x+55,530),'文字层级',40);bars(d,x+55,620,270,4)
 elif i==1:
  d.rounded_rectangle((x+50,385,x+340,475),radius=14,fill=GREEN);center(d,(x+195,405),'确认预约',36,PAPER)
  d.rectangle((x+50,535,x+340,635),outline=GRAY,width=3);txt(d,(x+75,560),'姓名',32,GRAY)
 elif i==2:
  for j,l in enumerate(['选择日期','填写信息','核对与提交']):
   yy=380+j*130;d.ellipse((x+35,yy,x+85,yy+50),fill=GREEN);center(d,(x+60,yy+5),str(j+1),28,PAPER);txt(d,(x+105,yy+8),l,30)
 else:
  for j,l in enumerate(['v1.0 → v1.1','问题记录','回归验证']):txt(d,(x+45,395+j*120),l,34,INK);line(d,[(x+45,450+j*120),(x+340,450+j*120)],PALE,3)
save(im,18)
#19
im,d=new(19,'语义色彩：角色稳定，颜色随情境改变','浅色与深色主题分别检查对比，而不是直接反相。')
for i,(bg,fg,accent,on,l) in enumerate([('#FFF9F0','#222222','#9B3027','#FFFFFF','浅色模式'),('#202423','#FFF9F0','#F5A396','#202423','深色模式')]):
 x=130+i*850;d.rounded_rectangle((x,240,x+690,940),radius=25,fill=bg,outline=GRAY,width=2);txt(d,(x+40,285),l,42,fg)
 for j,(name,col) in enumerate([('背景',bg),('正文',fg),('强调',accent),('强调上的字',on)]):
  y=400+j*105;d.rectangle((x+45,y,x+155,y+70),fill=col,outline=GRAY,width=2);txt(d,(x+185,y+13),name,34,fg)
 d.rounded_rectangle((x+405,555,x+635,655),radius=14,fill=accent);center(d,(x+520,580),'预约',36,on)
save(im,19)
#20
im,d=new(20,'组件的设计，必须包含状态','同一个预约动作：让用户知道能否操作、正在发生什么、结果如何。')
for i,(l,c) in enumerate([('常态',GREEN),('焦点',GREEN),('提交中',GRAY),('成功',GREEN),('失败',RED)]):
 x=85+i*345;panel(d,(x,235,x+315,545),l)
 if i==1:d.rounded_rectangle((x+17,350,x+298,475),radius=20,outline=RED,width=5)
 d.rounded_rectangle((x+30,365,x+285,460),radius=14,fill=c);center(d,(x+157,390),['确认预约','确认预约','提交中…','预约成功','重试预约'][i],30,PAPER)
panel(d,(160,610,930,950),'宽屏：标签与输入并排')
txt(d,(200,745),'预约日期',34);d.rectangle((420,730,850,815),outline=GRAY,width=3);txt(d,(450,750),'10 月 21 日',32)
panel(d,(1080,610,1630,950),'窄屏：标签移到上方')
txt(d,(1130,725),'预约日期',34);d.rectangle((1130,795,1580,880),outline=GRAY,width=3);txt(d,(1160,815),'10 月 21 日',32)
save(im,20)
#21
im,d=new(21,'规则如何继续生长？','每次变化都应有责任人、依据和可追踪的发布。')
positions=[(900,325),(1430,510),(1220,810),(580,810),(370,510)]
labels=[('提案','提出问题 / owner'),('试验','原型 / 使用情境'),('验证','可读性 / 可访问性'),('发布','v1.0 → v1.1'),('回访','反馈 / 后续修订')]
for i,(a,b) in enumerate(zip(positions,positions[1:]+positions[:1])):
 vx,vy=b[0]-a[0],b[1]-a[1];ln=math.hypot(vx,vy);arrow(d,(a[0]+vx/ln*125,a[1]+vy/ln*95),(b[0]-vx/ln*125,b[1]-vy/ln*95),GREEN,7)
for (x,y),(a,b) in zip(positions,labels):
 d.rounded_rectangle((x-165,y-75,x+165,y+75),radius=22,fill=PAPER,outline=PALE,width=3);center(d,(x,y-47),a,38);center(d,(x,y+10),b,26,GREEN)
center(d,(900,560),'可修改的规则',42,RED);center(d,(900,620),'比一次性的统一更长久',29,GRAY);save(im,21)
#22
im,d=new(22,'岸线设计周：跨媒介的一套语法','固定弧形母题、朱红青绿、信息层级；各载体按任务调整。')
# five media arranged two levels
for x,y,w,h,l in [(100,250,430,630,'海报'),(600,250,510,250,'导视'),(600,580,510,300,'册页'),(1200,250,490,320,'包装'),(1300,640,280,330,'手机')]:
 d.rounded_rectangle((x,y,x+w,y+h),radius=14,fill=PAPER,outline=PALE,width=3);txt(d,(x+20,y+15),l,28,GREEN)
# poster
grid(d,(140,330,490,820),4,5);txt(d,(140,340),'岸线',54);txt(d,(140,410),'设计周',42);motif(d,175,520,260);bars(d,140,825,220,2)
# sign
d.rectangle((630,335,1080,450),fill=GREEN);txt(d,(655,360),'展区 A   →',42,PAPER)
# booklet
line(d,[(855,635),(855,850)],PALE,3);motif(d,635,640,145);bars(d,875,650,190,7);txt(d,(635,810),'岸线',30)
# bag
motif(d,1320,330,200);line(d,[(1330,290),(1340,235),(1540,235),(1550,290)],INK,6)
# phone
d.rectangle((1320,700,1560,910),fill=BG);motif(d,1385,720,100);d.rounded_rectangle((1340,850,1540,895),radius=9,fill=GREEN);center(d,(1440,855),'预约',26,PAPER)
save(im,22)

#23
im,d=new(23,'连续图像：统一视点，才能比较','原创取景线稿，不是摄影作品；前三幅固定相机高度、主体尺度与灰底。')
for i,l in enumerate(['植物 A','植物 B','器物 C','反例：俯视 + 放大']):
 x=75+i*435;panel(d,(x,250,x+405,940),l);d.rectangle((x+25,360,x+380,800),fill='#D9D9D5')
 line(d,[(x+40,675),(x+365,675)],'#B1B5AE',3)
 if i<2:
  d.polygon([(x+135,665),(x+260,665),(x+240,760),(x+155,760)],fill=GREEN);line(d,[(x+198,665),(x+198,480)],INK,7)
  if i==0:
   leaf(d,x+190,520,75,GREEN);leaf(d,x+120,575,75,GREEN,True);leaf(d,x+195,610,60,GREEN)
  else:
   for j in range(5):
    a=j*2*math.pi/5;cx=x+200+math.cos(a)*65;cy=535+math.sin(a)*65;d.ellipse((cx-30,cy-30,cx+30,cy+30),fill=GREEN)
   d.ellipse((x+175,510,x+225,560),fill=RED)
 elif i==2:
  d.rectangle((x+135,560,x+255,760),fill=GREEN);d.arc((x+210,580,x+310,710),-90,90,fill=INK,width=12)
 else:
  d.ellipse((x+70,420,x+335,685),fill=GREEN);d.ellipse((x+90,440,x+315,665),fill=BG);d.ellipse((x+115,465,x+290,640),fill=RED)
 txt(d,(x+30,845),'视点与尺度' if i==3 else '同高 / 同光 / 同尺度',27,RED if i==3 else GREEN)
center(d,(900,965),'先约定画幅、裁切与光向，再允许主体变化。',30,GREEN);save(im,23)
#24
im,d=new(24,'可穿戴的系列：母题与结构一起设计','原创服装轮廓示意，不是裁剪图；弧形与配色保持，版型随用途变化。')
for x,l in [(100,'衬衣：接缝避开主母题'),(665,'裙：轮廓改变图形比例'),(1230,'包：边缘与承重结构')]:panel(d,(x,240,x+470,940),l)
# shirt
shirt=[(235,360),(175,395),(130,570),(215,600),(245,500),(240,820),(435,820),(430,500),(460,600),(535,570),(490,395),(430,360),(385,400),(280,400)]
d.polygon(shirt,fill=BG,outline=INK);line(d,[(335,410),(335,815)],GRAY,3);motif(d,267,510,130)
for yy in range(450,780,65):d.ellipse((329,yy,341,yy+12),fill=INK)
# skirt
d.polygon([(800,385),(1000,385),(1080,820),(720,820)],fill=BG,outline=INK);line(d,[(800,425),(1000,425)],GRAY,4);motif(d,790,515,205)
for xx in [800,900,1000]:line(d,[(900+(xx-900)*.65,430),(xx,800)],PALE,3)
# bag
line(d,[(1340,470),(1340,355),(1570,355),(1570,470)],INK,16);d.rounded_rectangle((1285,450,1625,825),radius=16,fill=BG,outline=INK,width=4);motif(d,1340,515,225);line(d,[(1305,475),(1305,800)],GRAY,3);line(d,[(1605,475),(1605,800)],GRAY,3)
center(d,(900,965),'母题可以跨媒介，缝线、受力、人体活动却不能忽略。',30,GREEN);save(im,24)

# A QA contact sheet; not a book asset.
thumbs=[]
for p in sorted(OUT.glob('fig-*.png')):
 q=Image.open(p);q.thumbnail((540,330));thumbs.append((p.name,q.copy()))
sheet=Image.new('RGB',(1800,math.ceil(len(thumbs)/3)*390),PAPER);sd=ImageDraw.Draw(sheet)
for i,(n,q) in enumerate(thumbs):
 x=(i%3)*600+20;y=(i//3)*390+15;sheet.paste(q,(x,y));sd.text((x,y+335),n,font=font(27),fill=INK)
(ROOT/'build').mkdir(exist_ok=True);sheet.save(ROOT/'build/figures-contact.png')
(OUT/'figures-manifest.json').write_text(json.dumps({'kind':'original-programmatic-teaching-diagrams','count':24,'script':'scripts/render_figures.py','palette':[BG,INK,RED,GREEN],'font':'Noto Sans SC','historical_reproductions':False},ensure_ascii=False,indent=2))
print('Rendered',len(thumbs),'figures to',OUT)
