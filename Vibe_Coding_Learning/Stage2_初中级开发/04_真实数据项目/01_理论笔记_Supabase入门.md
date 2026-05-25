# 04 真实数据项目 - 理论笔记：Supabase 入门

## 什么是 Supabase？

Supabase 是一个开源的 Firebase 替代品，提供：
- PostgreSQL 数据库
- 用户认证系统
- 实时数据订阅
- 自动生成的 RESTful API
- 文件存储

## 核心能力

### 数据库设计
- 创建数据表
- 设置字段类型和约束
- 定义表之间的关系
- 配置行级安全策略（RLS）

### 权限管理
- 用户角色设置
- 数据访问权限控制
- 公开/私有数据分离

## 为什么选 Supabase？

| 优势 | 说明 |
|------|------|
| 免费额度 | 适合学习和 MVP 阶段 |
| SQL 数据库 | 标准 PostgreSQL，学习迁移成本低 |
| 自带 API | 不用写后端代码即可 CRUD |
| 实时更新 | 订阅数据变化，自动更新 UI |
| AI 友好 | 结构与 AI 协作开发契合 |

参考：https://datawhalechina.github.io/easy-vibe/zh-cn/stage-2/backend/database-supabase/