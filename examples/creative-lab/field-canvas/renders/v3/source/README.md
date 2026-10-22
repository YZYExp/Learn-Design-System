# 野序 / FIELD NOTES · 可编辑创意实作

虚构植物艺术画报，不是真实刊物、标本或历史设计。ISSUE 07、2027夏刊以及花展日期、场地、开放时间均是原创演示文案，不提供真实活动报名。

## 六块原生画板
Rules：完整设计规则；Main：1080×1440封面；Spread：1800×1200双页文章；Exhibition：花展广告；Before：失败初稿；CropStudies：同一资产的完整、裁切与放大三次取舍。标题、正文、图注和日期均是可编辑文字，植物是可替换PNG，不是整页截图。

## AI与设计分工
uploads/field-botanical.png是实际生成的紫色鸢尾水粉图。图像负责笔触与色层；排版负责刊名、主题、层级、裁切、段落与阅读。完成稿不把正文压在花瓣上；跨页图注明确AI身份，不作鉴定依据。项目包含本地素材和字体，可离线编辑。

## 初稿与改稿
Before故意使刊名覆盖花心、次要信息压在复杂叶片，对比警告属于已知比较条件；它不是最终交付封面。CropStudies随后分离阅读区、调整花心关系、放大观看尺度；Main兑现改稿。Spread使用精简的四段正文、24px/1.72和880px主图，使正文与图注保留独立页脚空间。

## 系统与快照
field-system含token、本地字体、Masthead、EditorialCaption、EventBadge三个实际DOM组件与Cover组合预览。通过原生design-systems接口安装，canvas.json记录来源，ds/fieldnotes保存token与字体版本快照；它不自动同步，更新需重新安装。画布属性内联，可直接选取、重排与改字。

## 重建与导出
source/build_field.py恢复六板初稿，不需网络生成图；素材须先存在shared-assets/field-botanical.png。--source-only可先恢复源文件。运行会覆盖手工编辑，仅恢复时使用。使用tingly-design@0.26.1021打开；dc.html依赖原生support.js运行时。官方check --snapshots输出renders/check；export --as png --scale 2输出可保留二倍像素的成品，最后将@2x后缀规范为画板stem。

## 字体与许可
Field Sans为本地Noto Sans SC，Field Serif为本地URW P052。项目fonts内保留许可，均不依赖网络字体。

## 当前验证与恢复说明
本次工作区恢复后重新执行原生new、安装、check和scale=2导出。两项目原生创建回执在source/native_creation.json。系统check无问题；画布仅Before保留预期的对比警告。组件四个函数已实际浏览器调用并返回HTMLElement，截图在field-system/renders/components/ActualComponents.png。六张最终图保存在renders/export/{Main,Spread,Rules,Exhibition,Before,CropStudies}.png，名称移除CLI默认@2x后缀，像素仍是二倍。

原AI文件随工作区回滚丢失，本次植物画重新生成，画面构图与旧图有差异；六板版式、文案与已修复的跨页保持恢复，仅调整了封面和第二幅裁切的焦点以适应新图。
