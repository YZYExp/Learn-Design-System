"""Rebuild Refraction V4 native sources: optical gallery identity, 7 editable boards.
Run refresh_refraction_tokens.py afterwards to compile CSS through the native service.
The V3 comparison sources/renders are retained in refraction-canvas/renders/v3/.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,html,shutil,sys
R=Path(__file__).resolve().parent;S=R/'refraction-system';C=R/'refraction-canvas';A=R/'shared-assets/refraction-hero-v4.png';FONT=R.parents[1]/'assets/fonts/NotoSansSC-Regular.ttf'
WHITE='#F4F5F7';INK='#101114';RED='#D62A20';SILVER='#C6CBD1';MUTED='#4E535B'
for p in [S/'fonts',S/'assets/Photography',C/'uploads',C/'ds/refraction/fonts']:p.mkdir(parents=True,exist_ok=True)
if A.exists():
 shutil.copy2(A,C/'uploads/refraction-hero-v4.png');shutil.copy2(A,S/'assets/Photography/refraction-hero-v4.png')
elif '--source-only' not in sys.argv:raise FileNotFoundError('shared-assets/refraction-hero-v4.png is required; no substitute photograph is used.')
for p in [S/'fonts/NotoSansSC-Regular.ttf',C/'uploads/NotoSansSC-Regular.ttf',C/'ds/refraction/fonts/NotoSansSC-Regular.ttf']:
 shutil.copy2(FONT,p);shutil.copy2(FONT.parent/'OFL.txt',p.parent/'OFL.txt')
def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_text(s);q.replace(p)
def jwrite(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
T={'name':'折光 / REFRACTION','version':4,'color':{'themes':[{'id':'light','name':'冷白 / Gallery'},{'id':'dark','name':'暗场 / Night'}],'tokens':[
 {'name':'surface','value':{'light':WHITE,'dark':INK},'usage':'冷白或暗场基底；AI玻璃图像为独立可替换媒体。'},
 {'name':'ink','value':{'light':INK,'dark':WHITE},'usage':'阅读文字，on surface。'},
 {'name':'accent','value':RED,'usage':'展览红；大标题、入场票面与短线。'},
 {'name':'on-accent','value':'#FFFFFF','usage':'票面文字，on accent。'},
 {'name':'muted','value':{'light':MUTED,'dark':'#B8BEC6'},'usage':'辅助文字，on surface。'},
 {'name':'hairline','value':{'light':'#A5ABB4','dark':'#666C75'},'usage':'分隔与取景线；不承担文字。'},
 {'name':'silver','value':SILVER,'usage':'银色辅助面、图像边界，不能单独代替光学材质。'},
 {'name':'paper-white','value':'#FFFFFF','usage':'纯白展示面或反白。'}]},
 'type':{'fonts':[{'family':'Refraction Sans','file':'fonts/NotoSansSC-Regular.ttf','weight':'400'}],'families':{'sans':'"Refraction Sans", "Noto Sans SC", Arial, sans-serif'},'groups':[{'name':'光学展览层级','family':'sans','styles':[
 {'name':'display','fontSize':'180px','lineHeight':1.0,'fontWeight':900,'letterSpacing':'-7px','usage':'横向英文展示字；每个载体按比例调整，避免机械同尺寸。'},
 {'name':'title','fontSize':'96px','lineHeight':1.15,'fontWeight':800,'letterSpacing':'-2px','usage':'中文展名、提案关键判断。'},
 {'name':'subtitle','fontSize':'44px','lineHeight':1.3,'fontWeight':600,'usage':'短句和单元标题。'},
 {'name':'body','fontSize':'28px','lineHeight':1.65,'fontWeight':400,'usage':'提案与规则的完整解释。'},
 {'name':'meta','fontSize':'24px','lineHeight':1.5,'fontWeight':400,'usage':'日期、地点与入场说明。'},
 {'name':'caption','fontSize':'18px','lineHeight':1.5,'fontWeight':400,'usage':'图注与编辑标记。'}]}]},
 'spacing':{'tokens':[{'name':'space-xs','value':'8px','usage':'字标与小编号。'},{'name':'space-s','value':'16px','usage':'同组信息。'},{'name':'space-m','value':'32px','usage':'信息块之间。'},{'name':'space-l','value':'64px','usage':'竖版安全区。'},{'name':'space-xl','value':'80px','usage':'横版与编辑页外边界。'}]},
 'radius':{'tokens':[{'name':'radius-sharp','value':'0px','usage':'海报、照片与票面的直角边界。'},{'name':'radius-dot','value':'50%','usage':'少量独立标记。'}]},'shadow':{'tokens':[{'name':'shadow-none','value':'none','usage':'不为板块添加卡片阴影；光影由图像本身提供。'}]}}
jwrite(S/'tokens.json',T);jwrite(C/'ds/refraction/tokens.json',T)
if (S/'design-system.json').exists():
 idx=json.loads((S/'design-system.json').read_text());idx.update({'title':'折光 / REFRACTION · V4','namespace':'REFRACTION','groups':[{'name':'Exhibition','components':['ExhibitTitle','InfoStrip','PictureFrame']}],'assetGroups':{'Photography':{'title':'光学玻璃主视觉'}},'docs':{'readme':'project/README.md','sections':[]}});jwrite(S/'design-system.json',idx)
BUNDLE='''/* @ds-bundle: {"format":4,"namespace":"REFRACTION","components":[{"name":"ExhibitTitle"},{"name":"InfoStrip"},{"name":"PictureFrame"}]} */
(function(){
 const make=(tag,style,text)=>{const e=document.createElement(tag);e.style.cssText=style;if(text!==undefined)e.textContent=text;return e;};
 function ExhibitTitle(p={}){const e=make('div','display:flex;flex-direction:column;gap:var(--space-s);font-family:var(--font-sans);color:var(--ink);');const en=make('div','font-weight:900;letter-spacing:-0.04em;line-height:1;',p.english||'REFRACTION');en.className=p.compact?'subtitle':'title';e.append(en);const zh=make('div','letter-spacing:0.08em;',p.chinese||'折光 — 光学与感知研究展');zh.className='meta';e.append(zh);return e;}
 function InfoStrip(p={}){const e=make('div','display:flex;flex-wrap:wrap;gap:var(--space-l);padding-top:var(--space-s);border-top:1px solid var(--hairline);font-family:var(--font-sans);color:var(--ink);');e.className='meta';const a=make('div','display:flex;flex-direction:column;');a.append(make('div','font-weight:600;',p.date||'2026.11.07—12.06'));const hours=make('div','color:var(--muted);',p.hours||'10:00—18:00 · 周一闭馆');hours.className='caption';a.append(hours);const b=make('div','display:flex;flex-direction:column;');b.append(make('div','',p.venue||'折光实验展厅'));const address=make('div','color:var(--muted);',p.address||'虚构路 18 号');address.className='caption';b.append(address);e.append(a,b);return e;}
 function PictureFrame(p={}){const e=make('figure','margin:0;position:relative;overflow:hidden;border-radius:var(--radius-sharp);width:100%;aspect-ratio:'+(p.ratio||'3 / 4')+';background:var(--surface);');const im=document.createElement('img');im.src=p.src||'../../assets/Photography/refraction-hero-v4.png';im.alt='透明扭转光学玻璃带，冷银反射与一线红色映光；AI生成艺术示意';im.style.cssText='width:100%;height:100%;display:block;object-fit:cover;object-position:'+(p.position||'50% 50%')+';';e.append(im);return e;}
 window.REFRACTION={ExhibitTitle,InfoStrip,PictureFrame};})();'''
write(S/'components/bundle.js',BUNDLE);write(S/'components/bundle.css','/* Typography classes and font faces are compiled natively from tokens.json. */\n')
write(S/'components/index.d.ts','''export interface ExhibitTitleProps {chinese?:string;english?:string;compact?:boolean}
export interface InfoStripProps {date?:string;hours?:string;venue?:string;address?:string}
export interface PictureFrameProps {src?:string;ratio?:string;position?:string}
export declare function ExhibitTitle(p?:ExhibitTitleProps): HTMLElement;
export declare function InfoStrip(p?:InfoStripProps): HTMLElement;
export declare function PictureFrame(p?:PictureFrameProps): HTMLElement;
''')
previews={
'ExhibitTitle':('英文展示字与中文展名分工。',360,"root.style.cssText='display:flex;flex-direction:column;gap:var(--space-l);padding:var(--space-m)';root.append(REFRACTION.ExhibitTitle({}),REFRACTION.ExhibitTitle({english:'A SHIFT IN PERSPECTIVE',chinese:'让观看发生偏转',compact:true}));"),
'InfoStrip':('到场条件作为一个信息组。',180,"root.style.cssText='padding:var(--space-m)';root.append(REFRACTION.InfoStrip({}));"),
'PictureFrame':('保留玻璃完整弯折或裁出边缘细节。',740,"root.style.cssText='display:grid;grid-template-columns:0.8fr 1.2fr;gap:var(--space-m);padding:var(--space-m)';root.append(REFRACTION.PictureFrame({ratio:'3 / 4'}),REFRACTION.PictureFrame({ratio:'4 / 3',position:'82% 28%'}));")}
for n,(desc,h,js) in previews.items():
 write(S/f'components/{n}/README.md',f'# {n}\n\n{desc}\n\n以`REFRACTION.{n}(props)`调用，返回真实DOM；颜色、字体与间距读取原生token。公开参数见components/index.d.ts。不要用组件截图替代组件。\n')
 write(S/f'components/{n}/preview.html',f'''<!-- @dsCard group="Exhibition" height={h} subtitle="{desc}" -->
<!doctype html><html lang="zh"><head><meta charset="utf-8"></head><body><div id="root"></div><script>const root=document.getElementById('root');{js}</script></body></html>''')
write(S/'components/Cover/preview.html','''<!-- @dsCard group="Cover" height=420 subtitle="A shift in perspective" -->
<!doctype html><html lang="zh"><head><meta charset="utf-8"></head><body><div id="root"></div><script>const e=document.getElementById('root');e.style.cssText='display:grid;grid-template-columns:1fr 1fr;gap:var(--space-m);align-items:center;padding:var(--space-m);font-family:var(--font-sans);';e.append(REFRACTION.ExhibitTitle({compact:true}));const im=REFRACTION.PictureFrame({ratio:'16 / 8',position:'50% 50%'});e.append(im);</script></body></html>''')
write(S/'assets/Photography/README.md','# 光学玻璃主视觉\n\nrefraction-hero-v4.png为本次实际AI生成的光学玻璃艺术示意。材质有透射、银色反射与一线红色映光，不是真实物理实验或实拍展览。源图shared-assets/refraction-hero-v4.png；V3纸面/石膏图仅保留作历史比较，不再作为正式主视觉。\n')
def text(x,y,w,s,size=28,color=INK,weight=400,lh=1.3,extra=''):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;line-height:{lh};font-weight:{weight};color:{color};white-space:pre-line;{extra}">{html.escape(s)}</div>'
def rect(x,y,w,h,c,extra=''):return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};{extra}"></div>'
def img(x,y,w,h,pos='50% 50%',old=False,extra=''):
 src='refraction-hero-v3.png' if old else 'refraction-hero-v4.png'
 return f'<img src="uploads/{src}" alt="'+('V3纸面与石膏材质研究示意' if old else '透明扭转光学玻璃带，银反射与红色映光；AI生成艺术示意')+f'" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;display:block;object-fit:cover;object-position:{pos};{extra}">'
def line(x,y,w,c=INK):return rect(x,y,w,1,c)
def group(x,y,scale,w,h,b):return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:scale({scale});transform-origin:0 0;overflow:hidden;background:{WHITE};">{b}</div>'
def board(name,w,h,title,b,bg=WHITE):
 write(C/name,f'''<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>{title}</title><script src="./support.js"></script></head><body><x-dc><helmet><style>@font-face{{font-family:"Refraction Sans";src:url(uploads/NotoSansSC-Regular.ttf) format("truetype");font-weight:400;font-style:normal;}}body{{margin:0;font-family:"Refraction Sans","Noto Sans SC",Arial,sans-serif;color:{INK};}}a{{color:inherit;}}</style></helmet><div style="position:relative;width:{w}px;height:{h}px;box-sizing:border-box;overflow:hidden;background:{bg};">{b}</div></x-dc><script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>class Component extends DCLogic{{renderVals(){{return {{}};}}}}</script></body></html>''')
# Main: the glass is the field, not a rectangular illustration under a gigantic Chinese label.
MAIN=img(0,120,1080,1440,'50% 50%')+text(48,26,1000,'REFRACTION',121,weight=900,lh=1.08,extra='letter-spacing:-5.5px;')+text(57,180,670,'LIGHT / MATERIAL / PERCEPTION',18,weight=500,extra='letter-spacing:2.4px;')+text(57,1058,300,'折光',102,RED,700,1.1,'letter-spacing:6px;')+text(62,1190,680,'光学与感知研究展',28,weight=500,extra='letter-spacing:3px;')+rect(0,1300,1080,140,WHITE)+line(60,1315,960)+text(60,1340,510,'2026.11.07—12.06',30,weight=600)+text(60,1390,530,'10:00—18:00 · 周一闭馆',18,MUTED)+text(716,1340,310,'折光实验展厅',27,weight=600)+text(716,1390,310,'REFRACTION LAB',18,MUTED,extra='letter-spacing:1px;')
board('Main.dc.html',1080,1440,'折光｜光学艺术展海报',MAIN)
# Invitation: a luminous image field meets a saturated admission panel.
INV=img(0,0,1060,900,'50% 40%')+text(55,42,900,'REFRACTION',72,weight=900,lh=1.1,extra='letter-spacing:-3px;')+f'<div style="position:absolute;left:0;top:810px;width:1060px;height:90px;background:{WHITE};">'+text(60,27,900,'一场关于光、材料与观看的相遇。',28,weight=500)+'</div>'+f'<div style="position:absolute;left:1060px;top:0;width:540px;height:900px;background:{RED};">'+text(50,47,430,'OPENING / INVITATION',19,'#FFFFFF',500,1.4,'letter-spacing:1.6px;')+text(44,154,440,'07',192,'#FFFFFF',900,1.0,'letter-spacing:-10px;')+text(55,371,420,'NOVEMBER 2026',30,'#FFFFFF',600,1.3,'letter-spacing:1.2px;')+line(55,451,430,'#FFFFFF')+text(55,496,430,'开幕之夜',58,'#FFFFFF',700,1.2,'letter-spacing:2px;')+text(57,600,430,'18:30  /  折光实验展厅',26,'#FFFFFF')+text(57,658,430,'虚构路 18 号',24,'#FFFFFF')+text(57,802,430,'凭邀请入场 · 光学艺术研究展',20,'#FFFFFF')+'</div>' 
board('Invitation.dc.html',1600,900,'折光｜开幕邀请',INV)
# Proposal 1: complete object at left; a typographic curatorial statement on a generous field.
P1=img(0,0,720,900,'50% 43%')+text(800,60,670,'01 / CURATORIAL STATEMENT',20,extra='letter-spacing:1.8px;')+text(794,178,720,'看见光。\n也看见\n它的偏转。',98,weight=700,lh=1.3,extra='letter-spacing:-2px;')+rect(804,625,90,7,RED)+text(804,677,650,'透明的边缘，反射的表面。\n熟悉的材料，让观看重新发生。',28,lh=1.7)+text(804,832,650,'REFRACTION  /  折光 · 2026',20,MUTED,extra='letter-spacing:1px;')
board('Proposal01.dc.html',1600,900,'提案01｜展览命题',P1)
# Proposal 2: an asymmetrical editorial rhythm, rather than three identical cards.
P2=text(65,47,850,'A SHIFT IN\nPERSPECTIVE',90,weight=900,lh=1.02,extra='letter-spacing:-4px;')+text(1160,75,360,'02 / 观看的三次转折',20,extra='letter-spacing:1px;')+img(65,286,590,550,'18% 32%')+text(690,306,310,'01',100,RED,800,1.0)+text(697,438,300,'透过边缘',36,weight=600)+text(697,505,300,'透明，让背景\n成为形体的一部分。',25,MUTED,lh=1.7)+text(697,684,300,'02',100,weight=800,lh=1.0)+text(697,806,300,'随角度偏转',33,weight=600)+img(1080,280,455,300,'83% 20%')+text(1080,638,400,'03  捕捉一线红',37,RED,600)+text(1080,718,420,'银色保持冷静。\n红光只在关键转折处出现。',25,MUTED,lh=1.7)+text(65,854,600,'同一AI图像的裁切研究，非不同机位或物理实验。',17,MUTED)
board('Proposal02.dc.html',1600,900,'提案02｜观看路径',P2)
# Proposal 3: real source compositions in two sizes, with no generic card containers.
P3=rect(0,0,1600,900,'#E3E6EA')+text(65,42,1230,'ONE IDENTITY.\nDIFFERENT ENCOUNTERS.',63,weight=900,lh=1.05,extra='letter-spacing:-2px;')+text(1340,57,180,'03 / 应用',20)+group(65,250,.38,1080,1440,MAIN)+group(545,250,.58,1600,900,INV)+text(65,832,420,'远处识别 / 展览海报',21,weight=600)+text(545,805,870,'到场信息 / 开幕邀请',21,weight=600)+text(545,849,950,'相同英文识别与玻璃焦点，改变文字尺寸、裁切比例与信息密度。',20,MUTED)
board('Proposal03.dc.html',1600,900,'提案03｜跨媒介展开',P3,'#E3E6EA')
# Visual rules presented as a designed editorial plate, not a grid of instruction cards.
VR=text(60,36,1470,'OPTICAL / NOT ORNAMENTAL',78,weight=900,lh=1.15,extra='letter-spacing:-3px;')+text(64,145,1200,'折光的视觉系统：图像给出张力，文字建立秩序。',28,weight=500)+img(60,235,430,520,'50% 50%')+img(540,235,380,260,'84% 19%')+text(540,534,440,'REFRACTION',45,weight=900,extra='letter-spacing:-1.5px;')+text(544,610,420,'折光 / 光学与感知研究展',25,weight=500)+text(544,683,420,'展示字：紧密，但不相撞。\n中文：保持呼吸与完整字形。',22,MUTED,lh=1.8)+text(1030,247,480,'01  留住完整弯折',34,weight=600)+text(1030,310,480,'海报与命题页保留足够形体，\n细节页才允许更紧的裁切。',24,MUTED,lh=1.7)+text(1030,440,480,'02  信息按任务缩放',34,weight=600)+text(1030,503,480,'远看先认展览，近看再找日期。\n邀请不是海报的横向拉伸。',24,MUTED,lh=1.7)+text(1030,633,480,'03  只给一处红',34,weight=600)+text(1030,696,480,'红色建立入口或票面，\n不在每个信息块重复强调。',24,MUTED,lh=1.7)+line(60,810,1480)+rect(60,849,64,64,INK)+text(145,857,300,'INK  /  101114',22)+rect(500,849,64,64,RED)+text(585,857,300,'RED  /  D62A20',22)+rect(950,849,64,64,SILVER)+text(1035,857,430,'SILVER  /  C6CBD1',22)+text(60,951,1000,'8 / 16 / 32 / 64 / 80    ·    Noto Sans SC / 本地字体    ·    V4',17,MUTED)
board('VisualRules.dc.html',1600,1000,'折光｜视觉规则',VR)
# Revision preserves an editable V3 reference rather than pretending one photo was merely rearranged.
oldpath=C/'renders/v3/Main-fragment.html';old=oldpath.read_text() if oldpath.exists() else img(0,0,1080,1440,old=True)
REV=text(65,35,1350,'从材质练习，到一场光学艺术展。',61,weight=700)+text(65,133,1380,'V3 → V4：保留展名与到场内容，重做主视觉、展示字与媒介比例。',25,MUTED)+group(65,235,.44,1080,1440,old)+group(625,235,.44,1080,1440,MAIN)+text(65,894,480,'V3 / 纸面与体量',24,MUTED)+text(625,894,480,'V4 / 透明、反射与偏转',24,weight=600)+text(1210,257,320,'更强的图像焦点',31,weight=600)+text(1210,326,320,'完整玻璃弯折代替\n被斜切的矩形照片。',22,MUTED,lh=1.8)+text(1210,486,320,'有分工的展示字',31,weight=600)+text(1210,555,320,'英文建立展览识别，\n中文交代具体主题。',22,MUTED,lh=1.8)+text(1210,714,320,'真正跨媒介重排',31,weight=600)+text(1210,783,320,'海报、邀请与提案\n不再套用同一比例。',22,MUTED,lh=1.8)
board('Revision.dc.html',1600,1000,'折光｜V3到V4改稿对照',REV)
idx=json.loads((C/'canvas.json').read_text());idx['title']='折光 / REFRACTION · 光学艺术展 V4';oldboards=idx.get('boards',{});idx['boards']={}
boards=[('VisualRules.dc.html',0,0,1600,1000,'视觉规则'),('Main.dc.html',0,1120,1080,1440,'竖版海报'),('Invitation.dc.html',1160,1120,1600,900,'开幕邀请'),('Proposal01.dc.html',0,2680,1600,900,'提案01 · 展览命题'),('Proposal02.dc.html',1680,2680,1600,900,'提案02 · 观看路径'),('Proposal03.dc.html',3360,2680,1600,900,'提案03 · 跨媒介'),('Revision.dc.html',1680,0,1600,1000,'V3 → V4改稿对照')]
for n,x,y,w,h,title in boards:idx['boards'][n]={**oldboards.get(n,{}),'x':x,'y':y,'w':w,'h':h,'title':title}
idx['order']=['Main.dc.html','VisualRules.dc.html','Invitation.dc.html','Proposal01.dc.html','Proposal02.dc.html','Proposal03.dc.html','Revision.dc.html']
idx.setdefault('notes',{}).update({'t1':{'kind':'title1','x':0,'y':-250,'text':'REFRACTION / 光学与感知研究展','maxW':3280},'t2':{'kind':'title1','x':0,'y':2430,'text':'一种识别，三次不同的相遇','maxW':4960}})
idx['designSystems']=[{'title':'折光 / REFRACTION','namespace':'refraction','artifact':'projects/refraction-system','version':4,'copiedAt':datetime.now(timezone.utc).isoformat()}];jwrite(C/'canvas.json',idx)
# README sources are deliberately maintained outside this generator to keep prose reviewable.
print('Rebuilt Refraction V4: 7 editable artboards, version-4 token snapshot and 3 callable native components. Run native token refresh, check, export and component QA.')
