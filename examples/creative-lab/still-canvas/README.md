# 隙间 / STILL · V4原生画布

原创虚构咖啡品牌的5张完整画板，设计系统在`../still-system`。V4保留原生组件与交互框架，重新设计全部视觉结构；V3源与导出保留在`renders/v3`。

## 五张当前画板

- Main，1600×1000：压缩字标`[STILL]`、品牌主张与三栏编辑规则（光线、图形、颜色）。
- Campaign，1600×900：全幅俯拍摄影，前景MAKE ROOM信息块与下方BREW BETWEEN黑色横带。
- Packaging，1600×1050：三种可编辑图形谱系——规律条纹、流动等高线、断开的轨道；同时保留清楚的编号、风味、规格与信息面。
- Subscription，1440×1100：GOOD DAYS / ON REPEAT刊头、照片横带、购买计划选择行与COFFEE INDEX，不沿用旧左文右图。
- Stress，1440×1100：石墨主题完整产品详情，长商品名、整组风味、独立价格和实际行动位置。

隐藏ProductCard.dc.html为三次原生导入模板，小写productname避免HTML大小写归一化。三卡名为日常拼配、山坡花开、夜色低因，单包¥68/88/78。它们是教学商品与价格。

## 颜色与图片

纸白#F5F3EC、石墨#20211D、橄榄#424A32、一处鲜橙#F05A24。主行动橙底配石墨字，不以橙色写小字。图片采用`uploads/still-coffee-v4.png`：AI俯拍白杯咖啡与几何台面，仅供情境；黄色果实不识别物种。图片保持原色，文字、包装图形和价格独立可编辑。当前包装为平面图，不是3D实拍或生产刀模。

## 使用与检查

从上一级creative-lab执行：

```sh
npx --yes tingly-design@0.26.1021 open ./still-canvas
npx --yes tingly-design@0.26.1021 check ./still-canvas --snapshots
npx --yes tingly-design@0.26.1021 export ./still-canvas --as png --scale 2 --out ./still-canvas/renders/export
```

编辑器顶部点Play，订阅页“每月订阅 / 先试一次”切换¥148 / ¥156；“选择这份隙间”显示本地反馈，切换计划重置。无下单或扣款。`../still-build/test_interaction.cjs`可验证这条真实路径。

renders/check保留原生检查，renders/export保留@2x像素成品（按stem命名）。作者入口为`../still-build/build_still.py`，随后执行`v4_still.py`；字体在完整书工程和独立包本地fonts之间自动回退。重建前保存自己改动。tokens.css只由原生编辑器生成。字体采用SIL OFL，摄影记录在shared-assets/generation-log-v4.json。
