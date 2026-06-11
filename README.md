# AgentCenter Talks 📊

[English](README.md) | [中文](README.zh.md)

## Overview

**AgentCenter Talks** is a unique open-source project that documents the complete development process of the [agent-center](https://github.com/oopslink/agent-center) project through conversations and interactions between developers and AI agents.

This repository contains:
- **491 conversation channels** exported from the development process
- **Complete chat history** showing how the project was built entirely through AI-driven development
- **Interactive visualization** to explore the development journey
- A remarkable case study: **developers never reviewed a single line of code** during the entire development lifecycle

### Key Characteristics

🤖 **AI-Driven Development**: The entire `agent-center` project was developed through conversations with AI agents
📝 **Complete Transparency**: All development discussions and decisions are preserved
🎯 **Zero Code Review**: No traditional code reviews - pure AI collaboration
📊 **Visualization Tools**: Interactive HTML mockup to explore conversation graphs
🌍 **Multilingual Data**: Conversations primarily in Chinese with English documentation

## Project Structure

```
talks-on-project-agent-center/
├── data/
│   ├── talks/                    # 491 JSON files containing conversation data
│   │   └── channel-*.json        # Individual channel export (messages, metadata, etc.)
│   └── talks_副本/               # Backup copies of channel data
├── docs/                         # GitHub Pages static site
├── LICENSE                       # MIT License
├── README.md                     # English documentation
└── README.zh.md                  # Chinese documentation
```

## Data Format

Each channel JSON file contains structured conversation data:

```json
{
  "channelId": "UUID",
  "exportedAt": "ISO 8601 timestamp",
  "total": 1164,
  "messages": [
    {
      "id": "message UUID",
      "seq": 5165861,
      "channelId": "channel UUID",
      "senderType": "user" | "agent",
      "senderId": "user UUID",
      "messageType": "chat",
      "content": "message text",
      "createdAt": "ISO 8601 timestamp",
      "updatedAt": "ISO 8601 timestamp",
      "senderName": "sender display name",
      "reactions": [],
      "mentions": [],
      "attachments": []
    }
  ]
}
```

## Getting Started

### Viewing the Data

1. **Interactive Visualization**:
   Visit the online dashboard at: https://oopslink.github.io/talks-on-project-agent-center/

2. **Direct Access**:
   Browse the JSON files in the `data/talks/` directory directly

### Analyzing the Data

The data is structured JSON and can be easily processed with any programming language:

```javascript
// Example: Node.js
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data/talks/channel-*.json', 'utf8'));
console.log(`Total messages: ${data.total}`);
data.messages.forEach(msg => {
  console.log(`${msg.senderName}: ${msg.content}`);
});
```

```python
# Example: Python
import json
import glob

for file_path in glob.glob('data/talks/channel-*.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"Channel: {data['channelId']}")
        print(f"Messages: {data['total']}")
```

## Statistics

- **491** conversation channels
- **~1M+** total messages across all channels
- **62MB** of structured conversation data
- **5+ months** of continuous development discussions
- **100%** AI-driven development process

## Use Cases

This dataset is valuable for:

📚 **Research**: Study AI-assisted software development patterns
🔬 **Analysis**: Understand how AI and humans collaborate effectively
📖 **Case Study**: Learn from a real-world AI-native development process
🎓 **Education**: See practical examples of domain-driven design (DDD) discussions
🤝 **Community**: Reference for AI collaboration best practices

## Visualization Features

The interactive dashboard at https://oopslink.github.io/talks-on-project-agent-center/ provides:

- **Channel Overview**: Statistics on total channels and message counts
- **Graph View**: Visualization of conversation relationships
- **Search**: Find specific discussions across all channels
- **Layout Options**: Force-directed and hierarchical layout views
- **Interactive Navigation**: Zoom, pan, and explore the conversation network

## Key Discussion Topics

The conversations cover various aspects of the `agent-center` project:

- **Domain-Driven Design (DDD)**: Bounded contexts, entities, aggregates
- **System Architecture**: Microservices, event-driven design
- **UI/UX Design**: Members interface, identity boundaries
- **Code Development**: Implementation strategies without direct code review
- **Project Planning**: Requirements gathering and refinement

## Contributing

While this is primarily a documentation repository, we welcome:

- Issues and corrections to the data
- Documentation improvements
- Tool enhancements for visualization and analysis
- Insights and analysis of the development process

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this dataset in your research or projects, please cite using one of the following formats:

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

OopsLinK. (2026). AgentCenter Talks: AI-Driven Development Process Documentation. Retrieved from https://github.com/oopslink/talks-on-project-agent-center

### Chicago

OopsLinK. "AgentCenter Talks: AI-Driven Development Process Documentation." GitHub. Accessed 2026. https://github.com/oopslink/talks-on-project-agent-center

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

## Related Projects

- [Agent Center](https://github.com/oopslink/agent-center) - The main project developed through these conversations
- [Claude Code](https://github.com/anthropics/claude-code) - The AI development platform used

## Acknowledgments

Special thanks to:
- **[slock.ai](https://slock.ai)** - The primary AI development platform that powered the entire agent-center project development
- All participants in the development process
- The AI models and frameworks that made this unique development approach possible

---

**Made with ❤️ by developers and AI | Built with [slock.ai](https://slock.ai)**
