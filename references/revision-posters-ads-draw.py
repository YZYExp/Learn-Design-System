from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,json
BASE=Path(__file__).resolve().parents[1];OUT=BASE/'assets/images';FONT=BASE/'assets/fonts/NotoSansSC-Regular.ttf'
F=lambda n:ImageFont.truetype(str(FONT),n)
INK='#202938';PAPER='#f8f5ee'
def new(title,sub,palette):
 im=Image.new('RGB',(1600,1000),PAPER);d=ImageDraw.Draw(im);d.text((60,35),title,font=F(43),fill=palette[0]);d.text((60,100),sub,font=F(23),fill=INK);return im,d
def text(d,xy,s,size=25,fill=INK):
 x,y=xy
 for line in s.split('\n'):d.text((x,y),line,font=F(size),fill=fill);y+=size*1.5

def arrow(d,a,b,color,width=8):
 d.line((a,b),fill=color,width=width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);r=22;pts=[b,(b[0]-r*math.cos(ang-.5),b[1]-r*math.sin(ang-.5)),(b[0]-r*math.cos(ang+.5),b[1]-r*math.sin(ang+.5))];d.polygon(pts,fill=color)

def save(im,name):im.save(OUT/name)
# Lautrec: three overlapping depth planes; not an imitation of his drawing
im,d=new('劳特累克：遮挡把观众带进场内','原创结构分析｜依据原作位置概括层次，不是历史作品重绘',('#9b3525','#e8b93e'))
d.rectangle((75,180,600,930),fill='#f0cf5b',outline=INK,width=3)
text(d,(95,200),'场所名 × 3',40,'#a33328');text(d,(95,270),'演出类型 / 舞者名',24)
d.rectangle((90,360,585,475),fill='#26221d');text(d,(120,390),'后层：观众轮廓',27,'white')
d.polygon([(240,425),(310,420),(435,630),(145,665)],fill='#fff8dd',outline=INK);text(d,(205,530),'中层\n舞者亮部',26)
d.polygon([(440,470),(530,435),(560,840),(360,900),(340,695)],fill='#8c8a73');text(d,(390,710),'前层\n裁切人物',25)
text(d,(720,210),'① 先记住谁在什么地方演出\n红字与黄地建立远距离对比。',31)
text(d,(720,365),'② 看遮挡，而非数人物\n后排黑带衬出白裙，前景灰形又压上来。',29)
text(d,(720,535),'③ 字也可进入舞池\n下方文字跨过形体，但不能挡住主要动作。',29)
text(d,(720,735),'迁移练习：只保留黑、灰、白三层。\n若仍能分出主角与旁观者，层次才成立。',28)
arrow(d,(650,420),(570,420),'#9b3525');arrow(d,(650,600),(400,600),'#9b3525');save(im,'revision-posters-moulin-analysis.png')
# Gismonda: architecture of reading
im,d=new('穆夏：长窄幅怎样组织慢阅读','原创结构分析｜上部题名、弧形姓名、竖向人物与底部剧院',('#6d5d82','#d2ba73'))
d.rectangle((100,175,410,935),fill='#eadfc6',outline='#8b784d',width=5)
d.rectangle((120,190,390,265),outline='#505774',width=3);text(d,(135,205),'剧目名',34,'#505774')
d.arc((120,260,390,470),180,360,fill='#8b784d',width=17);text(d,(155,315),'演员姓名',24)
d.ellipse((230,375,285,430),fill='#b3919e');d.polygon([(230,430),(290,430),(335,810),(165,810)],fill='#b9bca2');d.line((185,380,155,720),fill='#749074',width=9)
d.rectangle((120,845,390,920),outline='#505774',width=3);text(d,(139,860),'剧院 / 去处',27)
for y,s in [(230,'题名是一道横向门槛'),(350,'弧形文字包住头部：文字与人物成一体'),(610,'人物占据纵轴：长幅不是把方图拉长'),(875,'到达底端后得到剧院信息')]:arrow(d,(470,y),(415,y),'#6d5d82');text(d,(520,y-20),s,30)
text(d,(520,670),'比例实验\n同样的人物若塞进横幅，\n必须裁切、缩小或重排文字。\n不能只做等比缩放。',28)
save(im,'revision-posters-gismonda-analysis.png')
# Cassandre: perspective and text frame
im,d=new('卡桑德：用透视把列车变成力量','原创结构分析｜图像给出速度感，边缘文字提供线路信息',('#1e466c','#c4452e'))
d.rectangle((80,180,620,930),fill='#ded5b5',outline='#504e43',width=4);d.rectangle((110,210,590,890),fill='#183b61')
text(d,(130,235),'NORD',68,'#e5d5a8');text(d,(170,315),'EXPRESS',47,'#e5d5a8')
vp=(540,540)
for a in [(120,420),(110,600),(140,850),(560,850)]:d.line((a,vp),fill='#e3d6b4',width=8)
d.polygon([(120,450),(540,540),(520,610),(110,595)],fill='#26252a');d.ellipse((390,660,510,800),fill='#27272b',outline='#dfd3ae',width=4)
text(d,(100,900),'城市名 / 铁路机构',23)
text(d,(730,205),'① 顶部大字先给“名字”\n并不要求先看懂机车全部结构。',31)
text(d,(730,370),'② 斜线汇聚制造方向张力\n低视点、近大远小、机械重复互相配合。',29)
text(d,(730,540),'③ 边框不是随意装饰\n城市与运营信息被放到外围，\n避免与机车主体争夺中心。',29)
text(d,(730,760),'反事实：若把机车改成平视小图，\n名字仍可读，但旅行的力量隐喻会减弱。',28)
arrow(d,(680,600),(535,555),'#c4452e');save(im,'revision-posters-nord-analysis.png')
# ads JOB hierarchy
im,d=new('JOB：品牌符号怎样进入装饰图案','原创结构分析｜分析的是欲望和记忆的建构，不是产品性能证据',('#75512e','#173f39'))
d.rectangle((80,180,620,930),fill='#d5bd8f',outline='#714e2c',width=6)
for x in range(105,600,90):
 for y in range(210,900,110):d.text((x,y),'JOB',font=F(30),fill='#9e9e70')
text(d,(110,205),'JOB',108,'#63462e')
d.ellipse((215,350,470,610),fill='#24222a');d.ellipse((280,390,380,505),fill='#dcae92');d.polygon([(260,510),(420,510),(510,875),(170,875)],fill='#c5816b');d.line((255,430,190,370),fill='#f4e3bd',width=8)
text(d,(750,215),'上部大字 + 底纹重复\n两种尺度把品牌嵌入画面。',31)
text(d,(750,390),'头发曲线与烟的曲线\n把注意力带回人物的手、脸和商品关系。',29)
text(d,(750,570),'受众的想象\n购买动作被包裹为一种姿态与生活方式。',29)
text(d,(750,755),'检查：装饰能否帮人记住品牌？\n若换个品牌仍完全相同，可能只是漂亮。',28)
arrow(d,(690,270),(585,270),'#173f39');save(im,'revision-ads-job-analysis.png')
# Coca material placement
im,d=new('早期可口可乐：从身份场景走向价格','原创结构分析｜人物、饮用动作、品牌价签各有不同任务',('#653645','#bd9b49'))
d.rectangle((90,180,630,930),fill='#553645',outline=INK,width=4);d.ellipse((200,250,490,440),fill='#ddd7ae');d.ellipse((260,420,420,580),fill='#dabf9a');d.polygon([(250,550),(430,550),(555,890),(135,890)],fill='#7b8e6a')
d.rectangle((140,760,600,900),fill='#e0d5b6');d.ellipse((430,640,590,840),fill='#cccf9f',outline='#e6d06d',width=7);text(d,(452,690),'品牌',33,'#a33e30');text(d,(463,745),'5¢',43,'#a33e30');d.rectangle((200,580,260,665),outline='#f4e2c1',width=4)
text(d,(740,215),'① 人脸：产生观看入口\n衣帽、花饰、珠饰共同暗示特定身份。',30)
text(d,(740,390),'② 举杯：连接人与产品\n商品不是凭空浮在角落的徽章。',30)
text(d,(740,565),'③ 品牌与价格：给出消费线索\n5美分把抽象场景连到具体交易。',30)
text(d,(740,760),'批判阅读：谁被当作“理想顾客”？\n优雅场景不是健康、安全或普适性的证明。',28)
arrow(d,(690,760),(585,755),'#bd9b49');save(im,'revision-ads-coca-analysis.png')
# VW negative space
im,d=new('Think Small：留白本身就是论点','原创结构分析｜空间反差先引起疑问，标题与正文负责解释',('#1e2d37','#3c6a87'))
d.rectangle((100,180,650,930),fill='white',outline='#777',width=2)
d.rounded_rectangle((250,350,340,390),radius=20,fill='#242b30');d.ellipse((255,382,280,405),fill='#111');d.ellipse((310,382,335,405),fill='#111')
text(d,(265,740),'Think small.',28)
for col in range(3):
 for line in range(10):d.line((145+col*155,805+line*7,270+col*155,805+line*7),fill='#6f777c',width=2)
text(d,(760,210),'图像不是最大，却最孤立\n大片空白使小车成为一个“异常”。',30)
text(d,(760,390),'标题不是另起话题\n两个词为上方的大小反差命名。',30)
text(d,(760,565),'正文不是填满剩余空间\n把小车的特征转成日常使用的理由。',30)
text(d,(760,755),'不能照搬的部分\n陌生产品、短停留触点或无证据的主张，\n可能根本撑不起这样少的信息。',28)
arrow(d,(700,380),(350,380),'#3c6a87');save(im,'revision-ads-think-small-analysis.png')
# Poster before-after iteration
im,d=new('海报改稿：改变阅读顺序，不只是换配色','原创教学样本｜虚构“城市夜行摄影展”，示例信息不指向实际活动',('#325b68','#dc693c'))
for x,label in [(60,'A  平均用力'),(810,'B  明确主次')]:d.rectangle((x,180,x+700,920),fill='#e8ece9',outline='#809393',width=3);text(d,(x+25,205),label,30)
for y,s in [(320,'城市夜行摄影展'),(420,'把城市看成光的地图'),(520,'周六 19:00'),(620,'岸线展厅  免费预约'),(720,'三位摄影师联展')]:text(d,(85,y),s,36,'#325b68')
text(d,(845,295),'城市夜行',76,'#18333b');text(d,(845,395),'摄影展',54,'#18333b');d.rectangle((845,490,1460,650),fill='#18333b')
for x in [880,980,1110,1290,1390]:d.rectangle((x,520,x+25,630),fill='#edba63')
text(d,(845,690),'周六 19:00  ·  岸线展厅',35,'#18333b');d.rounded_rectangle((845,780,1245,855),radius=10,fill='#dc693c');text(d,(870,794),'免费预约  →  示例入口',28,'white')
save(im,'revision-posters-redesign.png')
# Ad before-after with evidence
im,d=new('广告改稿：从口号走到可检查的理由','原创教学样本｜虚构修理服务；价格、场次均为练习设定',('#594a83','#c65e3a'))
for x,label in [(60,'A  情绪很多，行动很少'),(810,'B  主张、证据、下一步')]:d.rectangle((x,180,x+700,930),fill='#f0ebdf',outline='#b4a7c2',width=3);text(d,(x+25,205),label,29)
text(d,(100,325),'焕新生活\n匠心修复\n给你最好的陪伴',55,'#796a91');text(d,(100,650),'专业 · 优质 · 可靠 · 超值',31);d.ellipse((220,750,570,890),fill='#bdb0c9')
text(d,(850,310),'舍不得丢的台灯，\n先看看能不能修。',48,'#3c315a');d.ellipse((900,520,1110,570),fill='#bf9f57');d.line((1005,570,1005,690),fill='#6a6265',width=15);d.ellipse((930,690,1080,720),fill='#6a6265')
text(d,(1140,520),'现场检测\n先报价再维修\n练习设定：检测免费',28)
d.rectangle((850,765,1450,870),fill='#594a83');text(d,(875,780),'周六 14:00—17:00\n查看维修范围并预约 → 示例入口',28,'white')
save(im,'revision-ads-redesign.png')
print('8 analysis images generated')
