---
title: "ZeRO 系列论文学习"
collection: blog
type: "blog"
date: 2026-01-17
excerpt: '学习 ZeRO 系列论文，深入理解分布式训练中的优化技术。'
location: "Shanghai, China"
---

大模型分布式训练中, ZeRO (Zero Redundancy Optimizer) 系列论文提出了一系列创新的方法来优化内存使用和计算效率. 它是在没有Pipeline并行的情况下, 通过分布式存储和计算来实现大规模模型训练的关键技术. 下面是对 ZeRO 系列论文的学习总结.

---

## ZeRO: Memory Optimizations Toward Training Trillion  Parameter Models


### where did all the memory go?

- parameters
- gradients
- optimizer states
- activations
- temporary buffers

example: Adam. Adam需要存储参数, 两个动量项(一阶和二阶), 以及梯度. 这意味着每个参数需要4倍的内存.

#### Trick1: mixed precision training

| 内容                  | 用 FP16/FP32 |
| ------------------- | ----------- |
| forward/backward 权重 | FP16        |
| 激活                  | FP16        |
| 梯度累积                | FP32        |
| optimizer 状态（m/v）   | FP32        |
| master weight 副本    | FP32        |

Mixed precision training of a model with Ψ parameters using Adam requires enough memory to hold an f p16 copy of the parameters and the gradients, with memory requirements of 2Ψ and 2Ψ bytes respectively. In addition, it needs to hold the optimizer states: an f p32 copy of the parameters, momentum and variance, with memory requirements of 4Ψ, 4Ψ, and 4Ψ bytes, respectively.

Let’s use K to denote the memory multiplier of the optimizer states, i.e., the additional memory required to store them is KΨ bytes. Mixed-precision Adam has K = 12. In total, this results in 2Ψ + 2Ψ + KΨ = 16Ψ bytes of memory requirement. For a model such as GPT-2 with 1.5 Billion parameters, this leads to a memory requirement of at least 24 GB, which is significantly higher than the meager 3 GB of memory required to hold the f p16 parameters alone.

#### Residual memory

* 对 Transformer/GPT 这种模型来说：

  * 每一层都有 hidden states：`hidden_states[layer] = seq_len × hidden_dim × batch_size × dtype`
  * forward 计算时，需要 **保留所有层的 hidden states** 以便 backward 计算梯度
  * Attention 还需要保存 **key/value cache**
* **公式示意**：
   $$
  \text{activation mem} \approx batch_size \times seq_len \times hidden_dim \times num_layers \times sizeof(dtype)
  $$

* 因为 batch size × seq_len × num_layers 可能非常大，所以 activation 内存远远超过参数量（尤其是 FP16，参数量较小）

**example:**

* GPT-2 1.5B 参数

  * seq_len = 1K, batch size = 32 → activation 内存 ≈ 60 GB
  * 说明 activation 占用几乎是参数的几十倍

---

** Activation Checkpointing（重计算）**

* **核心思想**：

  * **不保存每层 activation**，只保存少量“checkpoint”节点
  * backward 时，如果某些 activation 不存在，就 **重新计算 forward** 来得到它

* **显存效果**：

  * activation 内存大约减小到 **√(总 activations)**
  * 对 GPT-2 1.5B：

    * 原始 activation ≈ 60 GB
    * checkpoint 后 ≈ 8 GB

* **代价**：

  * 约 **33% 的额外计算**（因为部分 forward 被重复计算）

---

** 大模型仍然显存爆炸**

* 对 100B 参数 GPT-like 模型：

  * batch size 32，即便用 activation checkpointing → activation 仍然需要 ~60 GB
  * 原因：

    1. 参数太多 → hidden_dim / layer 数量极大
    2. batch size 和 seq_len 大 → 激活数量巨增
* 所以 **activation 仍然是显存瓶颈**，甚至比参数和 optimizer 状态更严重

---
