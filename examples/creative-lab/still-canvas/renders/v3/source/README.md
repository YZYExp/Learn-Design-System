# 隙间 / STILL · 原生品牌画布

本项目是Tingly Design原生Canvas，关联设计系统在`../still-system`。品牌、商品与价格均为原创虚构教学内容；AI摄影是材料情境，不代表真实商品实拍。

## 五张可编辑画板

1. `Main.dc.html`，1600×1000：品牌主张、四色、字体、间距、图像与包装语法。
2. `Campaign.dc.html`，1600×900：AI绿釉咖啡杯摄影与可编辑广告文案。
3. `Packaging.dc.html`，1600×1050：01日常拼配、02山坡花开、03夜色低因的包装正面与信息面；是平面构成，不是3D实拍。
4. `Subscription.dc.html`，1440×1100：三张真实dc-import商品卡、两种计划与本地确认。
5. `Stress.dc.html`，1440×1100：夜间语义换色、长名称、原色摄影与修订理由。

隐藏的`ProductCard.dc.html`为可调用Canvas模板，供订阅页三次导入。商品名、系列、风味、价格、字色通过props传入；属性使用小写`productname`，避免HTML大小写归一化。隐藏只是不占展示位置，源文件保留。

## 打开与操作

命令统一从上一级、包含两个项目的`creative-lab/`目录执行：

```sh
npx --yes tingly-design@0.26.1021 open ./still-canvas
npx --yes tingly-design@0.26.1021 check ./still-canvas --snapshots
npx --yes tingly-design@0.26.1021 export ./still-canvas --as png --scale 2 --out ./still-canvas/renders/export
```

双击原生文字编辑，摄影为独立层。试交互时先点编辑器顶部**Play**进入播放模式，再在“04订阅电商”切换“每月订阅 / 先试一次”；金额与摘要分别为¥148 / ¥156。“选择这份隙间”显示本地确认，切回另一计划会清除确认。没有下单或扣款。

`ds/still/tokens.json`与fonts为原生安装快照。完整规则、DOM组件与preview在`../still-system/`：`STILL.ProductCard()`可实际调用；Canvas模板则保留可编辑图层。

## 检验与作者修订

首轮发现并修复：动态双括号被脚本压成单括号、导入属性大小写导致商品同名、价格被flex压成两行。小号陶土由4.2∶1加深为`clay-text`，品牌原色保留用于大编号。长名称不靠缩小正文塞入，而自然换行。

检查图保留于`renders/check/`，高分辨率成品在`renders/export/`。原生CLI默认`@2x.png`后缀；交付版如按画板stem命名，实际像素仍为两倍。

## 独立重建

`../still-build/build_still.py`重建两个STILL项目，需`../shared-assets/still-coffee.png`。字体优先取书工程，独立包自动回退`../still-system/fonts/NotoSansSC-Regular.ttf`，保留完整creative-lab即可。脚本会覆盖源文件，先保存自己的改动。`tokens.css`只由运行中的原生编辑器生成，不手写。

`../still-build/test_interaction.cjs`在原生编辑器Play模式检查金额切换、商品名、确认与重置；需环境变量TINGLY_DESIGN_CLI指向已安装0.26.1021的cli.mjs、DC_CHROME指向Chromium。生成记录在`../shared-assets/generation-log.json`。Noto Sans SC为SIL Open Font License，OFL.txt随字体保留。
