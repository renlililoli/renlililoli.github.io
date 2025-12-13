---
title: "LLM"
collection: blog
type: "blog"
date: 2025-11-02
excerpt: '学点大模型'
location: "Shanghai, China"
---

## Inference

大模型推理相关.

最近在看 [llama.cpp](https://github.com/ggml-org/llama.cpp), 感觉是相当有趣的项目, 纯c++实现了llama模型的推理, 并且支持量化. 最重要的是完全不依赖于blas库, 纯手搓算子. 内部不包含任何的卷积等不会在transformers模型中出现的操作.

### 快速上手

`llama.cpp`使用非常的简单, 从源仓库clone下来, 然后编译, 因为是完全独立的, 所以也不需要任何别的库, 尽管可以link blas 或者cublas等.

主要的功能在`llama-cli`中暴露了接口, 直接运行
```bash
./llama-cli --model ./models/7B/ggml-model-q4_0.ggml -t <core> --context-shifted -n <max context len>
```
就能进入交互式的对话模式, 其中`-t`指定使用的cpu核心数, `--context-shifted`表示使用shifted的上下文机制, `-n`表示上下文的最大长度.

我个人使用体验是7B模型在使用EPYC9754的128核心上非常流畅.

但是比较奇怪的是Q4_0量化的模型效果非常差, 几乎全是乱码, Q8就正常了, 感觉是量化的bug或者是cpu不支持某些指令集的缘故.

`llama.cpp`还支持server和webui模式,都很好用.


## LLM-RL

本科的时候学过一点强化学习, 所以想看看大模型和强化学习结合的东西. 之前看过很多qwen系列的文章和相关的博客,
也看过deepseek的一些介绍, 所以想看看LLM-RL的东西, 具体是什么样子的.

## 相关工作

准备看这篇survay文章:
[Reinforcement Learning Enhanced LLMs: A Survey](https://arxiv.org/abs/2412.10400)

找了一些知名高star的项目, 包括:
- [verl](https://github.com/volcengine/verl)
- [rllm](https://github.com/rllm-org/rllm)
- [ROLL](https://github.com/alibaba/ROLL)
- [lamorel](https://github.com/flowersteam/lamorel)
- [verifiers](https://github.com/PrimeIntellect-ai/verifiers)



