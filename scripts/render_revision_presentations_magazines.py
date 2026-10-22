#!/usr/bin/env python3
"""Original teaching slides and editorial layouts, plus labelled source-analysis plates.
Actual artworks are retained separately; this script does not regenerate them.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'assets/images';F=R/'assets/fonts/NotoSansSC-Regular.ttf'
C={'bg':'#FAF7EF','ink':'#142B45','blue':'#2F74AA','orange':'#D66430','light':'#DBE5EC','gray':'#607283','green':'#234B38','yellow':'#F2BD3B'}
W,H=1920,1080
fonts={}
def f(s):
 if s not in fonts:fonts[s]=ImageFont.truetype(str(F),s)
 return fonts[s]
def text(d,p,s,size=42,col=None):d.text(p,s,font=f(size),fill=col or C['ink'])
def ct(d,x,y,s,size=42,col=None):
 bb=d.textbbox((0,0),s,font=f(size));text(d,(x-(bb[2]-bb[0])/2,y),s,size,col)
def canvas(title,kicker='原创教学示例 · 所有客流数字均为虚构'):
 im=Image.new('RGB',(W,H),C['bg']);d=ImageDraw.Draw(im);text(d,(90,50),kicker,26,C['gray']);text(d,(90,110),title,54);d.line((90,208,1830,208),fill=C['light'],width=3);return im,d
def save(im,n):
 target=O/n;tmp=O/('.tmp-'+n);im.save(tmp,optimize=True);tmp.replace(target)
def bars(d,x,y,w,n=4,col=None):
 for j in range(n):d.rectangle((x,y+j*28,x+w*(.75 if j==n-1 else 1),y+j*28+6),fill=col or C['gray'])
def box(d,b,col=None):d.rounded_rectangle(b,20,fill=col or '#FFFFFF',outline=C['light'],width=2)
def arrow(d,a,b,col=None):
 c=col or C['orange'];d.line((a,b),fill=c,width=6);q=math.atan2(b[1]-a[1],b[0]-a[0]);s=18;d.polygon([b,(b[0]-s*math.cos(q-.5),b[1]-s*math.sin(q-.5)),(b[0]-s*math.cos(q+.5),b[1]-s*math.sin(q+.5))],fill=c)
def chart(d,b,mode='final'):
 x0,y0,x1,y1=b;vals=[20,80,130,180,95,70,45,30];labs=['09','10','11','12','13','14','15','16'];hi=200
 for v in [0,60,120,180]:
  y=y1-(y1-y0)*v/hi;d.line((x0,y,x1,y),fill=C['light'],width=2);text(d,(x0-65,y-18),str(v),28,C['gray'])
 bw=(x1-x0)/8
 for i,(v,l) in enumerate(zip(vals,labs)):
  x=x0+i*bw+15;y=y1-(y1-y0)*v/hi;co=C['orange'] if v>120 else C['blue'];d.rectangle((x,y,x+bw-30,y1),fill=co);ct(d,x+bw/2-15,y-52,str(v),35,co);ct(d,x+bw/2-15,y1+20,l+'时',28)
 y=y1-(y1-y0)*120/hi
 for x in range(int(x0),int(x1),30):d.line((x,y,min(x+17,x1),y),fill=C['orange'],width=4)
 text(d,(x1-355,y-58),'处理容量 120 人/小时',30,C['orange']);text(d,(x0-50,y0-65),'到馆人数 / 人',29,C['gray'])
# The same content, made useful through three changes.
im,d=canvas('初稿：把讲义缩进一页，观众无从判断')
text(d,(110,270),'博物馆运营汇报',54);text(d,(110,365),'一、背景与情况',34)
lines=['周末有家庭观众、临时访客、团体与预约观众。','本次观察时段为 09—16 时，全天人数合计 650 人。','09时20人，10时80人，11时130人，12时180人。','13时95人，14时70人，15时45人，16时30人。','现行处理能力为每小时120人，需关注高峰与排队。','从人员、信息、流程、动线等方面综合考虑优化。']
for i,s in enumerate(lines):text(d,(110,435+i*65),'• '+s,32)
d.pieslice((1280,320,1760,800),0,90,fill=C['orange']);d.pieslice((1280,320,1760,800),90,260,fill=C['blue']);d.pieslice((1280,320,1760,800),260,360,fill=C['light']);text(d,(1280,865),'未说明扇区含义的装饰饼图',28,C['gray'])
text(d,(110,950),'问题：标题只报主题；数字被埋；图表不回答决策问题。',33,C['orange']);save(im,'revision-presentations-edit-0.png')
im,d=canvas('第一步：让标题说出判断')
text(d,(110,285),'12时客流高于现行处理容量 50%',64);text(d,(110,390),'要回答：是否在 11—13 时增加一个临时入口岗位？',42,C['orange'])
for i,s in enumerate(['全天合计 650 人，不等于每小时都拥挤。','峰值 180 人/小时；容量 120 人/小时。','先呈现时段分布，再讨论人员安排。']):text(d,(130,540+i*115),f'{i+1}  '+s,43)
text(d,(110,955),'删除不能支撑本页判断的信息；保留数据口径。',32,C['gray']);save(im,'revision-presentations-edit-1.png')
im,d=canvas('第二步：把证据变成可比较的图')
text(d,(110,275),'12时客流高于现行处理容量 50%',59);chart(d,(210,470,1725,865))
text(d,(110,990),'虚构数据；容量是练习设定，非真实博物馆研究结论。',26,C['gray']);save(im,'revision-presentations-edit-2.png')
im,d=canvas('12时高峰超过现行处理容量 50%')
chart(d,(170,390,1340,865));box(d,(1450,300,1820,900),C['ink']);text(d,(1490,365),'建议试验',37,'#FFFFFF');text(d,(1490,450),'11—13 时',46,'#FFFFFF');text(d,(1490,520),'增设 1 岗',46,'#FFFFFF');text(d,(1490,660),'先运行两周',34,'#FFFFFF');text(d,(1490,725),'再评估等候',34,'#FFFFFF');text(d,(1490,790),'与岗位成本',34,'#FFFFFF')
text(d,(110,980),'第三步：让证据与行动相邻。这里是试验提案，不是已证实的改善效果。',30,C['gray']);save(im,'revision-presentations-edit-3.png')
# Eight-slide narrative. Fixed margin and type scale, deliberately different evidence layouts.
for idx in range(1,9):
 titles=['建议只在周末高峰增加一个入口岗位','全天人数不多，负荷却集中在中午','11—12时超过现行每小时处理容量','12时新增60人处理能力，才与峰值相当','岗位可以临时调配，但不能挤占安全职责','两周试验同时记录等候与岗位成本','达不到条件就回退，不把试验当成定论','今天需要批准一个小范围、可撤回的试验']
 im,d=canvas(titles[idx-1],f'博物馆入口优化 / 教学小报告 {idx:02d} / 虚构数据与情境')
 if idx==1:
  text(d,(110,310),'一个时间窗',68);text(d,(110,425),'11—13 时',105,C['orange']);text(d,(110,660),'一个岗位 / 两周试验 / 事后评估',48);box(d,(1190,300,1790,900),C['ink']);text(d,(1250,390),'先试验',80,'#FFFFFF');text(d,(1250,535),'再决定是否长期运行',40,'#FFFFFF')
 elif idx in [2,3]:
  chart(d,(210,390,1730,860));text(d,(120,970),'全天 650 人；处理容量 120 人/小时。比较必须使用相同时间单位。',32,C['gray'])
 elif idx==4:
  for i,(n,l,col) in enumerate([(120,'现行容量',C['blue']),(60,'峰值缺口',C['orange'])]):
   x=210+i*830;box(d,(x,320,x+650,810));ct(d,x+325,385,str(n),135,col);ct(d,x+325,570,l,49);ct(d,x+325,655,'人 / 小时',35,C['gray'])
  text(d,(120,925),'180 − 120 = 60；实际增岗能力尚需试验，不能预设一岗恰好补足。',34,C['gray'])
 elif idx==5:
  for i,(t,s) in enumerate([('可考虑','咨询引导 / 预约核验'),('不挪用','安保 / 消防 / 必要休息'),('需记录','培训 / 交接 / 异常处理')]):
   yy=325+i*195;d.rectangle((140,yy,430,yy+125),fill=[C['blue'],C['orange'],C['ink']][i]);text(d,(175,yy+30),t,45,'#FFFFFF');text(d,(500,yy+30),s,47)
 elif idx==6:
  for i,(t,s) in enumerate([('等候','同一时间窗 / 逐日记录'),('成本','实际工时 / 额外培训'),('体验','投诉 / 误入 / 信息清晰度')]):
   x=120+i*595;box(d,(x,325,x+550,860));ct(d,x+275,400,t,76,[C['blue'],C['orange'],C['ink']][i]);text(d,(x+45,600),s.split(' / ')[0],41);text(d,(x+45,685),s.split(' / ')[1],41)
 elif idx==7:
  for i,(t,s) in enumerate([('继续','等候改善且无关键岗位缺口'),('调整','改善有限，检查流程与能力'),('回退','安全受损或成本超出边界')]):
   yy=320+i*195;d.ellipse((135,yy,250,yy+115),fill=[C['blue'],C['gray'],C['orange']][i]);text(d,(290,yy+10),t,52);text(d,(600,yy+20),s,44)
 elif idx==8:
  text(d,(120,310),'批准：两周周末高峰试验',72,C['orange']);text(d,(120,470),'范围：一个入口，一个增岗时间窗',47);text(d,(120,590),'责任：现场主管；保留停止试验权限',47);text(d,(120,710),'回访：两周后提交等候、成本与异常记录',47);text(d,(120,885),'讨论重点：岗位从哪里来？出现什么情况必须停止？',39,C['blue'])
 save(im,f'revision-presentations-report-{idx:02d}.png')
# contact sheet for all actual rendered pages
sheet=Image.new('RGB',(1920,2160),C['bg']);sd=ImageDraw.Draw(sheet)
for i in range(8):
 q=Image.open(O/f'revision-presentations-report-{i+1:02d}.png');q.thumbnail((920,518));x=20+(i%2)*960;y=15+(i//2)*540;sheet.paste(q,(x,y))
save(sheet,'revision-presentations-report-sequence.png')
# actual source-analysis plates, preserving original image alongside numbered visual observations
def annotation(src,out,title,labels,rects):
 im,d=canvas(title,'真实原作 + 本书结构标注 / 原作版权按图注归属')
 q=Image.open(O/src).convert('RGB');q.thumbnail((1120,745));x=80;y=250;im.paste(q,(x,y))
 for i,b in enumerate(rects):
  b=(x+b[0]*q.width,y+b[1]*q.height,x+b[2]*q.width,y+b[3]*q.height);d.rectangle(b,outline=C['orange'],width=5);d.ellipse((b[0]-15,b[1]-15,b[0]+35,b[1]+35),fill=C['orange']);text(d,(b[0]-2,b[1]-12),str(i+1),31,'#FFFFFF')
 for i,s in enumerate(labels):
  yy=280+i*200;text(d,(1260,yy),str(i+1),50,C['orange'])
  for j,l in enumerate(s.split('|')):text(d,(1330,yy+8+j*55),l,31)
 save(im,out)
annotation('revision-presentations-nasa-page-11.png','revision-presentations-nasa-analysis.png','NASA原页：轨迹图承担“过程与位置”的说明',['轨迹与箭头|先建立空间关系','编号与图例|再定位具体事件','小字号密集区|远处投影需拆页'],[(.02,.02,.84,.55),(.02,.68,.75,.96),(.75,.70,.99,.98)])
annotation('revision-magazines-ver-sacrum-1898.jpg','revision-magazines-ver-sacrum-analysis.png','《Ver Sacrum》：刊名、插图与文字共同占据平面',['刊名形成顶部横向带|字形与整体语气相联','树与容器形成图像区|不是贴在正文旁的装饰','右侧文字分段排列|图文分工建立秩序'],[(.04,.07,.93,.24),(.04,.24,.59,.95),(.59,.24,.94,.92)])
annotation('revision-magazines-life-1936-cover.jpg','revision-magazines-life-cover-analysis.png','LIFE创刊封面：少量识别元素与一张强图',['固定刊名位置|先认出这是哪本刊物','建筑尺度与人物比例|摄影自身提供视觉张力','附属出版信息|退到次要阅读层'],[(.03,.087,.46,.24),(.02,.25,.98,.90),(.01,.89,.99,.99)])
annotation('revision-magazines-life-1936-spread.jpg','revision-magazines-life-page9-analysis.png','LIFE第9页：大照片进入正文叙事',['照片先给生活场景|不是重复封面的建筑','标题把场景转成议题|文字补上理解方向','双栏正文与页码|为连续阅读建立节奏'],[(.03,.23,.93,.71),(.03,.72,.94,.78),(.08,.79,.90,.92)])
# Original editorial demonstration: dawn market, drawn scenery rather than fake photography.
def market(im,b,detail=False):
 d=ImageDraw.Draw(im);x0,y0,x1,y1=b;w=x1-x0;h=y1-y0
 d.rectangle(b,fill='#D9E4DF');d.rectangle((x0,y0+h*.62,x1,y1),fill='#D9CCB2')
 # bridge behind market
 d.rectangle((x0,y0+h*.25,x1,y0+h*.34),fill='#7C8E85')
 for k in range(5):
  xx=x0+k*w/4;d.line((xx,y0+h*.13,xx,y0+h*.27),fill=C['green'],width=max(3,int(w/240)))
 for k in range(3):
  xx=x0+w*(.06+k*.31);yy=y0+h*.43;sw=w*.25
  d.rectangle((xx,yy,xx+sw,yy+h*.28),fill='#F4EBD8',outline=C['green'],width=3)
  d.polygon([(xx-w*.02,yy),(xx+sw/2,yy-h*.13),(xx+sw+w*.02,yy)],fill=[C['orange'],C['green'],C['blue']][k])
  for j in range(5):
   cx=xx+sw*(.12+j*.17);cy=yy+h*.2;rr=max(5,w*.015);d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=C['yellow'])
 # shoppers, varied positions / bags
 for k in range(6):
  cx=x0+w*(.10+k*.15);cy=y0+h*(.65+.09*(k%2));rr=w*.016
  d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill='#9A7052');d.rectangle((cx-rr,cy+rr,cx+rr,cy+rr*4),fill=[C['green'],C['blue'],C['orange']][k%3]);d.line((cx-rr*.5,cy+rr*4,cx-rr,cy+rr*6),fill=C['ink'],width=4);d.line((cx+rr*.5,cy+rr*4,cx+rr,cy+rr*6),fill=C['ink'],width=4)
def mag_base(title):
 im,d=canvas(title,'原创编辑设计练习 / “桥边”社区杂志 / 程序插图与虚构采访');return im,d
# cover bad and final side-by-side
im,d=mag_base('封面改稿：先选一个入口，再安排辅助信息')
for x in [110,1020]:box(d,(x,250,x+790,990))
market(im,(145,300,865,930));d=ImageDraw.Draw(im);text(d,(170,320),'桥边',100,C['green']);
for i,(s,c) in enumerate([('最全！早市指南',C['orange']),('鲜果 / 小吃 / 人情',C['ink']),('走进城市的一天',C['green']),('人物故事大集合',C['orange']),('路线·好物·访谈',C['blue'])]):text(d,(170,450+i*87),s,43,c)
text(d,(110,995),'初稿：五个主标题抢同一个位置',30,C['orange'])
market(im,(1055,400,1775,930));d=ImageDraw.Draw(im);text(d,(1085,290),'桥边',100,C['green']);text(d,(1085,430),'城市醒来之前',55,C['green']);d.rectangle((1070,800,1760,880),fill=C['bg']);text(d,(1085,815),'早市里的第一小时',42,C['green']);text(d,(1085,905),'第 03 期  /  人物·路线·小吃',28,C['green']);text(d,(1020,995),'改稿：刊名 + 一个主故事 + 次级目录',30,C['green']);save(im,'revision-magazines-cover-edit.png')
# spread bad
def spread_frame(title):
 im,d=mag_base(title);d.rectangle((100,250,1820,985),fill='#FFFFFF',outline=C['light'],width=2);d.line((960,250,960,985),fill=C['light'],width=3);return im,d
im,d=spread_frame('跨页初稿：图片一样大，文字填满剩余空隙')
for i in range(4):
 x=140+(i%2)*855;y=320+(i//2)*305;market(im,(x,y,x+390,y+220));d=ImageDraw.Draw(im);bars(d,x+420,y+10,355,7)
text(d,(140,920),'没有进入点，也看不出哪一组图片属于同一个故事。',35,C['orange']);save(im,'revision-magazines-spread-edit-0.png')
# revised opening
im,d=spread_frame('跨页第一步：用一张环境图建立现场')
market(im,(120,275,940,960));d=ImageDraw.Draw(im);text(d,(1000,320),'城市醒来之前',68,C['green']);text(d,(1000,440),'早市里的第一小时',46,C['orange']);text(d,(1000,550),'桥边的摊位先于街道忙起来。',37);text(d,(1000,615),'这一组故事跟随三位摊主，',37);text(d,(1000,680),'观察准备、交易与收摊。',37);bars(d,1000,800,700,4)
text(d,(140,925),'01  环境：地点与空间关系',28,C['green']);text(d,(1000,930),'摄影式题材；此处实际为原创程序插图。',26,C['gray']);save(im,'revision-magazines-spread-edit-1.png')
# revised feature details
im,d=spread_frame('跨页第二步：让远景、人物与细节各做一件事')
text(d,(140,285),'同一条街，三种观看距离',60,C['green']);market(im,(140,410,900,750));d=ImageDraw.Draw(im)
# portrait drawn detail
for x,l in [(1010,'02 人物：谁在做事'),(1410,'03 细节：怎样做事')]:
 d.rectangle((x,410,x+350,750),fill='#E6D8BE');text(d,(x,770),l,28,C['green'])
d.ellipse((1115,445,1265,595),fill='#9A7052');d.rectangle((1100,595,1280,750),fill=C['green']);d.rectangle((1435,600,1725,700),fill=C['orange'])
for j in range(5):d.ellipse((1455+j*48,555,1505+j*48,605),fill=C['yellow'])
text(d,(140,775),'01 环境：摊位怎样连接街道',29,C['green']);bars(d,140,845,740,3);bars(d,1010,845,735,3);save(im,'revision-magazines-spread-edit-2.png')
# revision third step caption hierarchy and no invented documentary truth
im,d=spread_frame('跨页第三步：图注补充事实，别只重复画面')
market(im,(140,310,1080,930));d=ImageDraw.Draw(im);text(d,(1140,320),'图注应该回答',51,C['green'])
for i,s in enumerate(['谁：人物身份与署名','何时：拍摄或观察时间','何地：具体地点与方位','为何：读者看不出的背景']):text(d,(1140,440+i*105),s,34)
text(d,(1140,885),'真实报道必须核实；',29,C['orange']);text(d,(1140,930),'练习不可伪装成实地采访。',29,C['orange']);save(im,'revision-magazines-spread-edit-3.png')
# editorial/ad separation
im,d=spread_frame('广告插页：允许风格跳转，身份边界要清楚')
text(d,(140,300),'早市人物',62,C['green']);market(im,(140,420,890,820));d=ImageDraw.Draw(im);bars(d,140,870,720,3)
d.rectangle((990,275,1795,960),fill=C['yellow']);text(d,(1030,310),'广告 / 虚构品牌教学样例',28,C['ink']);text(d,(1045,430),'一袋好好吃的早晨',61,C['green']);d.rounded_rectangle((1220,570,1600,835),radius=25,fill=C['green']);d.arc((1290,510,1530,670),180,360,fill=C['green'],width=22);text(d,(1280,660),'桥边面包',43,'#FFFFFF');text(d,(1050,875),'广告不冒充编辑推荐，价格与条件另列。',31,C['ink']);save(im,'revision-magazines-ad-boundary.png')
# sequencing strip / varied density, actually developed page thumbnails
im,d=mag_base('一册八页：让观看强度有起伏')
for i in range(8):
 x=95+(i%4)*440;y=285+(i//4)*355;d.rectangle((x,y,x+390,y+285),fill='#FFFFFF',outline=C['light'],width=2)
 if i==0:market(im,(x+12,y+55,x+378,y+272));d=ImageDraw.Draw(im);text(d,(x+22,y+10),'桥边',34,C['green'])
 elif i==1:text(d,(x+25,y+20),'本期目录',33,C['green']);bars(d,x+25,y+90,330,6)
 elif i in [2,3]:market(im,(x+12,y+12,x+378,y+200));d=ImageDraw.Draw(im);text(d,(x+25,y+215),'开场 / 现场',30,C['green'])
 elif i in [4,5]:market(im,(x+15,y+30,x+195,y+190));d=ImageDraw.Draw(im);bars(d,x+215,y+35,145,6);bars(d,x+15,y+220,345,2)
 elif i==6:d.rectangle((x+10,y+10,x+380,y+275),fill=C['yellow']);text(d,(x+35,y+35),'广告',28);text(d,(x+35,y+110),'一袋好好吃的早晨',29,C['green'])
 else:d.rectangle((x+10,y+10,x+380,y+275),fill=C['green']);text(d,(x+35,y+80),'下次见，桥边。',35,'#FFFFFF')
 text(d,(x,y+290),f'{i+1:02d} '+['封面','目录','开场左页','开场右页','人物左页','细节右页','广告','封底'][i],28,C['gray'])
text(d,(100,1000),'缩略图检查：图片尺寸、文字密度与故事任务变化；不是每页换一种字体。',30,C['green']);save(im,'revision-magazines-eight-pages.png')
# small QA contact sheet
names=[p for p in O.glob('revision-presentations-*.png') if 'report-' not in p.name]+list(O.glob('revision-magazines-*.png'))
sheet=Image.new('RGB',(1920,math.ceil(len(names)/3)*420),C['bg']);sd=ImageDraw.Draw(sheet)
for i,p in enumerate(sorted(names)):
 q=Image.open(p).convert('RGB');q.thumbnail((600,350));x=20+i%3*640;y=15+i//3*420;sheet.paste(q,(x,y));text(sd,(x,y+355),p.stem.replace('revision-','')[:31],21,C['gray'])
(R/'build').mkdir(exist_ok=True);sheet.save(R/'build/revision-presentations-magazines-contact.jpg')
print('Original layout examples and source-analysis plates generated.')
