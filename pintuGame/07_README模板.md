# README 模板

> 该文件可直接作为 Codex 生成项目后的 `README.md` 模板。

# 拼图冒险 Puzzle Game

## 1. 项目简介

这是一个基于 Python、pygame 和 Pillow 实现的滑动拼图游戏。游戏支持多张图片、3x3/4x4/5x5 难度、可解性打乱、原图参考、计时计步、提示、撤销、图鉴解锁、本地记录、成绩卡片和 exe 打包。

## 2. 功能亮点

- 使用 Pillow 自动生成和切割图片。
- 使用 pygame 完成窗口、绘制、事件和音效。
- 使用 random 进行可解随机打乱。
- 使用 os.path 兼容源码和 exe 资源路径。
- 使用 datetime 记录成绩日期并生成成绩卡片。
- 支持图鉴、成就、排行榜、提示、撤销、重新开局。

## 3. 环境要求

- Python 3.10 或更高版本。
- Windows 10/11 推荐。

安装依赖：

```bat
python -m pip install -r requirements.txt
```

## 4. 运行方式

首次运行前建议生成默认素材：

```bat
python tools\generate_assets.py
```

启动游戏：

```bat
python main.py
```

或双击：

```text
run_game.bat
```

## 5. 打包 exe

执行：

```text
build_exe.bat
```

打包完成后，在 `dist/` 目录中找到 exe。

## 6. 目录结构

```text
puzzle_game/
├── main.py
├── requirements.txt
├── README.md
├── 用户手册.md
├── assets/
├── src/
├── saves/
├── screenshots/
├── tests/
├── tools/
└── dist/
```

## 7. 测试命令

```bat
python -m py_compile main.py src\*.py tools\*.py
python -m unittest discover -s tests
python tools\smoke_test.py
python tools\package_check.py
```

## 8. 交付说明

课程提交时，请将完整 `puzzle_game/` 文件夹和 `dist/` 内 exe 一起压缩为：

```text
学号姓名.rar
```

例如：

```text
25331021张三.rar
```

## 9. 常见问题

### exe 无法读取图片

请检查 PyInstaller 命令是否包含：

```bat
--add-data "assets;assets"
```

### 音效无法播放

如果当前电脑没有可用音频设备，游戏会自动静音，不影响游玩。

### 存档在哪里

源码运行时在项目内 `saves/`。exe 运行时在 exe 同级目录的 `saves/`。
