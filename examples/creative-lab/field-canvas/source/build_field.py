"""FIELD NOTES V4: rebuild six editable native boards and their design system.
Artwork is an AI editorial photography study, never a botanical specimen.
Run only to recreate this initial V4; it overwrites later manual canvas edits.
"""
from pathlib import Path
import json,shutil,html
R=Path(__file__).resolve().parents[2];C=R/'field-canvas';D=R/'field-system';BOOK=R.parents[1]
for p in [C/'fonts',C/'uploads',D/'fonts',D/'components',D/'assets/Photography']:p.mkdir(parents=True,exist_ok=True)
for p in [C/'fonts',D/'fonts']:
 for a,b in [(BOOK/'assets/fonts/NotoSansSC-Regular.ttf','NotoSansSC-Regular.ttf'),(Path('/usr/share/fonts/opentype/urw-base35/NimbusRoman-Regular.otf'),'FieldSerif.otf'),(Path('/usr/share/fonts/opentype/urw-base35/NimbusRoman-Italic.otf'),'FieldSerif-Italic.otf')]:
  if a.resolve()!=(p/b).resolve():shutil.copy(a,p/b)
 for a,b in [(BOOK/'assets/fonts/OFL.txt','Noto-OFL.txt'),(BOOK/'assets/fonts/COPYRIGHT.txt','Noto-COPYRIGHT.txt'),(Path('/usr/share/doc/fonts-urw-base35/copyright'),'URW-COPYRIGHT.txt')]:
  if a.exists():shutil.copy(a,p/b)
asset=R/'shared-assets/field-botanical-v4.png'
if not asset.exists():raise SystemExit('Waiting for field-botanical-v4.png; no placeholder is substituted.')
shutil.copy(asset,C/'uploads/field-botanical-v4.png');shutil.copy(asset,D/'assets/Photography/iris-study-v4.png')
P='#F4EEDC';V='#482C45';G='#3E5947';B='#E4D2D2';M='#675A60';L='#B4AA97'
colors=[('paper',P,'All reading surfaces and editorial margins.'),('plum',V,'Headlines and body on paper and blush.'),('moss',G,'Running furniture on paper and blush.'),('blush',B,'Photography mattes; quiet secondary surface.'),('ink-secondary',M,'Captions and secondary reading on paper and blush.'),('rule',L,'Non-semantic hairlines only.'),('white','#FFFFFF','Reference swatch, not default paper.'),('on-plum',P,'Legible text on plum.')]
styles=[('masthead','42px',1.1,'Identity: Chinese anchor, no oversized default.'),('feature-title','60px',1.16,'Chinese feature title.'),('section-title','28px',1.3,'Section openings.'),('body','21px',1.8,'Long-form editorial copy.'),('caption','16px',1.5,'Image status, credits and running furniture.')]
tokens={'name':'野序 / FIELD NOTES · V4','version':4,'color':{'themes':[{'id':'paper','name':'Editorial ivory'}],'tokens':[{'name':n,'value':v,'usage':u}for n,v,u in colors]},'type':{'fonts':[{'family':'Field Sans','file':'fonts/NotoSansSC-Regular.ttf','weight':'100 900'},{'family':'Field Serif','file':'fonts/FieldSerif.otf','weight':'400'},{'family':'Field Serif','file':'fonts/FieldSerif-Italic.otf','weight':'400','style':'italic'}],'families':{'sans':'"Field Sans", sans-serif','serif':'"Field Serif", serif'},'groups':[{'name':'Chinese editorial','family':'sans','styles':[{'name':n,'fontSize':s,'lineHeight':h,'fontWeight':400,'usage':u}for n,s,h,u in styles]},{'name':'Latin editorial','family':'serif','styles':[{'name':'latin-display','fontSize':'176px','lineHeight':0.92,'fontWeight':400,'usage':'Optical crop and quiet English display.'},{'name':'latin-pullquote','fontSize':'42px','lineHeight':1.12,'fontWeight':400,'usage':'Short italic reading invitation.'}]}]},'spacing':{'tokens':[{'name':f'space-{n}','value':f'{n}px','usage':u}for n,u in [(8,'Micro-space'),(16,'Label separation'),(24,'Paragraph gap'),(40,'Column gutter'),(56,'Safe edge'),(80,'Major breathing space')]]},'radius':{'tokens':[{'name':'radius-none','value':'0px','usage':'All photographic frames.'},{'name':'radius-label','value':'2px','usage':'Small labels only.'},{'name':'radius-seal','value':'999px','usage':'Rare issue seal; not a recurring card shape.'}]},'sizing':{'tokens':[{'name':n,'value':v,'usage':u}for n,v,u in [('component-label','16px','Component small print'),('component-name','42px','Component bilingual name'),('component-english','46px','Component English name'),('component-date','52px','Calendar marker'),('component-display','84px','Cover preview headline'),('rule-width','1px','Hairline')]]}}
(D/'tokens.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2)+'\n')
di=json.loads((D/'design-system.json').read_text());di.update(title='野序 / FIELD NOTES · V4',namespace='FieldNotes');(D/'design-system.json').write_text(json.dumps(di,ensure_ascii=False,indent=2)+'\n')
(D/'components/bundle.css').write_text('.fn-root{font-family:var(--font-sans);color:var(--plum);background:var(--paper)}\n')
(D/'components/bundle.js').write_text('''/* @ds-bundle: {"format":4,"namespace":"FieldNotes","components":[{"name":"Masthead"},{"name":"EditorialCaption"},{"name":"EventBadge"},{"name":"Cover"}]} */
(function(){function e(tag,s,t){var n=document.createElement(tag);n.style.cssText=s;if(t)n.textContent=t;return n;}
window.FieldNotes={
Masthead:function(p){p=p||{};var n=e('div','display:flex;align-items:baseline;justify-content:space-between;gap:var(--space-40);padding:var(--space-24) var(--space-40);background:var(--paper);color:var(--plum);font-family:var(--font-sans)');n.appendChild(e('span','font-size:var(--component-name);line-height:1.1',p.name||'野序'));n.appendChild(e('span','font-family:var(--font-serif);font-size:var(--component-english);line-height:1',p.english||'Field notes.'));n.appendChild(e('span','font-size:var(--component-label);color:var(--moss)',p.issue||'No. 07 / SUMMER 2027'));return n;},
EditorialCaption:function(p){p=p||{};var n=e('div','display:flex;gap:var(--space-24);padding:var(--space-16) var(--space-40);border-top:var(--rule-width) solid var(--rule);background:var(--paper);color:var(--ink-secondary);font:var(--component-label)/1.5 var(--font-sans)');n.appendChild(e('span','font-family:var(--font-serif)',p.number||'Fig. 01'));n.appendChild(e('span','',p.text||'Iris study. AI-generated editorial image; not a botanical record.'));return n;},
EventBadge:function(p){p=p||{};var n=e('div','display:flex;align-items:baseline;gap:var(--space-24);padding:var(--space-24) var(--space-40);background:var(--blush);color:var(--plum);font-family:var(--font-sans)');n.appendChild(e('span','font-family:var(--font-serif);font-size:var(--component-date);line-height:1',p.date||'12—30 JUN'));n.appendChild(e('span','font-size:var(--component-label)',p.label||'Iris Studies / 野序纸上花展'));return n;},
Cover:function(){var n=e('div','padding:var(--space-24);background:var(--paper);color:var(--plum)');n.appendChild(FieldNotes.Masthead({}));n.appendChild(e('h2','font:italic var(--component-display)/1.05 var(--font-serif);margin:var(--space-40)','A closer look.'));n.appendChild(FieldNotes.EventBadge({}));n.appendChild(FieldNotes.EditorialCaption({}));return n;}
};})();''')
(D/'components/index.d.ts').write_text('''declare namespace FieldNotes {
function Masthead(props?: {name?:string;english?:string;issue?:string}):HTMLElement;
function EditorialCaption(props?: {number?:string;text?:string}):HTMLElement;
function EventBadge(props?: {date?:string;label?:string}):HTMLElement;
function Cover():HTMLElement;
}
''')
for n,sub,arg in [('Masthead','身份退到纸边，期号先于装饰。','{}'),('EditorialCaption','图像身份、局部和AI来源清楚独立。','{number:"Fig. 07",text:"花瓣近景。AI编辑摄影研究，不作为标本记录。"}'),('EventBadge','日期是信息锚点，不是按钮或圆角卡片。','{date:"12—30 JUN",label:"野序纸上花展 / 2027"}'),('Cover','真实调用三个编辑组件形成系统预览。','')]:
 d=D/'components'/n;d.mkdir(exist_ok=True);(d/'README.md').write_text(sub+'\n\n返回真实HTMLElement，使用语义token。不要随版面无限放大。\n');(d/'preview.html').write_text(f'<!-- @dsCard group="Editorial" height={500 if n=="Cover"else 180} subtitle="{sub}" -->\n<!doctype html><html lang="zh"><head><meta charset="utf-8"></head><body><div id="root"></div><script>document.getElementById("root").appendChild(FieldNotes.{n}({arg}));</script></body></html>')
(D/'assets/Photography/README.md').write_text('iris-study-v4.png是AI生成的单枝鸢尾编辑摄影风格研究图，不是真实摄影师拍摄、植物标本或科学记录。三种裁切分别承担封面气氛、跨页观看、展览招贴。\n')
# Source primitives: every visible property stays inline and every text stays literal.
def tx(tag,s,style=''):
 # The native canvas parser keeps entities in style text. Bare CSS family names
 # avoid quote entities while still selecting the exact local @font-face.
 style=style.replace('"Field Serif"','Field Serif, serif')
 return f'<{tag} style="margin:0;{html.escape(style,quote=True)}">{s}</{tag}>'
def box(content,x,y,w,h=None,extra=''):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'+(f'height:{h}px;'if h else'')+extra+'">'+content+'</div>'
def ph(x,y,w,h,pos='50% 50%',extra=''):
 return f'<img src="uploads/field-botanical-v4.png" alt="单枝深紫鸢尾，AI生成的编辑摄影研究图" style="position:absolute;display:block;left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:cover;object-position:{pos};{extra}" />'
def rule(x,y,w):return box('',x,y,w,1,f'background:{L};')
def furniture(l,r,w):
 return box(f'<div style="display:flex;justify-content:space-between;gap:40px;align-items:baseline;font-size:16px;letter-spacing:1.6px;color:{G};white-space:nowrap">{tx("span",l)}{tx("span",r)}</div>',56,40,w-112)
fonts='''@font-face{font-family:"Field Sans";src:url("fonts/NotoSansSC-Regular.ttf");font-weight:100 900}@font-face{font-family:"Field Serif";src:url("fonts/FieldSerif.otf");font-weight:400;font-style:normal}@font-face{font-family:"Field Serif";src:url("fonts/FieldSerif-Italic.otf");font-weight:400;font-style:italic}body{margin:0;font-family:"Field Sans",sans-serif}*{box-sizing:border-box}'''
def board(name,w,h,c,bg=P):
 (C/name).write_text(f'''<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>{name}</title><script src="./support.js"></script></head><body><x-dc><helmet><style>{fonts}</style></helmet><div style="position:relative;width:{w}px;height:{h}px;overflow:hidden;background:{bg};color:{V}">{c}</div></x-dc><script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>class Component extends DCLogic {{ renderVals(){{return {{}};}} }}</script></body></html>''')
# Cover: the flower is a tall right-hand presence; English display lives in the left margin.
c=ph(470,174,610,1160,'55% 45%')
c+=box(tx('h1','野序','font-size:70px;line-height:1;font-weight:400;letter-spacing:3px'),56,55,230)
c+=box(tx('p','No. 07','font-family:"Field Serif";font-size:60px;line-height:1')+tx('p','SUMMER 2027','font-size:14px;letter-spacing:2.4px;line-height:2.3'),800,49,224,100,'text-align:right;')
c+=rule(56,145,968)
c+=box(tx('p','Field','font-family:"Field Serif";font-size:200px;line-height:.94;letter-spacing:-8px'),42,294,560,205)
c+=box(tx('p','notes.','font-family:"Field Serif";font-style:italic;font-size:150px;line-height:.98;letter-spacing:-6px'),36,476,480,205)
c+=box(tx('p','THE IRIS ISSUE','font-size:15px;letter-spacing:3px;color:'+G),58,774,360)
c+=box(tx('h2','靠近一朵花，<br/>让时间慢下来。','font-size:31px;line-height:1.65;font-weight:400;letter-spacing:1px'),56,819,354)
c+=box(tx('p','On nature,<br/>and the art<br/>of looking.','font-family:"Field Serif";font-size:43px;line-height:1.08;font-style:italic'),56,1058,340)
c+=box(tx('p','植物、影像与纸本阅读<br/>A botanical art journal','font-size:16px;line-height:1.9;color:'+G),56,1238,350)
c+=box('<div style="display:flex;justify-content:space-between;gap:30px;white-space:nowrap;font-size:13px;color:'+M+'">'+tx('span','野序 / FIELD NOTES')+tx('span','AI EDITORIAL STUDY · 01')+'</div>',56,1382,968)
board('Main.dc.html',1080,1440,c)
# Spread: central photography crosses the gutter; independently readable outer text columns.
left1='看一朵花，可以先放下名字。先沿外缘看一圈：哪里张开，哪里垂下，哪里又被自己的阴影折回？当颜色退后，轮廓便显露出方向。我们不急着解释它，只让眼睛跟着转折走一次。'
left2='距离再近一点，花瓣不再是一片紫色。细小的纹理沿着表面延伸，深色褶皱与轻薄边缘互相衬托。摄影让这些关系暂时停住，纸页则允许我们在同一个位置反复停留。'
right1='这页没有试图给出关于鸢尾的全部知识。它选择一次靠近：保留花头与长叶的关系，同时让柔软的背景退后。图像负责感受，文字负责提出可以亲自验证的观看方法。'
right2='换到纸上，观看又增加了一个尺度。题名、图注与页码成为图像的邻居。让它们各有位置，画面便不必时时大声。空白不是等待被填满的地方，而是读者可以停一下的时间。'
c=furniture('FIELD ESSAY / 观察笔记','018—019 · NO. 07',1800)
c+=ph(460,146,772,920,'55% 45%')
c+=box(tx('h1','A closer<br/><em style="font-weight:400">look.</em>','font-family:"Field Serif";font-size:128px;line-height:.92;letter-spacing:-4px;font-weight:400'),56,103,570,270)
c+=box(tx('p','01 / THE OUTLINE','font-size:15px;letter-spacing:2px;color:'+G)+tx('p',left1,'font-size:21px;line-height:1.85;margin-top:22px'),56,428,332)
c+=box(tx('p','02 / THE SURFACE','font-size:15px;letter-spacing:2px;color:'+G)+tx('p',left2,'font-size:21px;line-height:1.85;margin-top:22px'),56,750,332)
c+=box(tx('h2','靠近，<br/>才看见。','font-size:62px;line-height:1.28;font-weight:400;letter-spacing:2px'),1296,148,448)
c+=box(tx('p','An iris, observed.','font-family:"Field Serif";font-size:35px;font-style:italic;line-height:1.1'),1296,348,448)
c+=box(tx('p','03 / THE EDIT','font-size:15px;letter-spacing:2px;color:'+G)+tx('p',right1,'font-size:21px;line-height:1.85;margin-top:22px'),1296,469,448)
c+=box(tx('p','04 / THE PAGE','font-size:15px;letter-spacing:2px;color:'+G)+tx('p',right2,'font-size:21px;line-height:1.85;margin-top:22px'),1296,780,448)
c+=box(tx('p','Fig. 01   单枝鸢尾的摄影风格研究。AI生成，非标本或科学记录。','font-size:14px;line-height:1.6;color:'+M),460,1084,772)
c+=rule(56,1134,1688)+box('<div style="display:flex;justify-content:space-between;white-space:nowrap;font-size:14px;color:'+G+'">'+tx('span','野序 / FIELD NOTES')+tx('span','THE ART OF LOOKING · 018 / 019')+'</div>',56,1151,1688)
board('Spread.dc.html',1800,1200,c)
# Poster: a narrow calendar/text spine beside almost full-height photography.
c=ph(340,0,740,1440,'54% 50%')
c+=box(tx('p','野序 / FIELD NOTES','font-size:15px;letter-spacing:1.8px'),36,43,270)
c+=box(tx('h1','花在<br/>纸上。','font-size:78px;line-height:1.23;font-weight:400;letter-spacing:3px'),36,149,280)
c+=box(tx('p','Iris<br/><em>Studies</em>','font-family:"Field Serif";font-size:76px;line-height:.95;letter-spacing:-2px'),36,425,286)
c+=box(tx('p','植物影像与纸本小展','font-size:20px;line-height:1.7'),36,640,270)
c+=rule(36,737,254)
c+=box(tx('p','12—30','font-family:"Field Serif";font-size:76px;line-height:1;letter-spacing:-3px')+tx('p','JUNE 2027','font-size:18px;letter-spacing:3px;line-height:2.4'),36,805,286)
c+=box(tx('p','11:00—19:00<br/>自由入场','font-size:22px;line-height:1.8'),36,1013,270)
c+=box(tx('p','野序纸上花房<br/>二层 · 阅读室','font-size:19px;line-height:1.8'),36,1188,270)
c+=box(tx('p','A quiet kind<br/>of wild.','font-family:"Field Serif";font-size:40px;font-style:italic;line-height:1.1'),790,1080,250)
c+=box(tx('p','AI IMAGE STUDY / 2027','font-size:11px;letter-spacing:1.5px;color:'+M),790,1359,250)
board('Exhibition.dc.html',1080,1440,c,B)
# Controlled bad cover: no random collisions, but every piece competes in volume.
c=box(tx('p','初稿 / 焦点过多，层级失效','font-size:18px;color:'+G),56,35,968)
c+=box(tx('h1','野序 07','font-size:150px;line-height:1.05;font-weight:400'),56,100,968,175)
c+=box(tx('p','FIELD NOTES','font-family:"Field Serif";font-size:126px;line-height:1.1;letter-spacing:-4px'),56,279,968,145)
c+=ph(56,451,968,574,'50% 31%')
c+=box(tx('h2','靠近一朵花，<br/>让时间慢下来。','font-size:67px;line-height:1.25;font-weight:400'),56,1059,968)
c+=box(tx('p','SUMMER 2027 / THE IRIS ISSUE','font-size:34px;letter-spacing:1.6px'),56,1259,968)
c+=box(tx('p','比较条件：文字都很清楚，却没有一个足够安静的入口。','font-size:20px;color:'+G),56,1361,968)
board('Before.dc.html',1080,1440,c)
# Editing study: unequal frames show a whole image, a portrait edit and a tactile detail.
c=furniture('FIELD NOTES / IMAGE EDIT','01 · 02 · 03',1800)
c+=box(tx('h1','One photograph,<br/><em>three ways of looking.</em>','font-family:"Field Serif";font-size:92px;line-height:.98;font-weight:400;letter-spacing:-2px'),56,105,1260,220)
c+=box(tx('p','同一张图，<br/>不是同一种任务。','font-size:31px;line-height:1.6'),1390,137,350)
c+=box(tx('p','同一AI生成图像的三种取景；非真实摄影记录','font-size:22px;line-height:1.5;color:'+G),56,321,1688)
c+=ph(56,373,340,455,'50% 50%')
c+=ph(470,373,512,455,'55% 38%')
# Large detail uses native image crop rather than baking a composite bitmap.
c+='<div style="position:absolute;left:1056px;top:373px;width:688px;height:455px;overflow:hidden"><img src="uploads/field-botanical-v4.png" alt="AI鸢尾摄影研究的花瓣局部" style="position:absolute;left:-165px;top:-195px;width:1020px;height:1360px;object-fit:cover" /></div>'
for x,w,num,title,body in [(56,340,'01','完整的姿态','保留花头、长叶与茎。用来建立对象，不急着追求视觉冲击。'),(470,512,'02','封面的取景','花头偏上，留出边缘与视线方向。为刊名留位置，而不是缩小全部元素。'),(1056,688,'03','一处可以停留的细节','放大褶皱、纹理与薄边，改变观看距离。局部必须说明身份，不能冒充另一件作品。')]:
 c+=box(tx('p',num+' / '+title,'font-size:24px;line-height:1.5')+tx('p',body,'font-size:20px;line-height:1.75;margin-top:15px;color:'+G),x,858,w)
board('CropStudies.dc.html',1800,1060,c)
# Rules: an editorial specimen, not a row of UI cards.
c=furniture('野序 / FIELD NOTES','V4 · EDITORIAL SYSTEM',1600)
c+=box(tx('h1','A field guide<br/><em>to restraint.</em>','font-family:"Field Serif";font-size:110px;line-height:.96;letter-spacing:-3px;font-weight:400'),56,125,980,235)
c+=box(tx('p','让花成为主角，<br/>让文字有自己的声音。','font-size:40px;line-height:1.5;font-weight:400'),56,423,600)
c+=ph(1130,118,414,760,'55% 45%')
c+=box(tx('p','野序','font-size:60px;line-height:1.1')+tx('p','Field notes.','font-family:"Field Serif";font-size:72px;font-style:italic;line-height:1.3'),730,423,355)
for i,(n,color,label) in enumerate([('PAPER',P,'#F4EEDC'),('PLUM',V,'#482C45'),('MOSS',G,'#3E5947'),('BLUSH',B,'#E4D2D2')]):
 x=56+i*262;c+=box('',x,675,214,60,f'background:{color};border:1px solid {L};');c+=box(tx('p',n,'font-size:14px;letter-spacing:2px')+tx('p',label,'font-family:"Field Serif";font-size:27px;line-height:1.7'),x,756,214)
c+=box(tx('p','01  不同媒介，不共用一张模板。<br/>02  每一页只设一个主要观看动作。<br/>03  细节图必须说明裁切与AI身份。','font-size:23px;line-height:1.9;color:'+G),56,905,800)
c+=box(tx('p','Typography<br/>Field Sans / Noto Sans SC<br/>Field Serif / Nimbus Roman<br/>Body 21 / 37.8 · Caption 16 / 24','font-size:18px;line-height:1.8;color:'+G),1130,919,414)
board('Rules.dc.html',1600,1120,c)
# Keep native creation identity and installed-system records.
ci=json.loads((C/'canvas.json').read_text());specs=[('Rules.dc.html',0,0,1600,1120,'01 · 编辑语法'),('Main.dc.html',1680,0,1080,1440,'02 · 封面'),('Spread.dc.html',2840,0,1800,1200,'03 · 跨页文章'),('Exhibition.dc.html',0,1560,1080,1440,'04 · 展览招贴'),('Before.dc.html',1160,1560,1080,1440,'05 · 受控反例'),('CropStudies.dc.html',2320,1560,1800,1060,'06 · 摄影取景')]
ci['boards']={n:{'x':x,'y':y,'w':w,'h':h,'title':t}for n,x,y,w,h,t in specs};ci['order']=['Main.dc.html']+[n for n,*_ in specs if n!='Main.dc.html'];ci['notes']={'field-title':{'kind':'title1','x':0,'y':-280,'text':'野序 / FIELD NOTES · A closer look','maxW':4400},'editorial-decision':{'x':1160,'y':3080,'w':1080,'fill':'pink','size':24,'text':'V4不是图片替换：中文身份退到纸边，英文衬线承担语气；封面为边缘取景、跨页为靠近观看、广告为日期与照片并置。Before以同等音量造成层级问题。V3归档不进入画布order。'}};(C/'canvas.json').write_text(json.dumps(ci,ensure_ascii=False,indent=2)+'\n')
readme='''# 野序 / FIELD NOTES · V4

原创虚构植物艺术杂志。No.07、2027夏刊、展览名称、日期、开放时间与场地都是示范文案，不是实际出版物或活动。植物图是AI生成的编辑摄影风格研究，不是真实摄影师作品、植物标本或科学记录。

## V4重构
V3以巨大的中文刊名和满版水粉块形成上下三段，三种媒介又共享相近框架。V4更换了观看方法：中文刊名缩到身份尺度；Nimbus Roman的细衬线、真实斜体和小号issue furniture建立编辑语气；照片从密集花丛改为单枝微距，留边与花头方向成为版式条件。

封面：左侧英文与小刊名，右侧窄幅长照片，专题文字成为可以停留的边注。
跨页：中部摄影跨越中缝，两侧各有独立文章栏，正文不跨装订缝，图注与页码清楚分开。
广告：左侧日期和垂直信息脊，右侧接近全高摄影；它不是封面的放大版。
Rules把字体、色彩和编辑限制做成完整语法页；CropStudies以不等宽画框说明完整姿态、封面取景与触觉细节；Before没有随机遮字，而是让刊名、期号、专题同样响亮，形成受控层级反例。

## 规则
paper承载长文，plum承载标题，moss用于小号家具，blush只是摄影的柔和衬底。线条不承担必要文字信息。每页只选择一个主要观看动作；正文必须有自己的平静区域。字体全部本地，Field Sans是Noto Sans SC；Field Serif是Nimbus Roman真实常规和斜体，不用浏览器合成斜体。

## 原生文件
六板仍为Main、Spread、Exhibition、Rules、Before、CropStudies，标题、图注与正文都是可编辑的字，照片单独存uploads/field-botanical-v4.png。source/build_field.py重建真正的V4，不是事后替换图片；运行会覆盖人工编辑。

field-system提供Masthead、EditorialCaption、EventBadge和Cover真实可调用组件、preview、token与本地字体。通过原生API安装后，ds/fieldnotes保存明确版本快照；改token需重新安装。source/install_field.py与verify_components.py负责实际安装、编译与浏览器组件检查。

## 归档
旧六张成品及旧源稿保留在renders/v3，旧构建源码在source/build_field_v3.py；它们不进入canvas.json的order。旧素材不改名不删除。

## 版权与身份
品牌、版式和文案为本书原创。AI资产来源日志位于shared-assets/generation-log-v4.json。Noto和URW字体许可在fonts内。本项目不借用真实杂志、Figma或Spotify的商标。
'''
(C/'README.md').write_text(readme)
(D/'README.md').write_text(readme.replace('## 原生文件','## 原生使用')+'\n## Tokens和组件\nversion=4；8个语义色，7个文字样式，6档间距、3半径及组件尺寸。Masthead把身份放低，EditorialCaption明确图像来源，EventBadge把日期变成信息锚点。三个组件都返回实际HTMLElement，Cover调用它们。tokens.css由原生编辑器生成，源脚本不手写。\n')
print('FIELD NOTES V4 rebuilt: six editorial boards, native identity preserved.')
