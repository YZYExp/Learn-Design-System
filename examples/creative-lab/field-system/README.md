# 野序 / FIELD NOTES · V4

原创虚构植物艺术杂志。No.07、2027夏刊、展览名称、日期、开放时间与场地都是示范文案，不是实际出版物或活动。植物图是AI生成的编辑摄影风格研究，不是真实摄影师作品、植物标本或科学记录。

## V4重构
V3以巨大的中文刊名和满版水粉块形成上下三段，三种媒介又共享相近框架。V4更换了观看方法：中文刊名缩到身份尺度；Nimbus Roman的细衬线、真实斜体和小号issue furniture建立编辑语气；照片从密集花丛改为单枝微距，留边与花头方向成为版式条件。

封面：左侧英文与小刊名，右侧窄幅长照片，专题文字成为可以停留的边注。
跨页：中部摄影跨越中缝，两侧各有独立文章栏，正文不跨装订缝，图注与页码清楚分开。
广告：左侧日期和垂直信息脊，右侧接近全高摄影；它不是封面的放大版。
Rules把字体、色彩和编辑限制做成完整语法页；CropStudies以不等宽画框说明完整姿态、封面取景与触觉细节；Before没有随机遮字，而是让刊名、期号、专题同样响亮，形成受控层级反例。

## 规则
paper承载长文，plum承载标题，moss用于小号家具，blush只是摄影的柔和衬底。线条不承担必要文字信息。每页只选择一个主要观看动作；正文必须有自己的平静区域。字体全部本地，Field Sans是Noto Sans SC；Field Serif是Nimbus Roman真实常规和斜体，不用浏览器合成斜体。

## 原生使用
六板仍为Main、Spread、Exhibition、Rules、Before、CropStudies，标题、图注与正文都是可编辑的字，照片单独存uploads/field-botanical-v4.png。source/build_field.py重建真正的V4，不是事后替换图片；运行会覆盖人工编辑。

field-system提供Masthead、EditorialCaption、EventBadge和Cover真实可调用组件、preview、token与本地字体。通过原生API安装后，ds/fieldnotes保存明确版本快照；改token需重新安装。source/install_field.py与verify_components.py负责实际安装、编译与浏览器组件检查。

## 归档
旧六张成品及旧源稿保留在renders/v3，旧构建源码在source/build_field_v3.py；它们不进入canvas.json的order。旧素材不改名不删除。

## 版权与身份
品牌、版式和文案为本书原创。AI资产来源日志位于shared-assets/generation-log-v4.json。Noto和URW字体许可在fonts内。本项目不借用真实杂志、Figma或Spotify的商标。

## Tokens和组件
version=4；8个语义色，7个文字样式，6档间距、3半径及组件尺寸。Masthead把身份放低，EditorialCaption明确图像来源，EventBadge把日期变成信息锚点。三个组件都返回实际HTMLElement，Cover调用它们。tokens.css由原生编辑器生成，源脚本不手写。
