#!/usr/bin/env python3
"""Render the exact learning sequence from the shared book manifest."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from book_manifest import load_book,ROOT

def main():
    book=load_book(); im=Image.new('RGB',(1100,1530),'#FAF8F2');d=ImageDraw.Draw(im)
    font=lambda size:ImageFont.truetype(str(ROOT/'assets/fonts/NotoSansSC-Regular.ttf'),size)
    ink='#1C2C2B';teal='#235F59'
    d.text((68,40),'设计的语法 · 阅读路径',font=font(43),fill=ink)
    d.text((70,111),'从观察作品，到制作、检验与维护',font=font(28),fill='#68736C')
    outputs=['任务表 · 信息骨架 · 颜色角色','图像方法 · 组合规则 · 变化条件','宣传与阅读的图文安排','材料检查 · 实体样张 · 路线','时间脚本 · Token · 预约状态卡','可编辑作品 · 试读 · 变更记录']
    for i,part in enumerate(book['parts']):
        y=195+i*200;d.rounded_rectangle((65,y,1035,y+165),radius=12,fill='#EFEFE5',outline='#D1D4C7',width=2)
        d.text((88,y+20),f'{i+1:02}',font=font(46),fill=teal)
        d.text((190,y+19),part['title'],font=font(35),fill=ink)
        ns=[x['number'] for x in part['chapters']]
        d.text((192,y+76),f'第{min(ns)}—{max(ns)}章',font=font(24),fill='#68736C')
        d.text((192,y+115),outputs[i],font=font(28),fill=ink)
        if i<5:d.line((550,y+174,550,y+189),fill='#C73D29',width=5);d.polygon([(542,y+184),(558,y+184),(550,y+195)],fill='#C73D29')
    d.text((70,1428),'连续练习：岸线设计周（教学虚构）',font=font(27),fill=teal)
    d.text((70,1471),'海报 → 册页 → 导视 → 纸袋 → 手机预约',font=font(27),fill='#68736C')
    im.save(ROOT/'assets/images/book-learning-map.png')
if __name__=='__main__':main()
