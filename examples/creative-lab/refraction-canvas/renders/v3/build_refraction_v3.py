"""Rebuild the original Refraction native projects; no flattened text or fabricated image.
First create native indexes with `tingly-design new`, then run this script.
With --source-only all editable sources are restored even before AI image is ready.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,shutil,html,sys
R=Path(__file__).resolve().parent;S=R/'refraction-system';C=R/'refraction-canvas';A=R/'shared-assets/refraction-hero.png';FONT=R.parents[1]/'assets/fonts/NotoSansSC-Regular.ttf'
for p in [S/'fonts',S/'assets/Photography',C/'uploads',C/'ds/refraction/fonts']:p.mkdir(parents=True,exist_ok=True)
if A.exists():
 shutil.copy2(A,C/'uploads/refraction-hero.png');shutil.copy2(A,S/'assets/Photography/refraction-hero.png')
elif '--source-only' not in sys.argv:raise FileNotFoundError('Generate shared-assets/refraction-hero.png first; no fake photograph is substituted.')
for p in [S/'fonts/NotoSansSC-Regular.ttf',C/'uploads/NotoSansSC-Regular.ttf',C/'ds/refraction/fonts/NotoSansSC-Regular.ttf']:
 shutil.copy2(FONT,p);shutil.copy2(FONT.parent/'OFL.txt',p.parent/'OFL.txt')
def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_text(s);q.replace(p)
def jwrite(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
T={'name':'折光 / REFRACTION','version':1,'color':{'themes':[{'id':'light','name':'纸面 / Paper'},{'id':'dark','name':'暗场 / Darkroom'}],'tokens':[
{'name':'surface','value':{'light':'#F3F0E8','dark':'#191919'},'usage':'纸面与暗场背景，不叠加渐变。'},
{'name':'ink','value':{'light':'#191919','dark':'#F3F0E8'},'usage':'标题与正文，on surface。'},
{'name':'accent','value':'#C7472E','usage':'编号、大字或短线；小字号文字使用ink。'},
{'name':'on-accent','value':'#FFFFFF','usage':'白字，on accent。'},
{'name':'muted','value':{'light':'#5D5A54','dark':'#C0BCB3'},'usage':'辅助文字，on surface。'},
{'name':'hairline','value':{'light':'#B6B0A3','dark':'#77736B'},'usage':'网格与分隔，不用于正文。'},
{'name':'paper-white','value':'#FFFFFF','usage':'反白实验与出片标记。'}]},
 'type':{'fonts':[{'family':'Refraction Sans','file':'fonts/NotoSansSC-Regular.ttf','weight':'400'}],'families':{'sans':'"Refraction Sans", "Noto Sans SC", Arial, sans-serif'},'groups':[{'name':'展览层级','family':'sans','styles':[
{'name':'display','fontSize':'176px','lineHeight':1.04,'fontWeight':400,'letterSpacing':'-6px','usage':'每板一次的品牌入口。'},
{'name':'title','fontSize':'88px','lineHeight':1.12,'fontWeight':400,'letterSpacing':'-3px','usage':'提案主标题。'},
{'name':'subtitle','fontSize':'48px','lineHeight':1.3,'fontWeight':400,'usage':'短句与跨媒介标题。'},
{'name':'body','fontSize':'28px','lineHeight':1.65,'fontWeight':400,'usage':'提案的完成叙述。'},
{'name':'meta','fontSize':'24px','lineHeight':1.5,'fontWeight':400,'usage':'日期地点。'},
{'name':'caption','fontSize':'18px','lineHeight':1.5,'fontWeight':400,'usage':'编号、图注和页码。'}]}]},
 'spacing':{'tokens':[{'name':'space-xs','value':'8px','usage':'小编号。'},{'name':'space-s','value':'16px','usage':'同组信息。'},{'name':'space-m','value':'32px','usage':'块内节奏。'},{'name':'space-l','value':'64px','usage':'竖海报边距。'},{'name':'space-xl','value':'80px','usage':'横版边距。'}]},
 'radius':{'tokens':[{'name':'radius-sharp','value':'0px','usage':'图像与面保持直角。'},{'name':'radius-dot','value':'50%','usage':'独立圆点。'}]},'shadow':{'tokens':[{'name':'shadow-none','value':'none','usage':'组件不增加阴影，使用真实主视觉的光影。'}]}}
jwrite(S/'tokens.json',T);jwrite(C/'ds/refraction/tokens.json',T)
if (S/'design-system.json').exists():
 idx=json.loads((S/'design-system.json').read_text());idx.update({'title':'折光 / REFRACTION','namespace':'REFRACTION','groups':[{'name':'Exhibition','components':['ExhibitTitle','InfoStrip','PictureFrame']}],'assetGroups':{'Photography':{'title':'材质主视觉'}},'docs':{'readme':'project/README.md','sections':[]}});jwrite(S/'design-system.json',idx)
BUNDLE='''/* @ds-bundle: {"format":4,"namespace":"REFRACTION","components":[{"name":"ExhibitTitle"},{"name":"InfoStrip"},{"name":"PictureFrame"}]} */
(function(){
 const make=(tag,style,text)=>{const e=document.createElement(tag);e.style.cssText=style;if(text!==undefined)e.textContent=text;return e;};
 function ExhibitTitle(p={}){const e=make('div','display:flex;flex-direction:column;gap:var(--space-s);font-family:var(--font-sans);color:var(--ink);');const title=make('div','line-height:1.08;letter-spacing:-0.035em;',p.chinese||'折光');title.className=p.compact?'subtitle':'title';e.append(title);const english=make('div','line-height:1.3;letter-spacing:0.06em;',p.english||'REFRACTION');english.className='meta';e.append(english);return e;}
 function InfoStrip(p={}){const e=make('div','display:flex;gap:var(--space-l);padding-top:var(--space-s);border-top:1px solid var(--hairline);font-family:var(--font-sans);color:var(--ink);line-height:1.5;');e.className='meta';const a=make('div','display:flex;flex-direction:column;');a.append(make('div','',p.date||'2026.11.07—12.06'));const hours=make('div','color:var(--muted);',p.hours||'10:00—18:00 · 周一闭馆');hours.className='caption';a.append(hours);const b=make('div','display:flex;flex-direction:column;');b.append(make('div','',p.venue||'折光实验展厅'));const address=make('div','color:var(--muted);',p.address||'虚构路 18 号 · 研究展览');address.className='caption';b.append(address);e.append(a,b);return e;}
 function PictureFrame(p={}){const e=make('figure','margin:0;position:relative;overflow:hidden;border-radius:var(--radius-sharp);width:100%;aspect-ratio:'+(p.ratio||'4 / 3')+';background:var(--surface);');const im=document.createElement('img');im.src=p.src||'../../assets/Photography/refraction-hero.png';im.alt='白色纸面、石膏与朱红色块的斜向光影构成';im.style.cssText='width:100%;height:100%;display:block;object-fit:cover;object-position:'+(p.position||'50% 50%')+';'+(p.diagonal?'clip-path:polygon(18% 0,100% 0,100% 100%,0 100%);':'');e.append(im);return e;}
 window.REFRACTION={ExhibitTitle,InfoStrip,PictureFrame};})();'''
write(S/'components/bundle.js',BUNDLE);write(S/'components/bundle.css','/* Fonts and style classes are generated natively from tokens.json. */\n')
write(S/'components/index.d.ts','''export interface ExhibitTitleProps {chinese?:string;english?:string;compact?:boolean}
export interface InfoStripProps {date?:string;hours?:string;venue?:string;address?:string}
export interface PictureFrameProps {src?:string;ratio?:string;position?:string;diagonal?:boolean}
export declare function ExhibitTitle(p?:ExhibitTitleProps): HTMLElement;
export declare function InfoStrip(p?:InfoStripProps): HTMLElement;
export declare function PictureFrame(p?:PictureFrameProps): HTMLElement;
''')
previews={
'ExhibitTitle':('两种密度，中文在前。',340,"root.style.cssText='display:flex;gap:var(--space-xl);padding:var(--space-m)';root.append(REFRACTION.ExhibitTitle({}),REFRACTION.ExhibitTitle({chinese:'重新观看',english:'A NEW ANGLE',compact:true}));"),
'InfoStrip':('日期与场所聚合。',180,"root.style.cssText='padding:var(--space-m)';root.append(REFRACTION.InfoStrip({}));"),
'PictureFrame':('同一AI素材的完整与斜切裁切。',440,"root.style.cssText='display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--space-m);padding:var(--space-m)';root.append(REFRACTION.PictureFrame({ratio:'4 / 3'}),REFRACTION.PictureFrame({ratio:'4 / 3',position:'50% 55%',diagonal:true}));")}
for n,(desc,h,js) in previews.items():
 write(S/f'components/{n}/README.md',f'# {n}\n\n{desc}\n\n以`REFRACTION.{n}(props)`调用，返回真实DOM；字号、颜色与间距来自原生tokens。不要以截图替代组件。\n')
 write(S/f'components/{n}/preview.html',f'''<!-- @dsCard group="Exhibition" height={h} subtitle="{desc}" -->
<!doctype html><html lang="zh"><head><meta charset="utf-8"></head><body><div id="root"></div><script>const root=document.getElementById('root');{js}</script></body></html>''')
write(S/'components/Cover/preview.html','''<!-- @dsCard group="Cover" height=380 subtitle="一束光，多种观看" -->
<!doctype html><html lang="zh"><head><meta charset="utf-8"></head><body><div id="root"></div><script>const e=document.getElementById('root');e.style.cssText='display:grid;grid-template-columns:1fr 1fr;gap:var(--space-l);padding:var(--space-m);';e.append(REFRACTION.ExhibitTitle({}),REFRACTION.PictureFrame({ratio:'16 / 9',src:'../../assets/Photography/refraction-hero.png'}));</script></body></html>''')
write(S/'assets/Photography/README.md','# 材质主视觉\n\nrefraction-hero.png是本次实际AI生图，不是实拍或历史原作。源文件在相邻shared-assets，当前为项目内副本。保留折面、硬光与朱红色块的关系，不以小裁切冒充新摄影视角。\n')
PAPER='#F3F0E8';INK='#191919';RED='#C7472E';MUTED='#5D5A54'
def text(x,y,w,s,size=28,color=INK,weight=400,lh=1.3,extra=''):
 return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;line-height:{lh};font-weight:{weight};color:{color};white-space:pre-line;{extra}">{html.escape(s)}</div>'
def rect(x,y,w,h,c,extra=''):return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};{extra}"></div>'
def img(x,y,w,h,pos='50% 50%',clip=False):return f'<img src="uploads/refraction-hero.png" alt="白色纸面与石膏的斜向光影，朱红色块位于结构中央" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;display:block;object-fit:cover;object-position:{pos};'+('clip-path:polygon(18% 0,100% 0,100% 100%,0 100%);' if clip else '')+'">'
def line(x,y,w,c=INK):return rect(x,y,w,1,c)
def board(name,w,h,title,b):
 write(C/name,f'''<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>{title}</title><script src="./support.js"></script></head><body><x-dc><helmet><style>@font-face{{font-family:"Refraction Sans";src:url(uploads/NotoSansSC-Regular.ttf) format("truetype");font-weight:400;font-style:normal;}}body{{margin:0;font-family:"Refraction Sans","Noto Sans SC",Arial,sans-serif;color:{INK};}}a{{color:inherit;}}</style></helmet><div style="position:relative;width:{w}px;height:{h}px;box-sizing:border-box;overflow:hidden;background:{PAPER};">{b}</div></x-dc><script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>class Component extends DCLogic{{renderVals(){{return {{}};}}}}</script></body></html>''')
# Original seven board compositions.
b=text(64,58,700,'FOLD / LIGHT / PERCEPTION',22,extra='letter-spacing:3px;')+text(870,58,150,'2026',22)+text(56,143,950,'折光',260,lh=1.07,extra='letter-spacing:-18px;')+text(64,440,960,'REFRACTION',68,extra='letter-spacing:3px;')+img(346,555,670,666,'50% 53%',True)+rect(64,603,214,16,RED)+text(64,665,270,'每一次偏转，\n都是新的观看。',32,lh=1.65)+text(64,1010,240,'纸面 / 石膏 / 光',22,MUTED)+line(64,1270,952)+text(64,1300,485,'2026.11.07—12.06',29)+text(64,1350,490,'10:00—18:00 · 周一闭馆',21,MUTED)+text(640,1300,380,'折光实验展厅',29)+text(640,1350,380,'REFRACTION LAB',21,MUTED,extra='letter-spacing:2px;')
board('Main.dc.html',1080,1440,'折光｜展览海报',b)
b=img(790,0,810,900,'50% 45%',True)+text(80,62,690,'OPENING INVITATION',22,extra='letter-spacing:3px;')+rect(80,126,96,8,RED)+text(68,180,730,'折光',194,lh=1.05,extra='letter-spacing:-12px;')+text(80,401,710,'REFRACTION',55,extra='letter-spacing:3px;')+text(80,510,600,'与我们一起，重新观看光。',32)+text(80,656,620,'开幕之夜  2026.11.07  18:30',28)+text(80,710,540,'折光实验展厅 · 虚构路 18 号',24,MUTED)+line(80,799,600)+text(80,828,650,'光与材料研究展  /  入场凭邀请',19,MUTED)
board('Invitation.dc.html',1600,900,'折光｜开幕邀请',b)
b=text(64,42,950,'折光的视觉语法',70)+text(1210,65,330,'REFRACTION / 01',22,extra='letter-spacing:2px;')+line(64,150,1472)+text(64,190,430,'01  三种颜色，各司其职',28)
for x,c,lab in [(64,PAPER,'PAPER / F3F0E8'),(212,INK,'INK / 191919'),(360,RED,'ACCENT / C7472E')]:b+=rect(x,250,130,130,c,'border:1px solid #B6B0A3;box-sizing:border-box;')+text(x,400,140,lab,15)
b+=text(64,470,430,'折光 Aa',98,extra='letter-spacing:-4px;')+text(64,605,430,'176 / 88 / 48 / 28 / 24 / 18',21,MUTED)+text(64,660,430,'中文先读，英文辨认。\n日期与地点始终成组。',25,lh=1.7)+text(575,190,430,'02  图像保留光与材料的关系',28)+img(575,250,430,300,'50% 48%')+text(575,580,430,'完整裁切 / 看清体量',23)+img(575,645,430,220,'50% 68%',True)+text(575,890,430,'斜切 / 延续画面的方向',23)+text(1080,190,460,'03  六栏，容纳两种尺度',28)
for i in range(6):b+=rect(1080+i*76,250,64,500,'#DDD7CB')
b+=text(1095,290,430,'让光，\n再走一次。',72,lh=1.2,extra='letter-spacing:-3px;')+text(1095,534,390,'大字建立入口。\n完整图像承载材质。\n细信息在底部汇合。',25,lh=1.8)+rect(1095,746,150,8,RED)+text(1080,808,460,'8 · 16 · 32 · 64 · 80',30)+text(1080,870,460,'从同组呼吸，到画板边界。',22,MUTED)
board('VisualRules.dc.html',1600,1000,'折光｜视觉规则',b)
b=img(780,0,820,900,'50% 52%')+text(80,64,650,'折光 / EXHIBITION PROPOSAL',22,extra='letter-spacing:2px;')+text(74,220,750,'让光，\n再走一次。',116,lh=1.2,extra='letter-spacing:-5px;')+rect(80,565,150,12,RED)+text(80,624,610,'从纸的折面、石膏的体量，\n看见光线重新组织日常。',30,lh=1.65)+text(80,824,600,'REFRACTION LAB · 2026',20,MUTED)
board('Proposal01.dc.html',1600,900,'提案01｜展览命题',b)
b=text(80,55,1100,'三种观看，连成一次探索。',66,lh=1.2)+text(1420,76,100,'02 / 03',20)+line(80,168,1440)
for x,num,title,caption,pos in [(80,'01','看见边界','从物的轮廓，辨认光的方向。','12% 26%'),(570,'02','改变角度','走近折面，观察阴影怎样转折。','50% 52%'),(1060,'03','重新成像','退后一步，让局部重新组成整体。','82% 74%')]:b+=img(x,216,440,420,pos)+text(x,666,80,num,24,RED)+text(x,710,440,title,46)+text(x,785,440,caption,23,MUTED)
board('Proposal02.dc.html',1600,900,'提案02｜观看路径',b)
b=text(80,55,1250,'同一束光，进入不同的场景。',66,lh=1.2)+text(1420,76,100,'03 / 03',20)+line(80,168,1440)+rect(80,220,330,470,PAPER,'border:1px solid #B6B0A3;box-sizing:border-box;')+text(100,242,290,'折光',79,extra='letter-spacing:-5px;')+text(100,345,290,'REFRACTION',23,extra='letter-spacing:1px;')+img(170,405,215,205,'50% 53%',True)+text(100,635,290,'2026.11.07—12.06',17)+rect(470,285,580,326,PAPER,'border:1px solid #B6B0A3;box-sizing:border-box;')+img(750,286,299,324,'50% 45%',True)+text(496,318,240,'折光',70,extra='letter-spacing:-4px;')+text(496,415,250,'REFRACTION',21)+text(496,515,250,'开幕之夜 · 11.07',18)+text(1130,260,380,'大字与图，\n各有位置。',61,lh=1.3,extra='letter-spacing:-2px;')+text(1130,470,380,'海报：先建立远处的印象。\n邀请：聚合到场的信息。\n提案：解释观看的次序。',24,lh=1.9)+text(80,751,980,'共享：纸色、字形、朱红强调、光影材质。',26)+text(80,804,980,'调整：图像裁切、主次比例与信息密度。',26,MUTED)+text(1130,794,380,'折光实验展厅\nREFRACTION LAB',22,lh=1.6)
board('Proposal03.dc.html',1600,900,'提案03｜跨媒介展开',b)
b=text(64,40,1100,'同一份内容，重排阅读顺序。',60)+text(1340,62,200,'EDIT / 01',20)+line(64,137,1472)
for x,title in [(64,'BEFORE / 入口分散'),(650,'AFTER / 先主题，再信息')]:b+=text(x,174,520,title,25)+rect(x,230,520,690,PAPER,'border:1px solid #B6B0A3;box-sizing:border-box;')
b+=text(84,258,480,'2026.11.07—12.06',25,extra='text-align:center;')+text(84,319,480,'REFRACTION',37,extra='text-align:center;letter-spacing:2px;')+img(105,392,436,330,'50% 55%')+text(84,744,480,'折光',100,extra='text-align:center;letter-spacing:16px;')+text(88,869,480,'折光实验展厅 · 10:00—18:00',21,extra='text-align:center;')+text(682,258,456,'折光',122,lh=1.05,extra='letter-spacing:-8px;')+text(682,411,456,'REFRACTION',34,extra='letter-spacing:2px;')+img(792,492,346,284,'50% 53%',True)+rect(682,527,78,8,RED)+text(682,577,110,'重新\n观看。',25,lh=1.7)+line(682,819,456)+text(682,841,456,'2026.11.07—12.06',23)+text(682,885,456,'折光实验展厅 · 10:00—18:00',19)+text(1230,260,300,'01 先读主题',30)+text(1230,328,300,'标题从底部移到入口，\n中文与英文建立主次。',23,MUTED,lh=1.7)+text(1230,470,300,'02 聚合细节',30)+text(1230,538,300,'日期、时间与地点，\n在同一区域被找到。',23,MUTED,lh=1.7)+text(1230,680,300,'03 保留图像',30)+text(1230,748,300,'不在材质中心压字，\n让斜向关系继续呼吸。',23,MUTED,lh=1.7)
board('Revision.dc.html',1600,1000,'折光｜海报改稿对照',b)
if (C/'canvas.json').exists():
 idx=json.loads((C/'canvas.json').read_text());idx['title']='折光 / REFRACTION · 创作画布';idx['boards']={};idx['order']=[]
 boards=[('VisualRules.dc.html',0,0,1600,1000,'视觉规则'),('Main.dc.html',0,1120,1080,1440,'竖版海报'),('Invitation.dc.html',1160,1120,1600,900,'开幕邀请'),('Proposal01.dc.html',0,2680,1600,900,'提案01 · 展览命题'),('Proposal02.dc.html',1680,2680,1600,900,'提案02 · 观看路径'),('Proposal03.dc.html',3360,2680,1600,900,'提案03 · 跨媒介'),('Revision.dc.html',1680,0,1600,1000,'海报改稿对照')]
 for n,x,y,w,h,title in boards:idx['boards'][n]={'x':x,'y':y,'w':w,'h':h,'title':title};idx['order'].append(n)
 idx['order'].remove('Main.dc.html');idx['order'].insert(0,'Main.dc.html')
 idx['notes']={'t1':{'kind':'title1','x':0,'y':-250,'text':'折光 / 从规则到展览视觉','maxW':3280},'t2':{'kind':'title1','x':0,'y':2430,'text':'视觉提案 / 观看的三次转折','maxW':4960}}
 idx['designSystems']=[{'title':'折光 / REFRACTION','namespace':'refraction','artifact':'projects/refraction-system','version':1,'copiedAt':datetime.now(timezone.utc).isoformat()}];jwrite(C/'canvas.json',idx)
print('Restored custom tokens, 3 callable components + Cover, native snapshot, 7 editable artboard sources.')
