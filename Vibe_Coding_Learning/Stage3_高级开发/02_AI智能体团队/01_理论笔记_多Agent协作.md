# 02 AI 智能体团队 - 理论笔记：多 Agent 协作

## 核心理念

用多个 AI Agent 协作完成大型开发任务。每个 Agent 有专门的职责，通过通信协作完成任务。

## Claude Agent Teams

```
项目负责人 Agent
├── 前端开发 Agent → 负责 UI/UX 实现
├── 后端开发 Agent → 负责 API 和数据库
├── 测试 Agent → 负责代码测试和验证
└── 文档 Agent → 负责文档生成
```

## 多 Agent 协作原则

1. **职责单一**：每个 Agent 聚焦一个领域
2. **明确接口**：Agent 之间的输入输出需要标准化
3. **分步执行**：大任务拆成小步骤，按序执行
4. **结果验证**：Agent 产出需要经过验证

## Vibe Coding 中的应用

- 用自然语言描述 Agent 的角色和任务
- 多个 Agent 并行工作，AI 负责协调
- 你是"产品经理"，Agent 团队是"开发团队"

参考：https://datawhalechina.github.io/easy-vibe/zh-cn/stage-3/core-skills/agent-teams/