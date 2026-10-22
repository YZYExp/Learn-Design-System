#!/usr/bin/env python3
"""Generate the fully labelled, fictional chapter 22 teaching applications."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
R=Path(__file__).resolve().parents[1]; O=R/'examples'; O.mkdir(exist_ok=True)
F=R/'assets/fonts/NotoSansSC-Regular.ttf'
BG='#FFF9F0';INK='#222222';RED='#9B3027';TEAL='#28665E';RULE='#D9D5CA'
def ft(n):return ImageFont.truetype(str(F),n)
def tx(d,x,y,t,n=30,c=INK):d.text((x,y),t,font=ft(n),fill=c)
def line(d,a,b,c=RULE,w=2):d.line([a,b],fill=c,width=w)
def motif(d,box,color=TEAL,w=55):d.arc(box,10,300,fill=color,width=w)
def canvas(w,h):
 im=Image.new('RGB',(w,h),BG);return im,ImageDraw.Draw(im)
def foot(d,y,w):
 line(d,(55,y),(w-55,y));tx(d,55,y+18,'原创虚构教学样张 · 非真实活动 · 请勿用于报名或导航',19)
def save(im,name):im.save(O/name,optimize=True)
# Poster: actual hierarchy, no placeholder bars
im,d=canvas(1000,1414)
tx(d,70,65,'SHORELINE / DESIGN WEEK',25,TEAL)
tx(d,65,130,'岸线',142);tx(d,70,315,'设计周',93)
tx(d,75,470,'形与日常',45,TEAL)
motif(d,(330,550,890,1110),TEAL,95);d.ellipse((720,960,840,1080),fill=RED)
d.rectangle((65,1110,600,1290),fill=BG)
tx(d,75,1120,'11月6—8日',53,RED);tx(d,75,1200,'旧港仓库园区',35)
foot(d,1310,1000);save(im,'poster.png')
# Folded leaflet: two faces across an A4 layout
im,d=canvas(1600,1132)
line(d,(800,45),(800,1050),RULE,3)
tx(d,65,60,'节目一览',61);tx(d,65,145,'岸线设计周  /  形与日常',30,TEAL)
items=[('周五  11月6日','10:00—17:00','展览：材料的第二次生命','A 展厅','自由参观'),('周六  11月7日','10:00—11:30','讲座：看见一套视觉语法','B 讲堂','需预约'),('周六  11月7日','14:00—16:00','从一张旧纸开始：','C 工坊','再生纸与印刷工作坊 · 需预约')]
y=245
for day,time,title,zone,note in items:
 line(d,(65,y-18),(735,y-18));tx(d,65,y,day,31,RED);tx(d,65,y+50,time,25,TEAL);tx(d,65,y+92,title,32);tx(d,65,y+145,zone,27);tx(d,65,y+188,note,25);y+=260
tx(d,865,60,'来到园区之后',55)
tx(d,865,150,'以字母与名称核对目的地',29,TEAL)
for i,(zone,title,desc) in enumerate([('A','展厅','材料展览 · 自由参观'),('B','讲堂','两场讲座 · 按场次预约'),('C','工坊','三场手作 · 按场次预约')]):
 yy=255+i*185;d.rectangle((865,yy,940,yy+80),fill=TEAL);tx(d,880,yy+5,zone,48,BG);tx(d,970,yy+2,title,39);tx(d,970,yy+65,desc,25)
for j,t in enumerate(['先在入口查看当天开放信息。','到场后按区域编号确认位置。','需要预约的节目，请核对确认结果。','具体余位与时间以正式通知为准。']):tx(d,865,860+j*43,t,25)
foot(d,1050,1600);save(im,'leaflet.png')
# Sign: a mock sign, not a real installation size
im,d=canvas(1400,800)
tx(d,65,50,'岸线设计周',39)
d.rectangle((55,160,1345,605),fill=TEAL)
tx(d,95,215,'C',180,BG);tx(d,315,240,'工坊',127,BG)
line(d,(910,385),(1240,385),BG,30)
d.polygon([(1240,385),(1125,300),(1125,470)],fill=BG)
tx(d,95,510,'手作活动  /  按场次预约',36,BG)
foot(d,690,1400);save(im,'sign.png')
# Paper bag artwork: only essential identity
im,d=canvas(1000,1100)
tx(d,75,70,'岸线设计周',74);tx(d,78,185,'形与日常',35,TEAL)
motif(d,(150,300,830,980),TEAL,110);d.ellipse((650,800,780,930),fill=RED)
foot(d,1010,1000);save(im,'bag-artwork.png')
# Phone: readable first step, explicit mock-up
im,d=canvas(760,1500)
d.rectangle((0,0,760,115),fill=TEAL);tx(d,45,30,'岸线设计周  /  预约',33,BG)
tx(d,45,165,'再生纸与印刷工作坊',45)
tx(d,45,250,'从一张旧纸开始',31,TEAL)
for yy,t in [(340,'11月7日（周六） 14:00—16:00'),(400,'C 工坊 · 旧港仓库园区'),(460,'本样张展示预约前的阅读与输入。')]:tx(d,45,yy,t,29)
line(d,(45,540),(715,540))
for yy,label,value in [(590,'姓名','请填写参加者姓名'),(780,'联系邮箱','用于接收预约结果')]:
 tx(d,45,yy,label,31);d.rectangle((45,yy+60,715,yy+140),outline=TEAL,width=3);tx(d,70,yy+80,value,27,'#5B635E')
tx(d,45,1010,'提交后请核对预约结果与参加信息。',29)
d.rounded_rectangle((45,1110,715,1220),radius=12,fill=RED);tx(d,260,1135,'确认预约',43,BG)
tx(d,45,1280,'纸面流程示意，无实际提交功能。',27,TEAL)
foot(d,1390,760);save(im,'phone.png')
# Book comparison plates: all full content, reduced but no fictional claims.
for names,name in [(['poster.png','sign.png','bag-artwork.png'],'example-22-identity.png'),(['leaflet.png','phone.png'],'example-22-information.png')]:
 out=Image.new('RGB',(1800,1250),BG);q=ImageDraw.Draw(out);tx(q,60,35,'岸线设计周 · 完整内容样张（原创虚构）',44)
 boxes=[(60,145,510,1100),(620,145,1110,1100),(1200,145,1740,1100)] if len(names)==3 else [(40,160,1240,1110),(1290,145,1760,1120)]
 for n,b in zip(names,boxes):
  src=Image.open(O/n).convert('RGB');src.thumbnail((b[2]-b[0],b[3]-b[1]));out.paste(src,(b[0],b[1]+(b[3]-b[1]-src.height)//2))
 out.save(R/'assets/images'/name,optimize=True)
(O/'tokens.json').write_text(json.dumps({'light':{'surface':BG,'text':INK,'action':RED,'onAction':'#FFFFFF'},'auxiliary':TEAL,'motif':'open arc + offset dot','grid':'four-column relationship; reflow by medium'},ensure_ascii=False,indent=2))
print('Generated five fully labelled teaching applications and two book plates.')
