#!/usr/bin/env python3
"""Regenerate five chapter 11–16 teaching analysis PNGs.

Run from any directory with Python 3 and Pillow installed::

    python3 scripts/render_revision_applications.py

Inputs are the downloaded original images under assets/images and the bundled
assets/fonts/NotoSansSC-Regular.ttf. Rights and source URLs are recorded in
references/revision-applications-images.json. This script changes only the five
revision-applications-analysis-*.png outputs; it never downloads, normalizes,
or rewrites the original artwork files.

The composition, labels, coordinates and crop are the executed production
logic. PNG byte identity can vary with Pillow, FreeType or compression-library
versions; the same source images and font reproduce the intended layout.
"""

from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'assets/images'
fontpath = ROOT / 'assets/fonts/NotoSansSC-Regular.ttf'
F=lambda n:ImageFont.truetype(str(fontpath),n)
def load(name,size):
 im=Image.open(p/('revision-applications-'+name)).convert('RGB'); im.thumbnail(size);return im

def main():
    # 11 linked form between master identity and real research group application
    im=Image.new('RGB',(1200,620),'#f4f2eb');d=ImageDraw.Draw(im);d.text((30,18),'观察关系，而不是给所有标志套同一轮廓',font=F(30),fill='#222')
    for x,name in [(30,'mit-03.jpg'),(620,'mit-07.jpg')]:
     a=load(name,(550,360));im.paste(a,(x,80));d.rectangle((x,80,x+a.width,80+a.height),outline='#bbb',width=2)
    d.text((30,460),'A  实验室：几何字母 + 名称',font=F(27),fill='#222');d.text((620,460),'B  研究组：字词 + 同源几何符号',font=F(27),fill='#222')
    d.text((30,520),'先保留名称的可读性，再在有限区域表达家族关系。',font=F(26),fill='#444');d.text((30,570),'原作品：Pentagram，MIT Media Lab，2014；本页为教学重组。',font=F(20),fill='#555');im.save(p/'revision-applications-analysis-brand.png')
    #12 original covers top then cropped text band enlarged
    im=Image.new('RGB',(1200,900),'#f6f1e4');d=ImageDraw.Draw(im);d.text((30,18),'1963：同一阅读入口，容纳不同图像',font=F(31),fill='#222')
    a=Image.open(p/'revision-applications-penguin-1963.png').convert('RGB').resize((1100,558),Image.Resampling.LANCZOS);im.paste(a,(50,70));sy=a.height/365;sx=a.width/719
    for yy,col in [(31,'#1b617d'),(78,'#c04f00')]:
     y=70+int(yy*sy);d.line((50,y,1150,y),fill=col,width=4)
    d.text((45,665),'蓝线：系列名与价格所在的页眉带',font=F(29),fill='#1b617d');d.text((45,720),'橙线：作者与书名进入图像的交界',font=F(29),fill='#a84400');d.text((45,775),'对照右侧书名：图像对比强时，文字需要重新判断。',font=F(26),fill='#222');d.text((45,840),'原封面：Penguin；1963年采用Marber网格；标线为本书分析。',font=F(20),fill='#555');im.save(p/'revision-applications-analysis-editorial.png')
    #14 crop and explicit interface separation
    im=Image.new('RGB',(1200,860),'#fafafa');d=ImageDraw.Draw(im);d.text((30,18),'606：把视线从“白色极简”移到连接关系',font=F(30),fill='#222')
    a=load('vitsoe-kitchen.jpg',(1140,642));im.paste(a,(30,70));
    for n,pt in [(1,(400,250)),(2,(710,270)),(3,(520,620))]:
     x,y=pt;d.ellipse((x-20,y-20,x+20,y+20),fill='#252525',outline='white',width=3);d.text((x-9,y-18),str(n),font=F(27),fill='white')
    d.text((30,735),'1 竖向轨道    2 开放与封闭收纳    3 桌面接入同一结构',font=F(25),fill='#222');d.text((30,800),'原产品：Dieter Rams，606，1960；Vitsœ实景摄影，标记为本书添加。',font=F(20),fill='#555');im.save(p/'revision-applications-analysis-product.png')
    #15 same house compare outside & threshold in two panels
    im=Image.new('RGB',(1200,800),'#ece8dd');d=ImageDraw.Draw(im);d.text((30,18),'Eames House：外立面的秩序，进入之后的层次',font=F(30),fill='#222')
    for x,name in [(30,'eames-exterior.jpg'),(615,'eames-entry.jpg')]:
     a=load(name,(555,500));im.paste(a,(x,80));
    d.text((30,605),'A  外观：钢框、面板、树木的前后关系',font=F(24),fill='#222');d.text((615,605),'B  入口：反射、帘幕与室内并置',font=F(24),fill='#222')
    d.text((30,670),'迁移的是结构与场地的协商，不是复制红黄蓝色块。',font=F(27),fill='#222');d.text((30,745),'原建筑：Charles & Ray Eames，1949；Eames Foundation现场照片；本书重组。',font=F(19),fill='#555');im.save(p/'revision-applications-analysis-space.png')
    #16 centre crop and full view; no invented film frames
    im=Image.new('RGB',(1200,950),'#f3f0e9');d=ImageDraw.Draw(im);d.text((30,18),'《金臂人》：整体色块与中央符号的两层尺度',font=F(30),fill='#222')
    a=load('bass-poster.jpg',(480,785));im.paste(a,(30,90))
    orig=Image.open(p/'revision-applications-bass-poster.jpg').convert('RGB'); crop=orig.crop((250,420,1110,1230));crop.thumbnail((590,570));im.paste(crop,(580,120))
    d.rectangle((570,110,1180,700),outline='#38566b',width=3);d.text((580,730),'局部：黑色手臂打破文字的安静矩形',font=F(25),fill='#222');d.text((580,785),'裁切只放大细节，不是另一张原海报。',font=F(24),fill='#222');d.text((30,905),'Saul Bass，1955，MoMA藏；右侧为本书教学裁切，左侧保留整幅。',font=F(20),fill='#555');im.save(p/'revision-applications-analysis-motion.png')


if __name__ == "__main__":
    main()
