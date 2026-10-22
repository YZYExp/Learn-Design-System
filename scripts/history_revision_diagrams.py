from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json
R=Path(__file__).resolve().parents[1];O=R/'assets/images';F=R/'assets/fonts/NotoSansSC-Regular.ttf'
font=lambda n:ImageFont.truetype(str(F),n)
records=[]
def txt(im,xy,s,n=25,c='#262626'):ImageDraw.Draw(im).text(xy,s,font=font(n),fill=c)
def base(title,sub):
 im=Image.new('RGB',(1600,1050),'#f5f4ef');txt(im,(55,28),title,40);txt(im,(55,88),sub,23,'#555555');return im
def place(im,src,box,crop=None):
 s=Image.open(O/src).convert('RGB');s=s.crop(crop) if crop else s
 s=ImageOps.contain(s,(box[2]-box[0],box[3]-box[1]));im.paste(s,(box[0]+(box[2]-box[0]-s.width)//2,box[1]+(box[3]-box[1]-s.height)//2));return s

def save(im,name,source,changes):
 tmp=O/(name+'.tmp.png');im.save(tmp);tmp.replace(O/name);records.append({'file':name,'kind':'original_analysis','creator':'本书原创分析图','title':name,'source':source,'rights':'分析框、标签与编排为本书原创；被引用作品/裁切图的权利沿用原图说明，不声明全部开放许可。','changes':changes})
# 05: Actual, explicitly cropped specimens
im=base('05 读两种花布的底层结构','左：Daisy局部。右：Trellis局部。原作裁切，未重新绘制或生成纹样。')
place(im,'reference-morris-daisy.jpg',(65,150,775,840),(450,550,2650,2800));place(im,'revision-history-trellis.jpg',(825,150,1535,840),(180,180,2860,3100))
txt(im,(70,875),'Daisy：小花簇之间的底色，形成独立间隔。',27);txt(im,(825,875),'Trellis：格架建立骨架，枝叶跨过骨架。',27)
txt(im,(65,960),'读法：先找支撑全幅的重复关系，再看花、鸟和叶如何改变局部节奏。Met Open Access / CC0。',25)
save(im,'revision-history-analysis-05.png',['https://www.metmuseum.org/art/collection/search/384017','https://www.metmuseum.org/art/collection/search/384020'],'两原图局部裁切并列；不是接边或精确重复单元的复原。')
#06
im=base('06 茶壶的部件，并不承担相同任务','MoMA藏布兰特《Teapot》1924：左为完整照片；右为三处局部（仅裁切）。')
place(im,'revision-history-brandt.jpg',(45,145,780,935))
place(im,'revision-history-brandt.jpg',(830,150,1100,390),(580,220,1150,840));txt(im,(1130,220),'① 提梁顶部',31);txt(im,(1130,270),'深色握持部形成识别点。',23)
place(im,'revision-history-brandt.jpg',(830,425,1100,660),(250,850,1440,1240));txt(im,(1130,480),'② 壶盖与壶身',31);txt(im,(1130,530),'平面边缘对照曲面体量。',23)
place(im,'revision-history-brandt.jpg',(830,700,1100,925),(450,1060,1090,1800));txt(im,(1130,755),'③ 壶嘴与支脚',31);txt(im,(1130,805),'方向与支撑各自明确。',23)
txt(im,(60,980),'本书观察，不是制造图、热学证明或人体工学测试。摄影与作品权利见原图归属。',24)
save(im,'revision-history-analysis-06.png','https://www.moma.org/collection/works/2438','保留全图；三个实物局部裁切，无生成补绘。')
#07
im=base('07 同一海报的三层关系','Müller-Brockmann，Musica Viva，1958，MoMA 7233。框线是本书观察，不是历史网格复原。')
place(im,'revision-history-muller.jpg',(55,145,680,950))
place(im,'revision-history-muller.jpg',(760,145,1095,485),(50,1100,740,1960));txt(im,(1125,190),'① 文字块',30);txt(im,(1125,245),'倾斜方向与大形呼应。',24)
place(im,'revision-history-muller.jpg',(760,535,1095,900),(180,520,1330,1470));txt(im,(1125,580),'② 小色块',30);txt(im,(1125,635),'尺度与间隔创造节奏。',24)
d=ImageDraw.Draw(im);d.line((175,730,475,430),fill='#724e8e',width=7);txt(im,(175,940),'③ 斜向结构：一个共同方向',25,'#724e8e')
txt(im,(60,990),'请与原图对照：本作不是常见的圆环版Musica Viva；不能套用另一作品的分析。',24)
save(im,'revision-history-analysis-07.png','https://www.moma.org/collection/works/7233','全图上增加方向观察线；两处局部裁切；未假定精确网格尺寸。')
#08
im=base('08 看似破格，也有清楚的中心与支点','Sottsass，Carlton，1981。低分辨率馆方展示图；局部放大仅供形态观察。')
place(im,'revision-history-carlton.jpg',(45,145,700,940))
place(im,'revision-history-carlton.jpg',(760,170,1105,495),(60,35,430,295));txt(im,(1140,250),'上部：空框与斜向构件',25)
place(im,'revision-history-carlton.jpg',(760,555,1105,900),(40,290,445,575));txt(im,(1140,650),'下部：抽屉、支脚与底座',25)
txt(im,(65,980),'判断顺序：整体轮廓 → 承重与使用位置 → 材料表情。不是承重验算或原作结构复原。',25)
save(im,'revision-history-analysis-08.png','https://www.metmuseum.org/art/collection/search/486989','保留全图并裁切两个实际部分；不以生成图代替。©Estate of Ettore Sottsass。')
#09
im=base('09 画谱怎样让一幅画成为可学习的关系','《芥子园画传》Met CP8：原图局部裁切。箭头仅表示本书的观看建议。')
place(im,'revision-history-mustard-seed.jpg',(55,170,990,940))
place(im,'revision-history-mustard-seed.jpg',(1040,170,1540,560),(200,750,1550,1600));txt(im,(1050,585),'局部：桥、屋、树怎样互相定位',25)
d=ImageDraw.Draw(im);d.line((320,780,600,680,775,710),fill='#555f85',width=7);d.ellipse((305,765,335,795),fill='#555f85')
txt(im,(1045,680),'读图三问：',30);txt(im,(1045,735),'① 前景在哪里形成入口？',25);txt(im,(1045,785),'② 路径在哪里转折？',25);txt(im,(1045,835),'③ 题记怎样获得阅读空间？',25)
txt(im,(65,980),'这不是笔法次序复原，也不能由一张图推断全部中国画的规则。Met Open Access / CC0。',25)
save(im,'revision-history-analysis-09.png','https://www.metmuseum.org/art/collection/search/63201','全图加观察方向线；局部裁切说明小尺度对象的关系。')
#10
im=base('10 看设计稿，先分开主样、试样与标注','Anni Albers，Design for Wall Hanging，1926，MoMA 3749。实际设计稿的局部。')
place(im,'revision-history-albers.jpg',(55,150,660,950))
place(im,'revision-history-albers.jpg',(750,150,1100,590),(310,160,1130,1590));txt(im,(1135,260),'① 主图',31);txt(im,(1135,315),'横向短条组成纵向分区。',23)
place(im,'revision-history-albers.jpg',(740,635,1100,820),(280,1640,1220,1900));txt(im,(1135,670),'② 下方小样',31);txt(im,(1135,725),'尺度不同，关系仍可比较。',23)
txt(im,(750,875),'③ 手写标记留在纸边；本书不猜读其技术含义。',25)
txt(im,(60,990),'这是纸上水粉与铅笔设计稿，不是织物照片，也不是完整织造工艺图。原权利归Albers Foundation / ARS。',23)
save(im,'revision-history-analysis-10.png','https://www.moma.org/collection/works/3749','全图与主图、底部小样裁切并置；不添画织纹或误释手写字。')
p=R/'references/revision-history-images.json';r=json.loads(p.read_text());r=[x for x in r if x['kind']!='original_analysis'];p.write_text(json.dumps(r+records,ensure_ascii=False,indent=2))
print('6 analysis figures saved')
