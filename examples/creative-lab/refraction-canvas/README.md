# 折光 V5：从完整提案到原生画板

先用imagegen探索完整海报，确认中文宋体、纸白与蓝青/金红光场，再从同一提案去字得到素材，最后将标题、日期、地点与图形重新做成可编辑层。不是把整张AI海报作为背景后盖几行字。

完整提案：../shared-assets/refraction-concept-v5.png；无字底图：../shared-assets/refraction-light-v5.png。宋体为Noto Serif CJK SC Medium（OFL），拉丁衬线为Nimbus Roman（URW许可），正文使用Noto Sans SC（OFL）。实际字形与AI提案略有区别，不宣称逐像素复刻。

当前七块画板：海报、邀请、三页提案、视觉规则与V4→V5对照。所有活动、地址与时间为教学虚构。V4对照为旧版真实导出，非构造的坏稿；新稿由无字素材与原生层组成。

三个真实组件：ExhibitTitle、InfoStrip、PictureFrame。双主题与安装快照保留；更新上游不自动改写已排版的内联值。build_refraction_v5.py重建当前原生源；refresh_refraction_tokens.py调用原生服务编译CSS。原生check/export重新生成截图。

CLI 0.26.1021的PNG导出需要操作系统安装随附Noto Serif CJK SC字体（fonts/RefractionSong.otf）；Linux安装后运行fc-cache。编辑器字体由工程内文件加载。
