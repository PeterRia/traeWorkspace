# 附录 A：AI 基础

## 01 AI 进化史

从规则系统到深度学习，从 GPT 到多模态大模型的发展历程。

### 关键里程碑
- 1950s：图灵测试 - AI 概念的诞生
- 2012：AlexNet - 深度学习革命
- 2017：Transformer 架构 - 现代 LLM 的基础
- 2022：ChatGPT - AI 对话时代开启
- 2024：多模态大模型 - 图文音视频全能

> 参考：https://datawhalechina.github.io/easy-vibe/zh-cn/appendix/8-artificial-intelligence/ai-history

---

## 02 提示词工程

### 什么是提示词工程？
设计和优化给 AI 的输入指令，以获得更好的输出结果。

### 核心技巧
1. **角色设定**：给 AI 一个明确的角色
   ```
   你是一个资深的前端开发工程师...
   ```
2. **结构化要求**：指定输出格式
   ```
   请用表格形式列出...
   ```
3. **分步引导**：链条式思考
   ```
   第一步...第二步...
   ```
4. **示例引导**：提供期望的样例
   ```
   类似这样的格式：[示例]
   ```

> 参考：https://datawhalechina.github.io/easy-vibe/zh-cn/appendix/8-artificial-intelligence/prompt-engineering

---

## 03 大语言模型原理

### 核心概念
- **Token**：LLM 处理的最小文本单元
- **上下文窗口**：模型一次能处理的 Token 数量上限
- **Temperature**：控制输出的随机性（0=确定，1=创意）
- **Embedding**：将文本转换为向量表示

### 主流模型对比

| 模型 | 特点 | 适用场景 |
|------|------|---------|
| GPT-4o | 多模态，综合能力强 | 通用开发 |
| Claude 3.5 | 长上下文，代码能力强 | 编程任务 |
| Gemini | 谷歌生态整合 | Google 用户 |
| GLM | 国产开源 | 中文场景 |

> 参考：https://datawhalechina.github.io/easy-vibe/zh-cn/appendix/8-artificial-intelligence/llm-principles

---

## 04 Agent 智能体

### 什么是 Agent？
能感知环境、制定计划、使用工具、执行行动的 AI 系统。

### Agent 核心能力
- **规划**：分解复杂任务
- **工具调用**：使用外部 API 和工具
- **记忆**：存储和检索历史信息
- **反思**：评估输出质量并自我修正

### Vibe Coding 中的 Agent
在 Vibe Coding 中，Agent 就是你的 AI 开发队友。你描述任务，Agent 理解、规划、执行。

> 参考：https://datawhalechina.github.io/easy-vibe/zh-cn/appendix/8-artificial-intelligence/ai-agents