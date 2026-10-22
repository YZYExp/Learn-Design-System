# 原创创作工坊：从AI素材到可编辑视觉系统

三套原创品牌、活动、刊物、商品、价格与时间均为教学虚构。V5折光先由内置imagegen生成完整海报提案，再从同一提案派生无字光场并重建可编辑画板；野序与隙间保留V4的主视觉。V3素材与历史亦保留，画布标题、正文、形状、布局、组件和系统另由本书作者编写。项目通过Tingly Design 0.26.1021原生new创建，保留可编辑源文件。

首次从Git克隆后，先在仓库根目录运行 `python scripts/restore_native_fonts.py`，校验并还原V5完整宋体，再进入本目录运行：

```bash
npx --yes tingly-design@0.26.1021 --projects .
```

或只打开一套：

```bash
npx --yes tingly-design@0.26.1021 open ./refraction-canvas
npx --yes tingly-design@0.26.1021 open ./field-canvas
npx --yes tingly-design@0.26.1021 open ./still-canvas
```

| 系统 | 核心语法 | 成品 |
| --- | --- | --- |
| 折光 | 中文宋体、纸白、蓝金光场与细衬线英文 | 海报、邀请、三页提案、规则、改稿 |
| 野序 | 单枝摄影风格影像、衬线编辑字与非对称阅读 | 封面、跨页、花展广告、规则、反例、裁切 |
| 隙间 | 材料色、风味编码、信息位置与行动 | 品牌广告、三包装、订阅原型、规则、压力测试 |

六个原生项目分别为三个*-system与三个*-canvas。每套自建设计系统含tokens、字体、README、实际可调用组件与preview。18块可见画板全部保留原生文字与图形；另有一块用于导入的隐藏商品卡。当前三张原始素材、完整折光提案与生成记录在shared-assets。首次取得软件需要联网，字体和图片已本地保存；正常查看和编辑不需要外部AI账号。

canvas/ds中的Token及字体是系统安装快照，源项目改动后需显式重新安装；快照不表示已排版的所有内联数值自动重写。各套README解释具体规则和更新方式。tokens.css由原生工具编译，不手工维护。

## 检查和导出

本机需Chrome/Chromium，可通过DC_CHROME指定已有可执行文件。CLI 0.26.1021导出折光PNG时还需在系统安装附带的Noto Serif CJK SC字体：Linux复制refraction-system/fonts/RefractionSong.otf到用户字体目录后运行fc-cache。编辑器通过工程文件加载字体。

```bash
npx --yes tingly-design@0.26.1021 check ./field-canvas --snapshots
npx --yes tingly-design@0.26.1021 export ./field-canvas --as png --scale 2 --out ./field-canvas/renders/export
```

其他套替换目录名。check预览在renders/check，正式2倍图在renders/export。本次交付将CLI的@2x后缀移除以保持书稿路径稳定，像素仍为两倍。野序Before为可读但焦点过多的受控反例，非上一版成品。隙间Play模式实际测试月订阅148元/单次156元、说明和本地确认；不进行下单或扣款。

## 如何学习

先看规则板，再看成品。只改一项：两字展名变六字、换一幅植物影像、加入第四款咖啡。观察层级、裁切、信息区是否仍成立，再改变媒介或主题。不要一开始同时换所有颜色、字体与图片，否则很难知道是哪条关系发生作用。

作者重建脚本会覆盖当前编排，手工修改前先另存。refraction使用build_refraction_v5.py/refresh_refraction_tokens.py（build_refraction.py为V4）；field使用field-canvas/source中的脚本；still使用still-build中的脚本。Play自动测试额外使用Node Playwright（npm install --no-save playwright），并需设置TINGLY_DESIGN_CLI与DC_CHROME；正常编辑无需该测试依赖。

用户本轮明确要求原生Canvas和Design System，因此.dc.html与组件preview.html是所需的可编辑源文件；没有生成书籍网站。原生格式参考由工具skills add取得，保存在reference，软件许可同时附上。字体按各自许可使用。


## 修订与包内文件

V5完整提案与去字光场记录在shared-assets/generation-log-v5.json；generation-log-v4.json保留上一轮素材记录，generation-log.json保留V3。各套源脚本与V3源码对照保留，当前canvas.json的order只包含正式画板。

交付包保留全部原生源、实际字体与书中用图。可再生成的check截图、未被书引用的旧PNG与系统视图导出不重复打包，原生检查报告与清单保留。需要重新审计渲染时，先按上文命令对三个canvas与三个system运行check/export，再执行总审计；缺少可再生截图不代表缺少画布源文件。
