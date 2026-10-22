#!/usr/bin/env python3
"""Collect actual native exports and compose the unmodified AI-input contact sheet."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];LAB=ROOT/'examples/creative-lab'
def rec(p,kind,**kw):
 with Image.open(p) as im:size=im.size
 return dict(file=str(p.relative_to(ROOT)),kind=kind,pixels=size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),**kw)
def main():
 records=[];log=json.loads((LAB/'shared-assets/generation-log-v5.json').read_text())
 for a in log['assets']:
  records.append(rec(LAB/'shared-assets'/a['file'],'ai_illustration',creator='本书原创AI素材',role=a.get('role'),prompt=a.get('prompt'),production_description=a.get('production_description'),prompt_record_type=a.get('prompt_record_type','verbatim prompt retained from V4 record'),provenance_log='examples/creative-lab/shared-assets/generation-log-v5.json'))
 concept=ROOT/'assets/images/refraction-concept-v5.png'
 records.append(rec(concept,'ai_illustration',creator='本书原创完整AI视觉提案',role='full_visual_proposal',source_asset='examples/creative-lab/shared-assets/refraction-concept-v5.png',provenance_log='examples/creative-lab/shared-assets/generation-log-v5.json',copy_editable=False))
 for name in ['refraction','field','still']:
  c=LAB/(name+'-canvas');d=json.loads((c/'canvas.json').read_text())
  for f in d['order']:
   if d['boards'][f].get('hidden'):continue
   stem=Path(f).stem.removesuffix('.dc');p=c/'renders/export'/(stem+'.png')
   records.append(rec(p,'original_design',title=d['boards'][f].get('title',stem),creator='本书原创：AI素材与可编辑版式联合创作',tool='Tingly Design 0.26.1021',source_canvas=str((c/f).relative_to(ROOT)),source_index=str((c/'canvas.json').relative_to(ROOT)),system=str((LAB/(name+'-system')/'design-system.json').relative_to(ROOT)),contains_ai_raster=any(a["file"] in (c/f).read_text() for a in log["assets"]),copy_editable=True))
  for p in sorted((LAB/(name+'-system')/'renders/check').glob('*.png')):records.append(rec(p,'original_design',creator='本书原创设计系统原生视图',tool='Tingly Design 0.26.1021'))
 p=LAB/'still-system/renders/export/Colors.png';records.append(rec(p,'original_design',creator='隙间原创系统的实际颜色视图',tool='Tingly Design 0.26.1021'))
 sheet=Image.new('RGB',(1800,950),'#F6F2E8');d=ImageDraw.Draw(sheet);fontfile=ROOT/'assets/fonts/NotoSansSC-Regular.ttf';font=ImageFont.truetype(str(fontfile),27);small=ImageFont.truetype(str(fontfile),20)
 for i,(f,title,sub) in enumerate([('refraction-light-v5.png','折光：纸白、蓝青与金红光场','完整提案派生 / 去字光场底图'),('field-botanical-v4.png','野序：单枝鸢尾与留白','生成素材 / 植物摄影感'),('still-coffee-v4.png','隙间：俯拍咖啡与日光','生成素材 / 品牌静物摄影感')]):
  x=35+i*600;d.text((x,32),title,font=font,fill='#292D29');d.text((x,78),sub,font=small,fill='#667069')
  with Image.open(LAB/'shared-assets'/f) as im:
   im=im.convert('RGB');im.thumbnail((550,745),Image.Resampling.LANCZOS);sheet.paste(im,(x+(550-im.width)//2,135+(745-im.height)//2))
 d.text((35,908),'三张无字素材；折光由完整AI提案派生，成品文字与布局在原生Canvas中重建。',font=small,fill='#41483F')
 p=ROOT/'assets/images/creative-inputs.png';sheet.save(p);records.append(rec(p,'ai_illustration',creator='本书AI素材联系表',processing='只缩放排版，未改绘图像'))
 (ROOT/'references/revision-creative-lab-images.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print({'records':len(records),'canvas_exports':18})
if __name__=='__main__':main()
