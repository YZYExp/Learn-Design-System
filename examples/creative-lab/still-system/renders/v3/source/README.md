# 隙间 / STILL

把一杯咖啡，留在日常的隙间。STILL是原创虚构咖啡品牌，所有品类、文案、规格与价格均为教学创作；不代表实际门店、产地或销售。

## 从材料建立秩序

暖石底色`surface`让绿釉器皿、牛皮纸与深棕文字共存。深绿`accent`承担主要行动，陶土`terracotta`用于大编号与风味装饰。中文使用随项目携带的Noto Sans SC，英文品牌使用本地衬线字体。画面用层级与留白支持缓慢阅读。

日间：`ink`与`ink-muted`在`surface`和`surface-raised`上阅读；`on-accent`仅用于`accent`之上。夜间不反相照片：底色变深，正文与行动成对变亮，摄影保持原色。原始陶土在暖石上约4.2∶1，不用于小号文字；小字提示使用加深的`clay-text`（#954128）。大编号继续保留品牌陶土。

## 颜色之外的规则

文字：76主张、44标题、24商品名、18正文、14注记；标题允许自然换行。间距：16组件内部、24信息组、40卡片、64版块、96宽画板边距。包装用方角，按钮仅2px细微圆角，风味标签才用胶囊轮廓。

摄影：AI生成材料情境照片，绿釉杯、暖石面、无字纸袋、自然侧光。它提供质感与情绪，不证明产地或产品性能。字标、价格、日期与名称均用可编辑文字层，图片不替代信息。

包装：01日常拼配、02山坡花开、03夜色低因共享字标、编号、名称、风味和规格位置，以编号与名称共同识别。信息面保留批次与烘焙日期填写位置。这是可编辑平面设计，不冒充已制成3D包装；投产前须完成材质打样、刀模和销售地标识核对。

## 三个真正可调用的组件

- `STILL.ActionButton({label,variant,disabled,onClick})`：原生button；实心为主要行动、描边为次行动，键盘焦点有独立边界。
- `STILL.FlavorTag({label})`：风味词，不以颜色独自编码，也不假装是按钮。
- `STILL.ProductCard({name,series,flavor,description,price,image,action,onClick})`：完整商品信息，允许自然增高；preview包含短名称与长名称。

普通DOM组件在`components/bundle.js`真正导出；每个组件有可运行preview，非截图占位。Canvas用原生`dc-import`的`ProductCard.dc.html`桥接可编辑模板，共享语义与信息架构；逻辑脚本不构造画面DOM。

## 五张画板和修订

关联Canvas：`../still-canvas`。规则1600×1000、摄影广告1600×900、包装1600×1050、订阅电商1440×1100、夜间与长名1440×1100。订阅可切换“每月订阅 / 先试一次”，金额与摘要同步；选择按钮只改变本地教学状态，不下单、不扣款。样例金额¥148 / ¥156，单包¥68 / ¥88 / ¥78。

首轮修订：小号陶土4.2∶1，加深文字色；价格被flex压成两行，增加nowrap；长标题允许自然换行，不靠缩小正文塞下。摄影在夜间保持原色。Native check和成图共同检验，源文件存在不等于画面正确。

## 打开、检查、重建

以下命令统一从上一级`creative-lab/`目录执行：

```sh
npx --yes tingly-design@0.26.1021 open ./still-system
npx --yes tingly-design@0.26.1021 check ./still-system --snapshots
npx --yes tingly-design@0.26.1021 check ./still-canvas --snapshots
```

项目由指定版本原生new创建；同版本已安装时可直接用本机CLI。`tokens.css`由运行中的编辑器随tokens.json变化自动生成，不手写。

作者重建脚本：`../still-build/build_still.py`。字体优先取完整书工程，独立教学包自动回退`still-system/fonts/NotoSansSC-Regular.ttf`；照片来自`shared-assets/still-coffee.png`。完整保留creative-lab即可独立重建；脚本会覆盖两个STILL项目，先保存自己的改动。摄影生成记录见`../shared-assets/generation-log.json`。Noto Sans SC采用SIL Open Font License，OFL.txt随字体保留。
