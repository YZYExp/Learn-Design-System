# 折光 / REFRACTION

“折光”是本书原创的虚构光与材料研究展。展览、展厅、日期、地址与邀请活动均为虚构教学示例，不是现实活动公告。本系统由空白原生design-system创建，没有复制现成Look模板。

## 视觉立场

一束硬光让纸的折面、石膏的体量与朱红色块形成关系。主视觉来自本次实际AI生图；文字、形状、细线和版式保留原生图层。AI提供材质与光影，系统决定它怎样被观看。

## 色彩与文字

- surface为纸面#F3F0E8与暗场#191919，ink在两个主题中反转，承担所有阅读文字。
- accent为#C7472E，仅用于大字、编号与短线；小字用ink。on-accent白色只用于朱红底。
- muted是辅助文字；hairline只用于分隔和网格，不承载正文。
- 本地Refraction Sans来自Noto Sans SC，附字体和OFL。字号176、88、48、28、24、18像素，避免引入多套字体。
- 中文标题建立第一入口，英文承担同组识别。日期、时间与场所聚合；标语不压在照片材料连接最复杂的位置。

## 网格、间距与裁切

横版80像素外边距，竖海报64像素；六栏为组织骨架。间距序列8、16、32、64、80。图像与色面保持直角，只有照片裁切边缘可延续原图的斜向关系。没有卡片投影或泛用渐变。

竖海报为中文主题→英文→材质图→日期地点；邀请把图像放在右侧，让到场信息在左侧汇合。三页提案分别讲命题、观看路径与跨媒介应用，不机械拉伸同一个海报。

“观看路径”的三张图来自同一AI图的不同裁切，不是三个相机视角；不作为物理实验或真实展厅记录。

## 三个可调用组件

components/bundle.js定义window.REFRACTION，三个函数返回真实DOM，无外部JS依赖：

```js
REFRACTION.ExhibitTitle({chinese:'折光',english:'REFRACTION'})
REFRACTION.InfoStrip({date:'2026.11.07—12.06',venue:'折光实验展厅'})
REFRACTION.PictureFrame({src:'../../assets/Photography/refraction-hero.png',ratio:'4 / 3',diagonal:true})
```

每个组件有独立README和原生preview.html。字号使用官方token编译出的样式类，颜色与间距读取变量。不要用组件截图替代组件。

## 快照与更新

相邻refraction-canvas/ds/refraction保存本系统的token和字体快照，canvas.json登记来源与版本。原生编辑器的“设计系统”面板可以重新安装更新；build_refraction.py显式重新复制快照。

画板采用具体内联样式，便于逐字改写、选择和挪动。快照为样式面板提供词汇，不声称每个已写入内联值都双向实时绑定。

tokens.css由Tingly Design原生token编译器生成，不能手写。修改tokens后可在原生编辑器中触发；批量重建时运行相邻refresh_refraction_tokens.py，它通过本地原生服务执行版本化token更新，触发官方CSS生成。

## 复建与核验

见相邻refraction-canvas/README.md。CLI固定0.26.1021。DS整体PNG导出不捕捉组件iframe内容，这是工具导出范围；原生编辑器中的三个live preview仍是真正可调用的组件。
