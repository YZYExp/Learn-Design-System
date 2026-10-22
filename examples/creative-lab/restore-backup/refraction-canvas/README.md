# 折光 / REFRACTION · 原生创作画布

本书原创虚构展览品牌练习。折光实验展厅、虚构路18号、2026年11月7日开幕与展期均为虚构教学内容。主视觉是实际AI生图，不是真实摄影；文字与图形保留原生可编辑层。

## 完成画板

| 文件 | 尺寸 | 用途 |
|---|---|---|
| VisualRules.dc.html | 1600×1000 | 三色、字图层级、裁切与六栏关系 |
| Main.dc.html | 1080×1440 | 竖版展览海报 |
| Invitation.dc.html | 1600×900 | 横版开幕邀请 |
| Proposal01.dc.html | 1600×900 | 提案一：展览命题 |
| Proposal02.dc.html | 1600×900 | 提案二：观看路径 |
| Proposal03.dc.html | 1600×900 | 提案三：跨媒介展开 |
| Revision.dc.html | 1600×1000 | 同素材同文案的改稿对照 |

根元素、canvas.json w/h和data-props.$preview尺寸一致。每个文件保留support.js、x-dc及逻辑块。文案是可双击改写的字面文本，照片为独立img，线与色面为独立div。没有把版面压平为图片。

## 创作决策

照片本身的折面与硬光提供方向，文字不再跟着倾斜。标题和日期保持稳定阅读方向；局部斜切延续图片的动势。图像承担方向性，文字承担可检索性。

竖海报先让中文主题被看见，保留一块相对完整的材料图；邀请把照片推向右侧，左侧容纳开幕信息。提案第一页提出观看命题，第二页安排观察次序，第三页展示规则跨媒介展开。

## Before / After记录

Revision两版使用相同素材、中文展名、英文名、日期和地点。

- Before把日期放在入口，中文展名落到图下方，英文与中文缺少明确主次，信息分散。
- After将中文移回入口，英文降为第二层；照片保留材质中心，到场条件在底部汇合。
- 比较的是先找到什么、能否顺利找到到场条件，不宣称所有人都按同一视线观看。

朱红小编号曾在核验中接近4.2:1对比，已改为24像素大字；日常小字仍使用ink。不能只看代码声称视觉完成，应看真实原生出图。

## 原生快照

ds/refraction/tokens.json与fonts是相邻refraction-system的安装快照，canvas.json的designSystems记录来源和版本。重新安装可更新样式选项，不是全部内联数值的自动双向绑定。

## 原生创建与复建

在creative-lab目录中首次创建：

```bash
npx --yes tingly-design@0.26.1021 new design-system refraction-system --title '折光 / REFRACTION'
npx --yes tingly-design@0.26.1021 new canvas refraction-canvas --title '折光 / REFRACTION' --size 1080x1440
python3 build_refraction.py
python3 refresh_refraction_tokens.py
```

构建读取shared-assets/refraction-hero.png与本书assets/fonts/NotoSansSC-Regular.ttf。素材缺失会停止，不生成假照片。--source-only可在生图完成前恢复可编辑源码。

```bash
npx --yes tingly-design@0.26.1021 check refraction-canvas --snapshots
npx --yes tingly-design@0.26.1021 check refraction-system --snapshots
npx --yes tingly-design@0.26.1021 export refraction-canvas --as png --scale 2 --out refraction-canvas/renders/export
```

无图形环境可用DC_CHROME指定本地Chrome或Headless Shell。检查图放renders/check，正式原生PNG放renders/export。CLI默认为2×文件名加@2x后缀，交付移除该后缀，使文件名与画板stem一致，保留完整2×像素。PNG用于阅读，不替代可编辑工程。

复建后须重新执行check/export并记录本轮结果；不能将恢复前的通过记录当作本轮验证。
