# 附录 E：开发工具基础

## 01 Git 版本控制

### 核心概念
- **仓库 (Repository)**：代码的存储空间
- **提交 (Commit)**：代码的一次快照
- **分支 (Branch)**：独立的开发线
- **合并 (Merge)**：合并不同分支的代码
- **推送 (Push)**：上传本地代码到远程

### 基本工作流
```bash
git add .                    # 暂存所有更改
git commit -m "描述修改"      # 提交更改
git push origin main         # 推送到远程
```

### Vibe Coding 中的 Git
- AI 可以帮你生成 commit message
- 使用 GitHub Desktop 降低 Git 操作门槛

> 参考：https://datawhalechina.github.io/easy-vibe/zh-cn/appendix/2-development-tools/git-version-control

---

## 02 计算机网络基础

### 核心概念

| 概念 | 说明 |
|------|------|
| IP 地址 | 设备的网络地址 |
| 域名 | IP 的人类可读版本 |
| DNS | 域名→IP 的解析服务 |
| HTTP/HTTPS | 网页数据传输协议 |
| 端口 | 同一设备上的不同服务入口 |
| CDN | 内容分发网络（加速访问） |

### HTTP 请求流程
```
浏览器输入 URL → DNS 解析 → 建立连接 → 发送请求 → 服务器处理 → 返回响应 → 浏览器渲染
```

### Vibe Coding 相关概念
- `localhost:3000`：本地开发服务器
- API 请求：前端→后端的通信
- CORS：跨域资源共享（常见部署问题）
- SSL/TLS：HTTPS 加密（上线需要）

> 参考：https://datawhalechina.github.io/easy-vibe/zh-cn/appendix/1-computer-fundamentals/computer-networks