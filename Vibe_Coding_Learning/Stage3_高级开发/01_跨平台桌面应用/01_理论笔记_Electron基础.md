# 01 跨平台桌面应用 - 理论笔记：Electron 基础

## 什么是 Electron？

使用 Web 技术（HTML/CSS/JavaScript）构建跨平台桌面应用的框架。一次开发，同时运行在 Windows、macOS、Linux。

## 核心架构

```
主进程 (Main Process)
├── 创建窗口
├── 系统交互（文件系统、通知等）
└── IPC 通信
    ↕
渲染进程 (Renderer Process)
├── HTML/CSS/JS 界面
└── 类似浏览器的工作方式
```

## Electron 的优势

| 优势 | 说明 |
|------|------|
| 跨平台 | 一次开发，三端运行 |
| Web 技术 | Vibe Coding 已掌握的技术栈 |
| 生态丰富 | 大量插件和模板 |
| AI 友好 | 可用 Vibe Coding 辅助开发 |

## 适用场景
- 桌面工具类应用（语音转文字、图片处理等）
- 企业内部工具
- 个人效率工具

参考：https://datawhalechina.github.io/easy-vibe/zh-cn/stage-3/cross-platform/electron-voice-to-text/