# V5仓库导入记录

- 目标仓库：YZYExp/Learn-Design-System（保留私有可见性）。
- 初始化提交：b804ad9d4fbfd85f46ab20d338b3d1c9160d3308，仅包含零字节README.md。
- 导入基线：原工程V5提交c1764f3ec590153414d79b56d5c66cd21cd32144。
- 本次为干净导入；导入前完整1.0—5.0历史保留在此前交付的版本历史.bundle，不把旧根提交并入新仓库。
- 保留33个正文章、导读、3附录、全部正文引用图、字体及许可、三套系统、三套Canvas、生成脚本、AI生成记录与验证报告。
- 排除可再生的V3/check截图与临时PNG；保留可编辑源文件和书中实际使用的对照图。
- PDF基线：236页，187次配图，178张独立图像，SHA256 f150752352f1b29826e82130e5c57683eeede069484e2399a4f30f9185efcd1b。完整AI提案193页、原生Main196页、方向对照199页。
- 历史验证报告记录导入前的实际构建；今后重新排版后应更新当前报告。

## 使用

Python 3.12安装requirements.txt后运行scripts/build_book.py；源图均已附带，无需先重新生成图片。构建完成运行scripts/check_book.py --render及scripts/check_book_embedding.py。

GitHub Actions的PDF构建不重新生成AI图像，不需要AI账号或密钥。原生画板用Tingly Design 0.26.1021打开，具体命令和字体安装说明见工坊README。

完整V5宋体以三个二进制分片版本管理；scripts/restore_native_fonts.py校验SHA256并还原原来三个字体路径，字形与覆盖范围均保留。
