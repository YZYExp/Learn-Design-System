#!/usr/bin/env python3
"""Build the public reading site from the canonical Markdown and source images."""
import argparse, hashlib, html, json, os, re, shutil, subprocess, sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
GROUPS=[('从这里开始',range(0,5)),('历史与材料',range(5,11)),('跨媒介应用',range(11,17)),('规则与协作',range(17,22)),('专题与练习',range(22,31)),('原创与当代',range(31,34))]
REPO='https://github.com/YZYExp/Learn-Design-System'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--serve',action='store_true');ap.add_argument('--site-url',default='https://yzyexp.github.io/Learn-Design-System/');a=ap.parse_args()
    docs=ROOT/'build/site-source';out=ROOT/'build/site'
    if docs.exists():shutil.rmtree(docs)
    (docs/'assets/media').mkdir(parents=True)
    images={}
    def media(p):
        p=p.resolve()
        if not p.is_relative_to(ROOT) or not p.is_file():raise ValueError('Missing/outside image: '+str(p))
        key=hashlib.sha256(p.read_bytes()).hexdigest()[:20];dest=docs/'assets/media'/(key+'.webp');cache=ROOT/'build/site-media-cache'/(key+'.webp')
        cache.parent.mkdir(parents=True,exist_ok=True)
        if cache.exists() and not dest.exists():shutil.copy2(cache,dest)
        if not dest.exists():
            with Image.open(p) as im:
                rgba=im.convert('RGBA');im=Image.new('RGB',rgba.size,'#faf8f2');im.paste(rgba,mask=rgba.getchannel('A'));im.thumbnail((1800,2400),Image.Resampling.LANCZOS);im.save(dest,'WEBP',quality=88,method=4);shutil.copy2(dest,cache)
        images[str(p.relative_to(ROOT))]=str(dest.relative_to(docs));return str(dest.relative_to(docs))
    chapters=[];nav=[{'首页':'index.md'}]
    for folder in ('chapters','appendices'):
        (docs/folder).mkdir(exist_ok=True)
        for p in sorted((ROOT/folder).glob('*.md')):
            text=p.read_text();title=next((x[2:] for x in text.splitlines() if x.startswith('# ')),p.stem)
            def image_match(m):
                target=m[2]
                if target.startswith(('https:','http:','data:')):return m[0]
                path=media(p.parent/target)
                return '!['+m[1]+']('+os.path.relpath(docs/path,docs/folder).replace(os.sep,'/')+')'
            text=re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',image_match,text)
            # Preserve local source citations as real links to the versioned repository.
            def link_match(m):
                target=m[2]
                if target.startswith(('http:','https:','#','mailto:')):return m[0]
                src=(p.parent/target.split('#')[0]).resolve()
                if src.is_relative_to(ROOT) and src.is_file() and (src.suffix!='.md' or src.parent.name not in ('chapters','appendices')):return '['+m[1]+']('+REPO+'/blob/main/'+str(src.relative_to(ROOT))+')'
                return m[0]
            text=re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)',link_match,text)
            (docs/folder/p.name).write_text(text)
            chapters.append({'title':title,'file':folder+'/'+p.name,'number':int(p.name[:2]) if folder=='chapters' else None})
    for group,nums in GROUPS:nav.append({group:[{c['title']:c['file']} for c in chapters if c['number'] in nums]})
    nav.append({'附录':[{c['title']:c['file']} for c in chapters if c['number'] is None]})
    cfile=lambda n:next(c['file'] for c in chapters if c['number']==n)
    hero=media(ROOT/'examples/creative-lab/refraction-canvas/renders/export/Main.png')
    field=media(ROOT/'examples/creative-lab/field-canvas/renders/export/Main.png')
    still=media(ROOT/'examples/creative-lab/still-canvas/renders/export/Packaging.png')
    home='''---\nhide:\n  - navigation\n  - toc\n---\n<div class="book-home">
<section class="book-hero"><div class="hero-copy"><p class="eyebrow">THE GRAMMAR OF DESIGN · 图解设计读本</p><h1>看见秩序。<br>读懂设计。</h1><p class="hero-lead">从一张海报、一页画报，到一个品牌与一套设计系统。<br>在真实作品里学会观察，再把自己的判断变成作品。</p><div class="hero-actions"><a class="button primary" href="INTRO">从导读开始 <span aria-hidden="true">↗</span></a><a class="text-link" href="#reading-map">浏览全书目录 <span aria-hidden="true">↓</span></a></div><div class="hero-facts"><span><b>33</b> 个正文章</span><span><b>178</b> 张独立配图</span><span><b>3</b> 套原创系统</span></div></div><figure class="hero-art"><a href="LAB" aria-label="阅读折光的完整视觉提案与原生重建"><img src="HERO" alt="折光V5：纸白上的蓝金光场与宋体中文海报" width="1080" height="1440" fetchpriority="high"></a><figcaption><span>01 / 折光 · REFRACTION</span><span>从完整提案，到可编辑画板</span></figcaption></figure></section>
<section class="home-intro"><p class="eyebrow">先学会看，再学会做</p><h2>“好看”之后，<br>还有很多可以说清楚的事。</h2><p>谁先吸引注意？什么让一组作品成为一家？同一种视觉语言，怎样进入海报、包装、空间与屏幕？这本书把艺术、美术与设计放在一起，从具体作品讲清关系，也走进 Token、组件与协作。</p></section>
<section class="home-routes" id="choose-a-route"><div class="section-heading"><p class="eyebrow">CHOOSE YOUR PATH</p><h2>从你感兴趣的地方开始。</h2></div>ROUTES</section>
<section class="home-studio"><div class="section-heading"><p class="eyebrow">THE MAKING OF A SYSTEM</p><h2>让规则，真的长出作品。</h2><p>完整 AI 提案、无字素材与原生画板各有职责。三套教学项目，把视觉选择带进真实的版式与可编辑工程。</p></div><div class="studio-gallery"><a class="studio-work" href="LAB"><figure><img src="HERO" alt="折光展览海报" loading="lazy" width="1080" height="1440"></figure><span class="work-index">01 / 展览与提案</span><h3>折光</h3><p>宋体、纸白与蓝金光场，重排为海报、邀请和提案。</p></a><a class="studio-work" href="LAB#313"><figure><img src="FIELD" alt="野序紫鸢尾画报封面" loading="lazy" width="1080" height="1440"></figure><span class="work-index">02 / 画报与编辑</span><h3>野序</h3><p>单枝影像如何成为封面、跨页与连续阅读的节奏。</p></a><a class="studio-work" href="LAB#314"><figure><img src="STILL" alt="隙间咖啡三种包装的可编辑设计" loading="lazy" width="1800" height="1200"></figure><span class="work-index">03 / 品牌与包装</span><h3>隙间</h3><p>让识别、风味、规格与行动，出现在合适的位置。</p></a></div><a class="text-link" href="LAB">走进原创工坊 <span aria-hidden="true">↗</span></a></section>
<section class="home-now"><p class="eyebrow">DESIGN IN THE PRESENT</p><div><h2>经典之外，<br>也去当代现场看看。</h2><p>Pepsi、Reddit、Wise、Spotify Mix、Config 与 Decathlon：六组 2023—2025 年的真实品牌项目，细看字体、广告、界面、包装与空间之间的联系。</p><a class="text-link" href="NOW">阅读六个真实品牌案例 <span aria-hidden="true">↗</span></a></div><p class="brand-list" aria-label="案例品牌">PEPSI / REDDIT / WISE<br>SPOTIFY MIX / CONFIG<br>DECATHLON</p></section>
<section class="home-catalog" id="reading-map"><div class="section-heading"><p class="eyebrow">CONTENTS / 全书阅读地图</p><h2>循序读，也可以跳着读。</h2><p>基础观察 → 历史与材料 → 跨媒介应用 → 规则实现 → 创作实践。每章保留配图、图注与就近来源，可通过顶部搜索查找主题。</p></div>CATALOG</section>
<footer class="home-notes"><p>写给非专业的设计爱好者。真实案例、原创分析、教学示意与 AI 图像在正文中分别标注；工坊项目为教学虚构。</p><a href="REPO">查看书稿与可编辑工程 ↗</a></footer></div>
'''
    routes=[(2,'学会观察','构图、色彩与网格：把“有设计感”说得更具体。','01—04'),(5,'看懂历史与材料','装饰、现代主义、东亚视觉与工艺的不同选择。','05—10'),(25,'走进具体媒介','海报、广告、演示、画报与包装，逐页观察和改稿。','25—29'),(19,'理解系统如何实现','从视觉角色到 Token、组件与协作中的规则。','17—21'),(31,'亲手长出作品','三套原创项目，混合 AI 图像与可编辑设计。','30—31'),(32,'去当代现场','六个真实品牌，观察同一语言如何随媒介变化。','32—33')]
    route_html=''.join(f'<a class="route" href="{cfile(n)}"><span class="route-number">{i:02}</span><h3>{title}</h3><p>{desc}</p><span class="route-chapters">{nums} <b aria-hidden="true">↗</b></span></a>' for i,(n,title,desc,nums) in enumerate(routes,1))
    catalog=''
    for i,(group,nums) in enumerate(GROUPS):
        links=''.join(f'<li><a href="{c["file"]}"><span>{c["number"]:02}</span>{html.escape(c["title"].split("｜",1)[-1])}<b aria-hidden="true">↗</b></a></li>' for c in chapters if c['number'] in nums)
        catalog+=f'<details {"open" if i==0 else ""}><summary>{group}<span>{len([c for c in chapters if c["number"] in nums])} 章</span></summary><ol>{links}</ol></details>'
    catalog+='<details><summary>附录<span>3 篇</span></summary><ol>'+''.join(f'<li><a href="{c["file"]}">{html.escape(c["title"])}<b aria-hidden="true">↗</b></a></li>' for c in chapters if c['number'] is None)+'</ol></details>'
    for key,value in {'INTRO':cfile(0),'LAB':cfile(31),'NOW':cfile(32),'HERO':hero,'FIELD':field,'STILL':still,'ROUTES':route_html,'CATALOG':catalog,'REPO':REPO}.items():home=home.replace(key,value)
    home=re.sub(r'href="((?:chapters|appendices)/[^"]+)\.md(?=[#"])',r'href="\1/',home)
    (docs/'index.md').write_text(home)
    shutil.copytree(ROOT/'website',docs/'assets/site',dirs_exist_ok=True)
    config={'site_name':'设计的语法','site_description':'从艺术秩序到设计系统：一部面向非专业读者的中文图解设计读本。','site_url':a.site_url,'repo_url':REPO,'repo_name':'源文件与工程','docs_dir':str(docs),'site_dir':str(out),'use_directory_urls':True,'theme':{'name':'material','language':'zh','font':False,'palette':[{'scheme':'default','primary':'custom','accent':'custom'}],'features':['navigation.sections','navigation.top','navigation.footer','search.suggest','search.highlight','content.code.copy','toc.follow']},'plugins':[{'search':{'lang':['zh','en']}}],'markdown_extensions':['tables','fenced_code','footnotes','toc','attr_list','md_in_html','admonition','pymdownx.highlight','pymdownx.superfences'],'extra_css':['assets/site/site.css'],'extra_javascript':['assets/site/reader.js'],'nav':nav,'copyright':'设计的语法 · 真实案例与图像权利归原作者；原创工坊为教学虚构。'}
    cfg=ROOT/'build/mkdocs.yml';cfg.write_text(json.dumps(config,ensure_ascii=False,indent=2))
    subprocess.run([sys.executable,'-m','mkdocs','serve' if a.serve else 'build','-f',str(cfg)],check=True)
    (ROOT/'build/site-build-report.json').write_text(json.dumps({'pages':len(chapters)+1,'chapters':len(chapters),'images':images,'site_url':a.site_url},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
