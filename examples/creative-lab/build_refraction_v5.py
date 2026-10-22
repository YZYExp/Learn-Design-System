"""Rebuild Refraction V5: imagegen direction first, editable typography second.
Run refresh_refraction_tokens.py after this to invoke the native token compiler.
"""
from pathlib import Path
import json,html,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;C=R/'refraction-canvas';S=R/'refraction-system'
PAPER='#F2EDDF';INK='#151D20';BLUE='#173D78';GOLD='#D3A25C';MUTED='#525957';PALE='#D6E1E8'
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def js(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for dest in [C/'uploads/refraction-light-v5.png',S/'assets/Photography/refraction-light-v5.png']:shutil.copy2(R/'shared-assets/refraction-light-v5.png',dest)
for f in (S/'fonts').iterdir():
 if f.is_file():
  (C/'fonts').mkdir(exist_ok=True);shutil.copy2(f,C/'fonts'/f.name)
T=json.loads((S/'tokens.json').read_text());T['version']=5
T['color']={'themes':[{'id':'light','name':'纸白 / Light study'},{'id':'dark','name':'暗室 / Darkroom'}],'tokens':[
{'name':n,'value':v,'usage':u} for n,v,u in [
('surface',{'light':PAPER,'dark':'#151D20'},'信息基底；光场图像独立承载复杂渐变。'),('ink',{'light':INK,'dark':PAPER},'主要阅读文字。'),('accent',BLUE,'深蓝用于重点文字或实底。'),('on-accent',PAPER,'深蓝上的反白文字。'),('muted',{'light':MUTED,'dark':'#BBC4C4'},'辅助文字，必须放在稳定底色上。'),('hairline',{'light':'#7D837C','dark':'#858F92'},'细分隔线。'),('light-field',PALE,'光场的浅色辅助面，不用来替代真实图像。'),('amber',GOLD,'少量装饰与图像呼应，不作纸白上的小字。'),('paper-white','#FFFDF6','局部信息承托。')]]}
T['type']['fonts']=[{'family':'Refraction Sans','file':'fonts/NotoSansSC-Regular.ttf','weight':'400'},{'family':'Noto Serif CJK SC','file':'fonts/RefractionSong.otf','weight':'500'},{'family':'Nimbus Roman','file':'fonts/RefractionLatin.otf','weight':'400'},{'family':'Nimbus Roman','file':'fonts/RefractionLatin-Italic.otf','weight':'400','style':'italic'}]
T['type']['families']={'sans':'"Refraction Sans",sans-serif','serif':'Noto Serif CJK SC,serif','latin':'Nimbus Roman,serif'}
T['type']['groups']=[{'name':'光场展览层级','family':'serif','styles':[{'name':n,'fontSize':s,'lineHeight':h,'fontWeight':500,'letterSpacing':ls,'usage':u} for n,s,h,ls,u in [('display','200px',1,'0px','海报主标题；按媒介重排，不把所有文字都做大。'),('title','96px',1.2,'2px','中文主识别。'),('subtitle','42px',1.4,'3px','展览主题。'),('body','26px',1.7,'0px','提案正文；不叠到复杂光场。'),('meta','22px',1.5,'1px','日期与地点。'),('caption','17px',1.5,'0px','辅助说明。')]]}]
js(S/'tokens.json',T);js(C/'ds/refraction/tokens.json',T)
for p in [S/'design-system.json',C/'ds/refraction/design-system.json']:
 if p.exists():d=json.loads(p.read_text());d['title']='折光 / REFRACTION · V5';d.get('assetGroups',{}).get('Photography',{}).update({'title':'折射光场 / AI图像'});js(p,d)
idx=json.loads((C/'canvas.json').read_text());idx['title']='折光 / REFRACTION · 纸白光场'
idx['boards']['Revision.dc.html']['title']='V4 → V5方向修订'
for a in idx.get('designSystems',[]):a.update(version=5,copiedAt=datetime.now(timezone.utc).isoformat())
js(C/'canvas.json',idx)
FACE='''@font-face{font-family:"Noto Serif CJK SC";src:url("fonts/RefractionSong.otf");font-weight:500;font-style:normal} @font-face{font-family:"Nimbus Roman";src:url("fonts/RefractionLatin.otf");font-weight:400;font-style:normal} @font-face{font-family:"Nimbus Roman";src:url("fonts/RefractionLatin-Italic.otf");font-weight:400;font-style:italic} @font-face{font-family:"Refraction Sans";src:url("fonts/NotoSansSC-Regular.ttf");font-weight:400;font-style:normal} body{margin:0;font-family:Refraction Sans,sans-serif;color:#151D20}'''
def txt(x,y,w,s,size=28,color=INK,family='Refraction Sans',spacing=0,lh=1.5,extra=''):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-family:{family};font-size:{size}px;font-weight:{500 if family=="Noto Serif CJK SC" else 400};line-height:{lh};letter-spacing:{spacing}px;color:{color};white-space:pre-line;{extra}">{html.escape(s)}</div>'
def rect(x,y,w,h,c):return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};"></div>'
def image(x,y,w,h,pos='50% 50%',src='refraction-light-v5.png',fit='cover'):
 return f'<img src="uploads/{src}" alt="折射光场，AI生成；非真实物理实验" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:{fit};object-position:{pos};display:block;">'
def group(x,y,k,w,h,b):return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:scale({k});transform-origin:0 0;overflow:hidden;background:{PAPER};">{b}</div>'
def board(name,w,h,title,body):
 write(C/(name+'.dc.html'),f'''<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>{title}</title><script src="./support.js"></script></head><body><x-dc><helmet><style>{FACE}</style></helmet><div style="position:relative;width:{w}px;height:{h}px;overflow:hidden;box-sizing:border-box;background:{PAPER};">{body}</div></x-dc><script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>class Component extends DCLogic{{renderVals(){{return {{}};}}}}</script></body></html>''')
# Match the imagegen proposal's actual hierarchy and optical coordinates.
MAIN=image(0,0,1080,1440)+txt(48,8,240,'折',200,family='Noto Serif CJK SC',lh=1)+txt(48,212,240,'光',200,family='Noto Serif CJK SC',lh=1)+txt(278,365,650,'REFRACTION',26,family='Nimbus Roman',spacing=6,lh=1.2)+txt(58,462,670,'光学与感知研究展',39,family='Noto Serif CJK SC',spacing=8,lh=1.5)+rect(60,543,64,1,INK)+txt(58,574,810,'LIGHT / FORM / PERCEPTION',22,family='Nimbus Roman',spacing=4.5)+txt(58,1314,720,'2026.11.07—12.06',42,family='Nimbus Roman',spacing=2,lh=1.2)+txt(60,1367,510,'10:00—18:00',27,family='Nimbus Roman',spacing=4,lh=1.2)+rect(510,1376,260,1,INK)+txt(813,1360,260,'折光实验展厅',25,family='Noto Serif CJK SC',spacing=3,lh=1.4)
board('Main',1080,1440,'折光｜纸白光场原生海报',MAIN)
INV=image(0,0,1600,2133,fit='fill')+txt(70,58,640,'折光',152,family='Noto Serif CJK SC',spacing=18,lh=1.2)+txt(80,271,700,'REFRACTION  /  OPENING',25,family='Nimbus Roman',spacing=4)+txt(83,419,760,'一场关于光、形与感知的相遇。',35,family='Noto Serif CJK SC',spacing=3)+txt(83,654,800,'2026.11.07',64,family='Nimbus Roman',spacing=1.5,lh=1.2)+txt(86,752,820,'18:30  开幕之夜  /  折光实验展厅',27,family='Noto Serif CJK SC',spacing=1)+txt(87,811,740,'虚构路 18 号 · 凭邀请入场',22,color=MUTED)+txt(1220,72,300,'07',148,color=INK,family='Nimbus Roman',lh=1)+txt(1234,253,300,'NOV / 2026',24,color=INK,family='Nimbus Roman',spacing=3)
board('Invitation',1600,900,'折光｜开幕邀请',INV)
P1=image(0,0,675,900)+txt(760,73,740,'01  /  CURATORIAL STATEMENT',20,color=MUTED,family='Nimbus Roman',spacing=3)+txt(753,180,770,'让光成形，\n让观看\n慢下来。',79,family='Noto Serif CJK SC',spacing=3,lh=1.5)+txt(762,600,745,'A study in light.',64,family='Nimbus Roman',lh=1.3,extra='font-style:italic;')+rect(765,716,72,1,INK)+txt(765,754,700,'一束光，两种边缘。\n以纸白留出观看，以字形交代展览。',26,color=MUTED,lh=1.8)
board('Proposal01',1600,900,'提案01｜展览命题',P1)
P2=txt(64,42,1170,'边缘的两种速度。',82,family='Noto Serif CJK SC',spacing=2,lh=1.4)+txt(1200,87,360,'02 / LIGHT STUDIES',20,family='Nimbus Roman',spacing=2)+image(64,236,840,544,'35% 76%')+image(1010,236,526,275,'76% 51%')+txt(1010,553,490,'清晰的转折',34,family='Noto Serif CJK SC',spacing=2)+txt(1010,616,490,'窄色边建立方向，\n柔和阴影让边界继续延伸。',25,color=MUTED,lh=1.7)+txt(66,813,880,'同一生成光场的两种取景；不是不同机位或物理实验。',19,color=MUTED)+txt(1010,765,490,'局部不替代整体。',32,family='Noto Serif CJK SC')
board('Proposal02',1600,900,'提案02｜光场的边缘',P2)
P3=txt(64,34,1150,'同一种光，走进不同的相遇。',59,family='Noto Serif CJK SC',spacing=2)+txt(65,130,1230,'03 / APPLICATIONS     ·     保留字形、纸白与光场，重新安排信息。',21,color=MUTED,family='Refraction Sans')+group(65,237,.40,1080,1440,MAIN)+group(550,260,.57,1600,900,INV)+txt(65,837,460,'展览海报 / 先看见，再读到',23,family='Noto Serif CJK SC')+txt(550,807,900,'开幕邀请 / 先找到时间，再决定到场',23,family='Noto Serif CJK SC')+txt(550,852,900,'两个版面都是原生文字与同一无字光场组成，不是拉伸海报截图。',20,color=MUTED)
board('Proposal03',1600,900,'提案03｜跨媒介展开',P3)
VR=txt(64,42,920,'让光成形，\n让文字留白。',84,family='Noto Serif CJK SC',spacing=2,lh=1.45)+txt(68,330,770,'REFRACTION / VISUAL LANGUAGE',22,family='Nimbus Roman',spacing=3)+group(1080,43,.37,1080,1440,MAIN)+txt(67,427,885,'01  字形先分工',33,family='Noto Serif CJK SC')+txt(68,490,900,'宋体建立中文主识别；细衬线英文作旁注。\n正文与说明仍保留稳定的无衬线阅读层。',25,color=MUTED,lh=1.8)+txt(67,616,885,'02  光场只讲一件事',33,family='Noto Serif CJK SC')+txt(68,680,900,'保留聚光与展开的方向；信息落在平静纸底。\n蓝与金来自图像，深蓝才进入小号重点文字。',25,color=MUTED,lh=1.8)+rect(67,816,1466,1,'#8C918B')
for x,c,label in [(68,PAPER,'纸白 / F2EDDF'),(530,INK,'墨黑 / 151D20'),(1000,BLUE,'深蓝 / 173D78')]:VR+=rect(x,857,64,64,c)+txt(x+90,865,370,label,23,family='Refraction Sans')
VR+=txt(68,952,1400,'V5  ·  完整AI提案 → 去字光场 → 可编辑字层与跨媒介规则  ·  所有活动为教学虚构',18,color=MUTED)
board('VisualRules',1600,1000,'折光｜视觉规则',VR)
REV=txt(64,33,1430,'先把整张海报想清楚。',68,family='Noto Serif CJK SC',spacing=2)+txt(67,139,1430,'V4 → V5：从银环大字，转向中文宋体、纸白与折射光场。',26,color=MUTED)+image(64,238,410,547,src='refraction-poster-v4.png',fit='contain')+group(614,238,.38,1080,1440,MAIN)+txt(65,830,480,'V4 / 上一版真实导出',25,color=MUTED)+txt(615,830,450,'V5 / 本轮原生重建',25,family='Noto Serif CJK SC')+txt(1130,253,400,'先整张定方向',32,family='Noto Serif CJK SC')+txt(1130,320,400,'完整AI提案同时探索\n图像、字形与留白。',24,color=MUTED,lh=1.8)+txt(1130,463,400,'再拆开制作',32,family='Noto Serif CJK SC')+txt(1130,530,400,'保留无字光场；标题、\n日期和地点回到真实字层。',24,color=MUTED,lh=1.8)+txt(1130,687,400,'最后检验系统',32,family='Noto Serif CJK SC')+txt(1130,754,400,'邀请与提案重排，\n不退回相同左右模板。',24,color=MUTED,lh=1.8)
board('Revision',1600,1000,'折光｜V4到V5方向修订',REV)
# Real reusable component API, not flattened artwork.
b=(S/'components/bundle.js').read_text();start=b.index(' function ExhibitTitle(');end=b.index(' function InfoStrip(',start)
b=b[:start]+''' function ExhibitTitle(p={}){const e=make('div','display:flex;flex-direction:column;gap:var(--space-s);color:var(--ink)');const zh=make('div','font-family:var(--font-serif);font-weight:500;letter-spacing:.06em',p.chinese||'折光');zh.className=p.compact?'subtitle':'title';const en=make('div','font-family:var(--font-latin);font-size:24px;letter-spacing:.2em',p.english||'REFRACTION');e.append(zh,en);return e;}
'''+b[end:]
b=b.replace('refraction-hero-v4.png','refraction-light-v5.png').replace('透明扭转光学玻璃带，冷银反射与一线红色映光；AI生成艺术示意','纸白上的蓝青、金红折射光场；AI生成艺术示意')
write(S/'components/bundle.js',b)
for name in ['ExhibitTitle','PictureFrame','Cover']:
 p=S/f'components/{name}/preview.html';v=p.read_text().replace('A shift in perspective','A study in light').replace('英文展示字与中文展名分工。','中文宋体主识别与细衬线英文分工。').replace('保留玻璃完整弯折或裁出边缘细节。','保留光场聚合与展开，局部裁切只用于细读。');write(p,v)
write(S/'components/ExhibitTitle/README.md','# ExhibitTitle\n\n中文宋体为主识别，细衬线英文为辅助。用REFRACTION.ExhibitTitle(props)返回真实DOM；chinese/english/compact可改，字体与色彩读取原生token。\n')
write(S/'components/PictureFrame/README.md','# PictureFrame\n\n无字光场作为独立位图，不包含海报标题。用src/ratio/position控制图像与裁切，不以局部裁切冒充真实实验。\n')
readme='''# 折光 V5：从完整提案到原生画板

先用imagegen探索完整海报，确认中文宋体、纸白与蓝青/金红光场，再从同一提案去字得到素材，最后将标题、日期、地点与图形重新做成可编辑层。不是把整张AI海报作为背景后盖几行字。

完整提案：../shared-assets/refraction-concept-v5.png；无字底图：../shared-assets/refraction-light-v5.png。宋体为Noto Serif CJK SC Medium（OFL），拉丁衬线为Nimbus Roman（URW许可），正文使用Noto Sans SC（OFL）。实际字形与AI提案略有区别，不宣称逐像素复刻。

当前七块画板：海报、邀请、三页提案、视觉规则与V4→V5对照。所有活动、地址与时间为教学虚构。V4对照为旧版真实导出，非构造的坏稿；新稿由无字素材与原生层组成。

三个真实组件：ExhibitTitle、InfoStrip、PictureFrame。双主题与安装快照保留；更新上游不自动改写已排版的内联值。build_refraction_v5.py重建当前原生源；refresh_refraction_tokens.py调用原生服务编译CSS。原生check/export重新生成截图。CLI 0.26.1021 的PNG导出需要操作系统也安装随附的Noto Serif CJK SC字体：Linux可复制fonts/RefractionSong.otf到用户字体目录后运行fc-cache；编辑器字体由工程内文件加载。
'''
write(S/'README.md',readme);write(C/'README.md',readme)
write(S/'assets/Photography/README.md','# AI折射光场\n\nrefraction-light-v5.png由完整AI提案定向去除所有文字和黑色细线得到，作为可编辑画板的无字背景。它是艺术教学示意，不是真实光学实验照片。光场与标题分层保存。\n')
print('V5 generated: 7 editable boards, 3 reusable components, real local serif fonts')
