# 幻彩滑动拼图

这是一个用于课程作业的 Python 滑动拼图游戏。项目使用 `pygame` 创建窗口、处理事件、绘制界面和播放音效；使用 Pillow 加载、生成、裁剪、切割图片并生成成绩卡；使用 `random` 从完成状态执行合法移动来打乱棋盘，保证每局可解；使用 `os.path` 兼容源码运行和 PyInstaller exe 路径；使用 `datetime` 记录成绩日期、生成成绩卡文件名和水印。

## 运行

```bat
python -m pip install -r requirements.txt
python tools\generate_assets.py
python main.py
```

也可以双击 `run_game.bat`。

## 测试

```bat
python -m py_compile main.py src\*.py tools\*.py
python -m unittest discover -s tests
python tools\generate_assets.py
python tools\smoke_test.py
python tools\package_check.py
```

PowerShell 不会稳定展开 `src/*.py`，若通配符失败，可用：

```powershell
python -m py_compile main.py (Get-ChildItem src,tools -Filter *.py).FullName
```

## 打包 exe

双击 `build_exe.bat`，或在项目根目录执行：

```bat
pyinstaller --noconfirm --windowed --name PuzzleGame --add-data "assets;assets" main.py
```

成功后 exe 位于 `dist\PuzzleGame\PuzzleGame.exe`。exe 运行时，存档写到 exe 同级的 `saves\save_data.json`，不会写入 `sys._MEIPASS`。

## 功能完成情况

A 级已完成：主菜单、选图、选难度、游戏中、暂停、胜利结算、图片切块、可解打乱、点击移动、胜利判断、原图参考、计时计步、重新开局、本地 JSON 存档、README、用户手册、requirements、`run_game.bat`、`build_exe.bat`。

B 级已完成或基本完成：图鉴冒险、成就系统、H 键高亮可移动拼块、G 键曼哈顿距离提示、Ctrl+Z/Ctrl+Y 撤销重做、基础音效、评级、成绩卡片。

C 级降级说明：未实现拖拽操作、旋转模式、限时挑战、限步挑战；胜利判断已预留 rotation 字段，标准模式中 rotation 恒为 0。动态背景和胜利粒子已做轻量实现。

## 资源说明

项目使用 `imagegen` 生成正式美术资源：`assets/images/imagegen_cover.png` 以及 6 张主题拼图图。完整提示词保存在 `assets/images/IMAGEGEN_PROMPTS.md`。若主题资源缺失，`src/asset_generator.py` 仍会用 Pillow 自动生成 6 张备用图片，并用 `wave`/`math` 自动生成 `move.wav`、`click.wav`、`error.wav`、`win.wav`。

## 存档内容

存档文件为 `saves/save_data.json`，保存设置、图鉴解锁、完成次数、排行榜、最佳时间、最少步数、成就和最近成绩。若 JSON 损坏，程序会自动备份为 `save_data.json.broken_YYYYMMDD_HHMMSS.bak` 并重建。排行榜键采用 `image_id + difficulty + mode`。

## 压缩交付

在 `pintuGame` 目录中，将 `puzzle_game` 文件夹压缩为 `学号姓名.rar`。Windows 没有内置 rar 压缩器，可使用 WinRAR/7-Zip 的“添加到压缩文件”，格式选择 RAR，文件名填写 `学号姓名.rar`。
