#!/usr/bin/env python3
"""A contact sheet of actual native exports; never generates artwork."""
from pathlib import Path
import argparse,os
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];LAB=ROOT/'examples/creative-lab'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'build/creative-gallery.png');a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True)
 im=Image.new('RGB',(1800,1120),'#F3F0E8');d=ImageDraw.Draw(im)
 def font(n):return ImageFont.truetype(str(ROOT/'assets/fonts/NotoSansSC-Regular.ttf'),n)
 d.text((42,29),'从 AI 素材到可编辑作品',font=font(46),fill='#202521');d.text((44,99),'三套原创设计系统 / Tingly Design 原生 Canvas 实际导出',font=font(24),fill='#526057')
 for folder,f,(x,y,w,h) in [('refraction-canvas','Main.png',(42,209,550,733)),('field-canvas','Main.png',(625,209,550,733)),('still-canvas','Campaign.png',(1208,209,550,310)),('still-canvas','Packaging.png',(1208,550,550,361))]:
  with Image.open(LAB/folder/'renders/export'/f) as p:
   p=p.convert('RGB');p.thumbnail((w,h),Image.Resampling.LANCZOS);im.paste(p,(x+(w-p.width)//2,y+(h-p.height)//2))
 for x,title,desc in [(42,'折光 / REFRACTION','展览海报、邀请与三页提案'),(625,'野序 / FIELD NOTES','画报封面、跨页与花展广告'),(1208,'隙间 / STILL','品牌广告、包装与订阅原型')]:
  d.text((x,163),title,font=font(25),fill='#202521');d.text((x,976),desc,font=font(24),fill='#526057')
 d.line((42,1038,1758,1038),fill='#C8C5B7',width=1);d.text((42,1060),'AI 生成主视觉；文字、版式、组件与系统为原生可编辑源文件。品牌及项目均为教学虚构。',font=font(22),fill='#526057');temp=a.output.with_suffix('.pending.png');im.save(temp,format='PNG')
 with Image.open(temp) as verify:verify.verify()
 os.replace(temp,a.output);print(a.output)
if __name__=='__main__':main()
