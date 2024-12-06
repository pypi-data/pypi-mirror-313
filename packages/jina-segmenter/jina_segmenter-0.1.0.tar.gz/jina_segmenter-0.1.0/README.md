# Jina Segmenter

一个基于 Jina AI API 的智能文本分段工具。它能够智能地将长文本分割成合适大小的片段，同时保持语义的完整性。

## 特性

- 智能文本分段，保持语义完整性
- 自动计算和优化分片大小
- 支持自定义最大分片大小
- 返回每个分片的 token 数量
- 简单易用的 API

## 安装

```bash
pip install jina-segmenter
```

## 使用方法

首先，你需要设置 Jina AI 的 API key：

```python
import os
os.environ['JINA_API_KEY'] = 'your_jina_api_key'
```

然后你就可以使用分段功能：

```python
from jina_segmenter import segment_text

text = "你的长文本..."
chunks = segment_text(text)  # 默认最大分片大小为 1500 tokens

# 查看分片结果
for i, chunk in enumerate(chunks, 1):
    print(f"片段 {i} (tokens: {chunk['tokens']}):")
    print(chunk['text'])
    print("-" * 30)
```

你也可以自定义最大分片大小：

```python
chunks = segment_text(text, max_chunk_size=1000)
```

## 获取 API Key

1. 访问 [Jina AI](https://jina.ai/)
2. 注册并登录你的账号
3. 在控制台中创建新的 API key

## 依赖

- Python >= 3.6
- requests >= 2.31.0

## 许可证

MIT License

## 作者

WSY (wangshuyue@gmail.com)
