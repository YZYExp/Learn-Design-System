# 字体

`NotoSansSC-Regular.ttf`：Noto Sans CJK 项目的简体中文字体。由官方可变 TrueType 版本按 wght=400 静态实例化，不裁删字形。

- 官方源文件：https://github.com/notofonts/noto-cjk/blob/main/Sans/Variable/TTF/Subset/NotoSansSC-VF.ttf
- 源项目：https://github.com/notofonts/noto-cjk
- 许可：SIL Open Font License 1.1，随附 `OFL.txt`。
- 实例化：`fontTools.varLib.instancer.instantiateVariableFont(font, {'wght':400})`。

PDF 嵌入所用字形，程序教学图使用同一字体；最终 PDF 不要求阅读设备自行安装中文字体。
