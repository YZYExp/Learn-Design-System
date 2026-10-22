# 折光 / REFRACTION · V4原生创作画布

本书原创虚构光学艺术展练习。展览、地址、2026年11月7日开幕、展期与到场条件均为虚构教学内容。主视觉为实际AI生成的透明弯折玻璃艺术示意，不是真实摄影或物理实验。

## 七块正式画板

| 文件 | 尺寸 | 视觉任务 |
|---|---|---|
| Main.dc.html | 1080×1440 | 连续玻璃图像场、英文展示字、中文展名和底部到场信息 |
| Invitation.dc.html | 1600×900 | 银色玻璃与窄红票面相接，日期成为入口 |
| Proposal01.dc.html | 1600×900 | 完整形体与策展命题，保留观看呼吸 |
| Proposal02.dc.html | 1600×900 | 不等尺寸的图像裁切、三次观看转折 |
| Proposal03.dc.html | 1600×900 | 海报与邀请按各自真实比例进入应用页 |
| VisualRules.dc.html | 1600×1000 | 将字图关系与红黑银角色组织为编辑页 |
| Revision.dc.html | 1600×1000 | V3材质研究到V4光学展的方向修订对照 |

文件stem、根元素尺寸、canvas.json及data-props.$preview保持一致。每个文件保留support.js、x-dc与逻辑块。文字是可双击改写的字面内容，图像是独立img，色面与分隔线是独立div；没有将成品版面整体压平。

## V4改了什么

邀请左下说明句放在独立冷白底带，避开玻璃高光与深色边线；应用页的内嵌邀请保持同样处理。

V3的大幅中文两字、斜切照片、左右分栏邀请和三张相等裁切，容易让所有输出成为同一个模板。V4以光学玻璃焦点与英文展示字建立展览识别；中文、日期与正文按载体重新安排。海报、红票邀请、完整形体提案、非等宽细节页、跨媒介比例页各承担不同任务。

Revision如实展示V3和V4的不同图像与排字方向，不能称作“同图、只移动文字”的对照。旧七板PNG与V3可编辑源码保存在renders/v3，仅供历史比较；它们不加入正式canvas.order。Revision左侧保留原V3可编辑参考图层，右侧为V4图层；不是把两个成品PNG贴在画板上。

Proposal02的几幅图是同一AI源图的不同裁切，不是三个相机视点。Proposal03的媒介缩略版仍由原生文字、图片和图形组成；外框按比例缩放并裁住媒介边界，不能让主视觉越过海报页脚。

## 原生快照与组件

ds/refraction/tokens.json的version为4，字体本地随附；canvas.json记录refraction-system来源。快照供样式面板选择和后续更新，具体内联值仍可直接编辑。系统有ExhibitTitle、InfoStrip、PictureFrame三个可调用组件及Cover预览。

## 复建与原生核验

CLI固定实际使用版本0.26.1021。首次创建原生工程后，在creative-lab目录运行：

```bash
npx --yes tingly-design@0.26.1021 new design-system refraction-system --title '折光 / REFRACTION'
npx --yes tingly-design@0.26.1021 new canvas refraction-canvas --title '折光 / REFRACTION' --size 1080x1440
python3 build_refraction.py
python3 refresh_refraction_tokens.py
npx --yes tingly-design@0.26.1021 check refraction-canvas --snapshots
npx --yes tingly-design@0.26.1021 check refraction-system --snapshots
npx --yes tingly-design@0.26.1021 export refraction-canvas --as png --scale 2 --out refraction-canvas/renders/export
```

已缓存同版本时可设置TINGLY_DESIGN_CLI指向实际cli.mjs，辅助脚本即使用该路径；无图形环境可用DC_CHROME指定本地Chrome。构建读取shared-assets/refraction-hero-v4.png与本书本地字体；素材不存在便停止，不制造假照片。--source-only只在等待生图时恢复源码。

原生check图在renders/check，正式2×PNG在renders/export。官方CLI默认输出@2x后缀；正式交付仅去掉后缀以保持原stem，不改变像素。export-manifest.json记录实际路径、尺寸与SHA-256，export-report.json保留原始CLI输出。

构建后必须重新执行check、export与verify_refraction_components.mjs，不能把V3通过记录当成本轮结果。最新本轮check-report.json与renders/component-live-qa.json给出实际核验结果；DS整体导出不捕捉组件iframe，不等于组件不存在。

## 本轮实际结果

V4重新执行原生canvas七板与design-system六视图check，均为problems:[]；七板2×PNG及DS colors原生export均为failed:[]。真实组件iframe调用passed:true，ExhibitTitle读取96px原生title样式，三个namespace均为object，PictureFrame的两张V4玻璃裁切加载正常。七板最终PNG已经逐一加载核对，Main为2160×2880，其余按各自画板尺寸2×输出。
