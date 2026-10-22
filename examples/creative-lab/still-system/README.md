# 隙间 / STILL · V4

“让日常，有一次停顿。”STILL是原创虚构独立咖啡品牌，所有商品与金额为教学创作。V4以编辑设计建立辨识：压缩的大字标`[STILL]`、图形里的间隙、三种品类谱系，以及一处清楚的鲜橙行动。

## 当前颜色与字号

纸白`#F5F3EC`负责阅读，石墨`#20211D`负责结构与正文，橄榄`#424A32`连接摄影气氛与品类，鲜橙`#F05A24`用于主要行动。橙底配石墨字；小字号文字不使用鲜橙。日间为纸白表面，夜间为石墨表面，正文成对换色，图片不反相。`terracotta`与`clay-text`是兼容旧组件名的令牌，V4的实际值已是橄榄，不再表示陶土。

中文随项目携带Noto Sans SC，英文品牌使用Arial无衬线粗体；超大字标收紧字距，商品名保留正常阅读间距。按钮与风味信息改为方角，商品列使用上方粗线组织，不使用胶囊与卡片阴影。

## 三种包装语法

01日常拼配：石墨底、鲜橙规律条纹，中间保留明显停顿。02山坡花开：橄榄底、纸白流动等高线。03夜色低因：纸白底、石墨轨道线，在中央断开。三款共享上方字标、右上编号与250g规格、下方品类与风味位置；信息面保留日期、批次与储存说明。图形是原生可编辑线条与矢量，不是烘焙在AI包装效果图里。当前平面不冒充生产刀模，法定标识投产前另行核对。

## 摄影的职责

`assets/Photography/still-coffee-v4.png`是AI生成俯拍情境：白色小杯与咖啡、深色几何台面和精确斜影。黄色果实不作物种或产地判断。照片提供光线与气氛，不证明产品事实。图像本身无字；品牌、价格、品类、说明均为可编辑层。生成记录位于`../shared-assets/generation-log-v4.json`。

## 三个真实组件

`STILL.ActionButton({label,variant,disabled,onClick})`返回原生button；`STILL.FlavorTag({label})`提供非交互风味信息；`STILL.ProductCard({name,series,flavor,description,price,image,action,onClick})`返回完整商品信息，允许长名称增高。组件API保持稳定，V4同步其颜色、字号、方角与编辑型结构，各自preview可运行。Canvas另以原生dc-import模板保留图层编辑。

## 五板与实际交互

关联`../still-canvas`：Main为大字标与三栏编辑型规则页；Campaign为全幅顶视摄影、MAKE ROOM与下方黑色品牌横带；Packaging为三套图形谱系；Subscription为期刊式刊头、照片横带、独立购买选择行与三列商品；Stress为完整石墨产品详情与长名检验。既有5个stem不变，隐藏ProductCard模板继续被调用。

Play模式中可切换每月订阅¥148 / 一次体验¥156，选择显示本地确认，切回另一计划清除确认。无真实下单、账号或扣款。长标题、价格nowrap和单行风味分组作为必要压力检查。

## 打开、检查与重建

下列命令从上一级creative-lab运行：

```sh
npx --yes tingly-design@0.26.1021 open ./still-system
npx --yes tingly-design@0.26.1021 check ./still-system --snapshots
npx --yes tingly-design@0.26.1021 check ./still-canvas --snapshots
```

`tokens.css`由运行中的原生编辑器生成，不手写。作者入口`../still-build/build_still.py`创建可移植基础，再执行同目录`v4_still.py`完成V4覆盖；两文件一起保存。独立包字体回退到本系统fonts，图片来自shared-assets/still-coffee-v4.png。重建会覆盖作者源文件，先保存自己的改动。V3源与图保存在renders/v3及still-build/v3，当前版本不使用旧绿杯与牛皮纸袋。
