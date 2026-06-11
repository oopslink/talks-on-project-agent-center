# AgentCenter Talks 📊

[English](README.md) | [中文](README.zh.md)

## 项目简介

**AgentCenter Talks** 是一个独特的开源项目，记录了 [agent-center](https://github.com/oopslink/agent-center) 项目从开发人员与 AI 代理之间的对话完整开发过程。

本仓库包含：
- **491 个对话频道** 导出自开发过程
- **完整的聊天记录** 展示项目如何完全通过 AI 驱动开发完成
- **交互式可视化工具** 用于探索开发过程
- 一个非凡的案例研究：**整个开发生命周期中，开发人员从未查看过任何一行代码**

### 项目特点

🤖 **AI 驱动开发**：整个 `agent-center` 项目通过与 AI 代理的对话开发完成
📝 **完全透明**：所有开发讨论和决策都被保留
🎯 **零代码审查**：无传统代码审查 - 纯 AI 协作
📊 **可视化工具**：交互式 HTML 模型来探索对话图表
🌍 **多语言数据**：对话主要使用中文，文档使用英文

## 项目结构

```
talks-on-project-agent-center/
├── data/
│   ├── talks/                    # 491 个 JSON 文件，包含对话数据
│   │   └── channel-*.json        # 单个频道导出（消息、元数据等）
│   └── talks_副本/               # 频道数据的备份副本
├── mockup.html                   # 交互式可视化仪表板
├── LICENSE                       # MIT 许可证
├── README.md                     # 英文文档
└── README.zh.md                  # 中文文档
```

## 数据格式

每个频道 JSON 文件包含结构化的对话数据：

```json
{
  "channelId": "UUID",
  "exportedAt": "ISO 8601 时间戳",
  "total": 1164,
  "messages": [
    {
      "id": "消息 UUID",
      "seq": 5165861,
      "channelId": "频道 UUID",
      "senderType": "user" | "agent",
      "senderId": "用户 UUID",
      "messageType": "chat",
      "content": "消息文本",
      "createdAt": "ISO 8601 时间戳",
      "updatedAt": "ISO 8601 时间戳",
      "senderName": "发送者显示名称",
      "reactions": [],
      "mentions": [],
      "attachments": []
    }
  ]
}
```

## 快速开始

### 查看数据

1. **交互式可视化**：
   ```bash
   # 在浏览器中打开 mockup.html
   open mockup.html
   ```

2. **直接访问**：
   直接浏览 `data/talks/` 目录中的 JSON 文件

### 分析数据

数据为结构化 JSON，可以使用任何编程语言轻松处理：

```javascript
// 示例：Node.js
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/talks/channel-*.json', 'utf8'));
console.log(`总消息数：${data.total}`);
data.messages.forEach(msg => {
  console.log(`${msg.senderName}：${msg.content}`);
});
```

```python
# 示例：Python
import json
import glob

for file_path in glob.glob('data/talks/channel-*.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"频道：{data['channelId']}")
        print(f"消息数：{data['total']}")
```

## 数据统计

- **491** 个对话频道
- **100万+** 条消息分布在所有频道中
- **62MB** 的结构化对话数据
- **5 个多月** 的持续开发讨论
- **100%** AI 驱动的开发过程

## 使用场景

该数据集对以下用途很有价值：

📚 **研究**：研究 AI 辅助软件开发模式
🔬 **分析**：理解 AI 和人类如何有效协作
📖 **案例研究**：学习真实的 AI 原生开发流程
🎓 **教育**：查看领域驱动设计（DDD）讨论的实际示例
🤝 **社区**：AI 协作最佳实践参考

## 可视化功能

`mockup.html` 提供：

- **频道概览**：显示频道总数和消息数统计
- **图表视图**：对话关系的可视化
- **搜索功能**：在所有频道中查找特定讨论
- **布局选项**：力导向图和分层布局视图
- **交互式导航**：缩放、平移和探索对话网络

## 主要讨论话题

对话涵盖了 `agent-center` 项目的各个方面：

- **领域驱动设计（DDD）**：有界上下文、实体、聚合
- **系统架构**：微服务、事件驱动设计
- **UI/UX 设计**：成员界面、身份边界
- **代码开发**：无直接代码审查的实现策略
- **项目规划**：需求收集和优化

## 贡献

虽然这主要是一个文档仓库，但我们欢迎：

- 问题报告和数据更正
- 文档改进
- 可视化和分析工具增强
- 对开发过程的见解和分析

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 引用

如果您在研究或项目中使用此数据集，请使用以下格式之一引用：

### BibTeX

```bibtex
@dataset{agentcenter_talks,
  title={AgentCenter Talks: AI-Driven Development Process Documentation},
  author={OopsLinK},
  year={2026},
  url={https://github.com/oopslink/talks-on-project-agent-center}
}
```

### APA

OopsLinK. (2026). AgentCenter Talks: AI-Driven Development Process Documentation. 取自 https://github.com/oopslink/talks-on-project-agent-center

### Chicago

OopsLinK. "AgentCenter Talks: AI-Driven Development Process Documentation." GitHub. 访问日期 2026. https://github.com/oopslink/talks-on-project-agent-center

### MLA

OopsLinK. "AgentCenter Talks: AI-Driven Development Process Documentation." GitHub, 2026, github.com/oopslink/talks-on-project-agent-center.

### RIS

```
TY  - DATA
AU  - OopsLinK
TI  - AgentCenter Talks: AI-Driven Development Process Documentation
PY  - 2026
UR  - https://github.com/oopslink/talks-on-project-agent-center
ER  -
```

## 相关项目

- [Agent Center](https://github.com/oopslink/agent-center) - 通过这些对话开发的主项目
- [Claude Code](https://github.com/anthropics/claude-code) - 使用的 AI 开发平台

## 致谢

特别感谢：
- **[slock.ai](https://slock.ai)** - 驱动整个 agent-center 项目开发的主要 AI 开发平台
- 所有参与开发过程的参与者
- 使这种独特开发方式成为可能的 AI 模型和框架

---

**由开发者和 AI 共同完成 | 由 [slock.ai](https://slock.ai) 提供支持**
