"""Build labelled reading plates from the cited reference images; never recolor artworks."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,fitz
R=Path(__file__).resolve().parents[1];D=R/'assets/images';F=R/'assets/fonts/NotoSansSC-Regular.ttf'
font=lambda n:ImageFont.truetype(str(F),n)
def canvas(title,h=1000):
 im=Image.new('RGB',(1800,h),'white');d=ImageDraw.Draw(im);d.text((45,24),title,font=font(44),fill='#222222');return im,d
def text(d,xy,t,n=27,c='#222222'):d.text(xy,t,font=font(n),fill=c)
def place(im,f,box,crop=None,bg='white'):
 q=Image.open(D/f).convert('RGBA');q=q.crop(crop) if crop else q;q.thumbnail((box[2]-box[0],box[3]-box[1]));b=Image.new('RGBA',q.size,bg);b.alpha_composite(q);x=box[0]+(box[2]-box[0]-q.width)//2;y=box[1]+(box[3]-box[1]-q.height)//2;im.paste(b.convert('RGB'),(x,y));return (x,y,q.width,q.height)
meta=[]
def save(im,name,sources):
 tmp=D/(name+'.tmp');im.save(tmp,format='PNG');tmp.replace(D/name);meta.append(dict(file='assets/images/'+name,filename=name,kind='original_analysis',title=name,creator='本书编辑：原作局部研究标注',date='2026-10-21',source_files=sources,rights='标注与版式为本书原创；原图版权沿用对应来源条目，不据此获得作品再许可',use='书内研究评论'))
im,d=canvas('17  看清变化发生在哪里：Molnár 1985',1000)
place(im,'revision-digital-molnar.jpg',(40,105,885,750));
place(im,'revision-digital-molnar.jpg',(930,120,1750,360),(95,70,1160,175));text(d,(940,370),'A 上沿：逐个矩形的小幅高低变化')
place(im,'revision-digital-molnar.jpg',(930,445,1750,735),(95,380,1170,520));text(d,(940,750),'B 交接带：密集横边使局部聚成一条带')
text(d,(45,850),'原作保留红线、白纸与两组竖矩形；分析聚焦位置与密度。',30)
text(d,(45,910),'局部裁切为研究引图。不是原作算法复原，不能从照片反推随机参数。',26)
save(im,'revision-digital-analysis-molnar.png',['revision-digital-molnar.jpg'])
im,d=canvas('19  同一行动角色，两组实际前景／背景',880)
for x,fn,bg,label in [(50,'revision-digital-material-light.png','#fffbfe','浅色主题的官方按钮样图'),(930,'revision-digital-material-dark.png','#1c1b1f','深色主题的官方按钮样图')]:
 d.rectangle((x,125,x+820,570),fill=bg);place(im,fn,(x+75,240,x+745,460),bg=bg);text(d,(x,605),label,30)
text(d,(50,700),'观察：填充色的明暗顺序与文字明暗一起改变。',32)
text(d,(50,765),'按官方PNG原样并置；页面背景为本书教学补配。不要从压缩截图提取正式Token。',26)
save(im,'revision-digital-analysis-roles.png',['revision-digital-material-light.png','revision-digital-material-dark.png'])
doc=fitz.open(R/'build/revision-digital/gov-report.pdf');p=doc[12]
# Select the official figure only, leave the uncropped page separately available.
rect=fitz.Rect(58,184,475,370);detail=D/'revision-digital-gov-error-detail.png';tmp=detail.with_name(detail.stem+'.tmp.png');p.get_pixmap(matrix=fitz.Matrix(3,3),clip=rect).save(tmp);tmp.replace(detail)
im,d=canvas('20  错误摘要：三个有位置的视觉线索',900)
place(im,'revision-digital-gov-error-detail.png',(35,110,1280,775));
text(d,(1320,180),'1 红边界',32);text(d,(1320,235),'圈定整体问题区',27)
text(d,(1320,355),'2 下划线链接',32);text(d,(1320,410),'每条指向待改字段',27)
text(d,(1320,530),'3 黄色焦点',32);text(d,(1320,585),'标明当前键盘位置',27)
text(d,(45,815),'原始页面：英国教育部2024年指引第13页图17。局部放大，未改页面颜色。',26)
save(im,'revision-digital-analysis-errors.png',['revision-digital-gov-page13.png','revision-digital-gov-error-detail.png'])
im,d=canvas('23  类型学的比较单位：先保持整幅，再读局部',1100)
place(im,'revision-digital-becher.jpg',(30,100,780,1030));
place(im,'revision-digital-becher.jpg',(850,120,1760,510),(0,0,1553,665));text(d,(860,535),'第一行局部：罐体轮廓与支承方式不同',30)
text(d,(860,675),'读图顺序',34);text(d,(860,740),'整幅：三列三行的重复间距',29);text(d,(860,800),'单幅：主体占比、正面与地面位置',29);text(d,(860,860),'跨幅：罐体、支柱、开口的变化',29)
text(d,(860,960),'局部放大未重排原作。',26);text(d,(860,1005),'© Becher遗产管理方；图片来源MoMA。',25)
save(im,'revision-digital-analysis-becher.png',['revision-digital-becher.jpg'])
im,d=canvas('24  Vionnet 1922：三种不同的体积与边界',1100)
place(im,'revision-digital-vionnet.jpg',(30,110,650,1035));
place(im,'revision-digital-vionnet.jpg',(700,110,1210,600),(410,500,900,1070));text(d,(710,625),'A 背部蝴蝶结：体积集中',27)
place(im,'revision-digital-vionnet.jpg',(1260,110,1765,600),(385,345,815,785));text(d,(1270,625),'B 袖部薄纱：透明与花饰',27)
place(im,'revision-digital-vionnet.jpg',(720,705,1740,990),(440,1470,1516,2000));
text(d,(740,1020),'C 拖裾：重力把长度展开成地面的轮廓',27)
save(im,'revision-digital-analysis-vionnet.png',['revision-digital-vionnet.jpg'])
p=R/'references/revision-digital-images.json';a=[m for m in json.loads(p.read_text()) if m.get('kind')!='original_analysis' and m.get('filename')!='revision-digital-gov-error-detail.png']
for m in a:
 m['filename']=Path(m['file']).name;m['kind']='real_artwork'
 if 'ibm-' in m['filename']:m['download_url']=m['download_url'].replace('https://www.ibm.com','https://design-language-website.netlify.app')
 if 'gov-' in m['filename']:m['rights']='© Crown copyright 2024；PDF第22页：Open Government Licence v3.0，第三方例外从其声明'
a.append(dict(file='assets/images/revision-digital-gov-error-detail.png',filename='revision-digital-gov-error-detail.png',kind='real_artwork',title='英国教育部指引第13页图17，局部截取',creator='UK Department for Education',date='2024',source_url='https://assets.publishing.service.gov.uk/media/66e447b50d913026165c3e9b/Recommended_method_of_submission_guidance.pdf',rights='© Crown copyright 2024；OGL v3.0，第三方例外从其声明',use='研究引图，PDF同页局部放大'))
a.extend(meta);p.write_text(json.dumps(a,ensure_ascii=False,indent=2));print('saved',len(meta),'analytical plates;',len(a),'manifest entries')
