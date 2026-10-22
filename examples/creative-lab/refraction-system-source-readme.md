# 折光 / REFRACTION · V4

“折光”是本书原创虚构的光学与感知研究展。展厅、虚构路18号、展期、开幕之夜及入场条件均为虚构教学内容，不是现实活动公告。本系统由空白原生design-system创建，不复制现成Look模板。

## 从材料练习到光学艺术展

V3使用纸面、石膏和几何体的硬光照片式构成。V4不再只给旧版更换一张图片，而是以透明弯折玻璃、银色反射与一线红光为焦点，重新决定展示字、信息位置和载体比例。冷白是展示场，不再模拟旧纸。

主视觉shared-assets/refraction-hero-v4.png是实际AI生图；不是真实展品、摄影记录或光学实验。玻璃的可见透射和反射作为艺术示意，不能据此推导材料性能。原始图像和生成记录独立保留；文字、色面、分隔线和版式均为原生可编辑图层。

## 四个视觉角色

- **冷白surface** #F4F5F7：图像与排字的展示场。暗场主题为#101114。
- **阅读ink** #101114：标题与正文；暗场中反转为冷白。
- **展览红accent** #D62A20：入口、中文展名、数字或邀请票面。白字on-accent用于红底；不在每一个段落重复强调。
- **银silver** #C6CBD1：辅助结构。银色平面不能代替玻璃图像的真实复杂光影；muted和hairline分别用于辅助文字及分隔。

英文REFRACTION承担远距离识别，紧密排字但不让字母相撞；中文说明展名和题意，保留完整字形与适度字距。Noto Sans SC作为本地字体随工程保存，附OFL。显示字、标题、短句、正文与元信息有不同尺度，不机械把同一个176px字号套进所有载体。

## 图像与版面的关系

海报让图像成为连续视觉场，英文标志位于上部，中文与到场信息分层进入下部。开幕邀请以银色玻璃场与窄幅红票面相接，日期成为票面的识别入口。三页提案分别组织完整形体、不同密度的细节裁切与两个实际媒介比例。

同一图像的细节裁切不冒充不同机位或不同物理阶段；提案二明确注明这一边界。常用间距8、16、32、64、80只是关系词汇，具体媒介还需要重新安排文字与图像大小。直角边界保持干净，不增加卡片阴影或通用框架装饰。

## 三个可调用原生组件

components/bundle.js定义window.REFRACTION，返回真实DOM，无外部JS依赖：

```js
REFRACTION.ExhibitTitle({english:'REFRACTION',chinese:'折光 — 光学与感知研究展'})
REFRACTION.InfoStrip({date:'2026.11.07—12.06',venue:'折光实验展厅'})
REFRACTION.PictureFrame({src:'../../assets/Photography/refraction-hero-v4.png',ratio:'3 / 4',position:'50% 50%'})
```

ExhibitTitle另有compact密度；InfoStrip聚合日期、时间、场所；PictureFrame根据任务指定比例与裁切中心。每个组件有独立README和真实preview.html，颜色、字体、间距来自原生token。组件不能由截图替代。

## 版本、快照与核验

本版tokens.json的version为4。相邻refraction-canvas/ds/refraction保存token及字体快照，canvas.json记录来源与版本。重新安装或运行build_refraction.py可更新快照；画板内联样式仍是具体可编辑数值，不宣称所有属性与token双向实时绑定。

tokens.css由Tingly Design 0.26.1021原生token编译器生成，不能手写。refresh_refraction_tokens.py通过本地原生服务进行版本化token更新，触发官方CSS生成。三个组件的真实iframe调用由verify_refraction_components.mjs核验，不用mock DOM冒充原生编辑器。

复建与实际本轮结果见相邻refraction-canvas/README.md。原生DS整图PNG导出不捕捉组件iframe内容；原生编辑器的三个live preview仍可调用。
