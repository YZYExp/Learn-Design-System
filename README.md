# 设计的语法

## 从艺术秩序到设计系统 · 5.1 全文校订版

面向非专业读者的中文图解设计读本。全书包含导读、33个正文章和3篇附录，从构图、色彩、字体与材料出发，介绍品牌、海报、广告、PPT、画报、包装、产品与空间设计，再进入生成方法、Token、组件和协作维护。

本版逐章校订正文，减少口水话、机械设问、重复提醒与口号式结语，保留真实案例、设计分析和可操作练习。修订标准见 [全文校订标准](docs/editorial-standards.md)。配图仍为187次使用、178张独立图像，包含真实作品、原创分析、教学图、原创设计和明确标注的AI图像。

[在线阅读](https://yzyexp.github.io/Learn-Design-System/) · [分章书稿](chapters/) · [附录](appendices/) · [当前插图页码](references/current-artwork-page-index.md) · [素材与引用](references/)

![折光V5：海报与邀请的原生画板](examples/creative-lab/refraction-canvas/renders/export/Proposal03.png)

## 阅读路线

| 部分 | 章节 | 内容 |
| --- | --- | --- |
| 基础观察 | 00—04 | 阅读方法、视觉关系、色彩、字体与网格 |
| 历史与材料 | 05—10 | 装饰、包豪斯、现代主义、后现代、东亚视觉与工艺 |
| 跨媒介应用 | 11—16 | 品牌、书籍、导视、产品、空间与动效 |
| 规则实现 | 17—21 | 生成艺术、数字系统、Token、组件与治理 |
| 专题与练习 | 22—30 | 跨媒介实践、摄影、服装、海报、广告、PPT、画报、包装与改稿 |
| 原创与当代 | 31—33 | 三套原创项目、六个当代品牌及延伸学习 |
| 附录 | A—C | 术语、旁读入口与设计工作纸 |

历史案例与当代项目相互对照。2023—2025年的品牌案例包括Pepsi、Reddit、Wise、Spotify Mix、Config与Decathlon；相应章保留官方出处和图像身份说明。

## 原创工坊

[创作工程](examples/creative-lab/README.md)包含折光、野序与隙间三套教学项目，各有设计系统、原生Canvas、素材、字体及制作脚本。折光采用V5纸白、宋体中文与蓝金光场方向；野序为植物摄影风格画报；隙间为咖啡品牌、包装与电商原型。三者共保留18块可见画板。

AI完整提案用于确定视觉方向，无字素材用于排版，可编辑文字与图形在原生画板中重建。完整提案与重建成品各有用途，并非逐像素复刻。品牌、活动、刊物、商品和价格均为教学虚构。

首次克隆后，在仓库根目录还原原生工程所需字体，再打开项目：

```bash
python scripts/restore_native_fonts.py
cd examples/creative-lab
npx --yes tingly-design@0.26.1021 --projects .
```

首次取得工具需要联网；素材和字体随工程提供。原生工程检查命令为 `DC_CHROME=/你的/Chrome路径 python scripts/check_creative_lab.py`。

## 构建PDF与阅读站

建议Python 3.12。正文和图片已附带，构建阅读版无需重新生成图片。

```bash
python -m pip install -r requirements.txt
python scripts/restore_native_fonts.py
python scripts/build_book.py
python scripts/check_book.py --render
python scripts/check_book_embedding.py
```

PDF输出为 `build/design-grammar.pdf`。检查报告记录页数、缺字、图注、链接与配图放置；生成产物不纳入Git。GitHub Actions的 **Build illustrated book** 工作流会构建PDF，并将PDF与检查报告保存为 `design-grammar-pdf` artifact。

阅读站使用同一套分章Markdown与图片，构建时将实际引用图像转换为网页用WebP，原始图片保留：

```bash
python -m pip install -r requirements-site.txt
python scripts/build_site.py
python scripts/check_site.py
python -m http.server 8000 --directory build/site
```

推送main会触发GitHub Pages发布。首次部署需在仓库Settings → Pages中将Source设为GitHub Actions。

教学图的绘制脚本位于 [scripts/](scripts/)。修改图像后，先重绘对应素材，再构建PDF；`collect_creative_lab.py` 收集原生导出，`render_creative_gallery.py` 生成工坊总览。PPT示例保存为PNG及绘图代码，未提供可编辑PPTX。

## 来源与版本记录

真实图索引见 [case-index.md](references/case-index.md)，图像下载与处理记录见 `references/revision-*-images.json`。作品按原权利人归属；公开可访问不等于获得开放再许可。Met开放图像遵循其各自记录。教学标线、局部裁切和生成图均在图注中说明。

当前PDF嵌入检查见 `references/embedded-artwork-current-audit.json`，当前页码见 [插图索引](references/current-artwork-page-index.md)。[V5索引](references/v5-artwork-page-index.md)与[V4索引](references/v4-artwork-page-index.md)保留旧版定位，不能用来查本版页码。

仓库首次提交仅含零字节README，后续导入V5工程并继续修订；历史不重写。导入说明见 [repository-import.md](docs/repository-import.md)。导入前版本保留在此前交付的Git bundle中。
