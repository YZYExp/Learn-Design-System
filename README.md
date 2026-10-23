# 设计的语法

## 从艺术秩序到设计系统 · 6.0 主线重编版

面向非专业读者的中文图解设计读本。全书包含导读、六篇33个正文章和3篇附录，沿着“观察作品 → 提炼视觉关系 → 适配不同媒介 → 建立可复用规则 → 检验与维护”展开，从构图、色彩和图像语言，走到海报、广告、PPT、书籍、画报、包装、产品、服装、空间与数字设计。

本版在5.1全文校订的基础上重编学习顺序，让“岸线设计周”的任务、制作与检验贯穿全书，并将六个当代品牌的完整分析移到相应专题。原有178张独立图像全部保留，新增一张阅读路径图；合并三处重复用图后，共185次配图使用、179张独立图像。图片包含真实作品、原创分析、教学图、原创设计和明确标注的AI图像。修订依据见 [全文校订标准](docs/editorial-standards.md)，编排与章号变更见 [6.0重编记录](docs/restructure-6.0.md)。

[在线阅读](https://yzyexp.github.io/Learn-Design-System/) · [分章书稿](chapters/) · [附录](appendices/) · [当前插图页码](references/current-artwork-page-index.md) · [素材与引用](references/)

![折光V5：海报与邀请的原生画板](examples/creative-lab/refraction-canvas/renders/export/Proposal03.png)

## 阅读路线

| 部分 | 章节 | 内容 |
| --- | --- | --- |
| 第1篇 · 看懂一件作品 | 01—04 | 用任务、视觉关系、颜色与网格建立观察方法。 |
| 第2篇 · 形成一种视觉语言 | 05—11 | 从图像到装饰、几何、文字和生成规则，理解视觉选择如何组合。 |
| 第3篇 · 组织传播与阅读 | 12—17 | 将同一套判断用于品牌、海报、广告、演示、书籍和画报。 |
| 第4篇 · 进入材料、身体与空间 | 18—23 | 让视觉规则经受材料、包装、器物、身体和场所的约束。 |
| 第5篇 · 处理时间、操作与状态 | 24—27 | 从时间脚本走到交互，用语义角色、Token与组件组织变化。 |
| 第6篇 · 完成、检验与维护 | 28—33 | 完成综合项目，与真实案例比较，再安排协作、修订与练习。 |
| 附录 | A—C | 术语、旁读入口与设计工作纸 |

“岸线设计周”为教学虚构：从第一篇确定海报、册页、导视、纸袋与手机预约的共同任务，随后随媒介章节逐步积累规则，在第28章汇成完整练习。第29章的折光、野序、隙间是三套独立原创项目，可与岸线练习相互参照。

历史案例与当代项目相互对照。2023—2025年的六个品牌案例分别放在品牌识别（Reddit，第12章）、书籍与编辑（Spotify Mix，第16章）、包装（Pepsi，第19章）、服装（Decathlon，第21章）、导视（Config，第23章）和数字系统（Wise，第25章）旁；第30章集中比较其方法与适用条件。完整分析保留官方出处和图像身份说明。

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

建议Python 3.12。正文和图片已附带，构建阅读版无需重新生成图片。`book.json` 是网站与PDF共用的目录清单，定义显示章号、六篇顺序、标题与稳定源文件路径；文件名中的旧章号保留，以维护已有URL。总目录、前后章导航与PDF顺序均从清单生成。

```bash
python -m pip install -r requirements.txt
python scripts/restore_native_fonts.py
python scripts/check_structure.py
python scripts/build_book.py
python scripts/check_book.py --render
python scripts/check_book_embedding.py
```

PDF输出为 `build/design-grammar.pdf`。检查报告记录页数、缺字、图注、链接与配图放置；生成产物不纳入Git。GitHub Actions的 **Build illustrated book** 工作流会构建PDF，并将PDF与检查报告保存为 `design-grammar-pdf` artifact。

阅读站使用同一套分章Markdown与图片，构建时将实际引用图像转换为网页用WebP，原始图片保留：

```bash
python -m pip install -r requirements-site.txt
python scripts/check_structure.py
python scripts/build_site.py
python scripts/check_site.py
python -m http.server 8000 --directory build/site
```

网页发布与PDF导出使用两个独立CI工作流：**Publish reading homepage** 仅安装网页依赖、校验链接并部署GitHub Pages；**Build illustrated book** 构建并检查PDF，再上传阅读包。PDF排版或导出失败不会阻塞网页部署。推送main会按各工作流配置触发构建；首次部署需在仓库Settings → Pages中将Source设为GitHub Actions。

教学图的绘制脚本位于 [scripts/](scripts/)。修改图像后，先重绘对应素材，再构建PDF；`collect_creative_lab.py` 收集原生导出，`render_creative_gallery.py` 生成工坊总览。PPT示例保存为PNG及绘图代码，未提供可编辑PPTX。

## 来源与版本记录

真实图索引见 [case-index.md](references/case-index.md)，图像下载与处理记录见 `references/revision-*-images.json`。作品按原权利人归属；公开可访问不等于获得开放再许可。Met开放图像遵循其各自记录。教学标线、局部裁切和生成图均在图注中说明。

当前PDF嵌入检查见 `references/embedded-artwork-current-audit.json`，当前页码见 [插图索引](references/current-artwork-page-index.md)。[V5索引](references/v5-artwork-page-index.md)与[V4索引](references/v4-artwork-page-index.md)保留旧版定位，不能用来查本版页码。

仓库首次提交仅含零字节README，后续导入V5工程并继续修订；历史不重写。导入说明见 [repository-import.md](docs/repository-import.md)。导入前版本保留在此前交付的Git bundle中。
