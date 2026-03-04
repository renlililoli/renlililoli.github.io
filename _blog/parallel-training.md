---
title: "并行训练"
collection: blog
type: "blog"
date: 2026-03-02
excerpt: "Notes on playing with the UltraScale Playbook."
location: "Shanghai, China"
---

基于 [UltraScale Playbook](https://github.com/nanotron/nanotron) 的内存估算工具，可预测 LLM 训练过程中的内存消耗：

<iframe 
  src="{{ '/files/memory-estimator/' | relative_url }}"
  width="100%" 
  height="900"
  style="border:none; border-radius:12px; overflow:hidden; min-height:800px;">
</iframe>

## DP，TP，PP 都比较常见，省略

## Sequence Parallelism

部分的操作是tokenwise的，比如layernorm，residual，gelu等，这些操作可以被并行化。这样我们就可以把一个batch的token分配到多张卡上，从而实现token级别的并行。但是坏处是在attention时需要进行通信把激活值传递给其他卡，这样会导致通信开销增加。by the way， attention部分来自于激活的peak mem占用没有减少。这部分只有TP

### ring attention

事实上也可以在seq维度对attention进行拆分， ring attention是一个非常经典的方案， 能够很好的计算通信重叠。并且能达到理论最大带宽。

主要的想法就是

$$
O_i = A_i V = softmax(Q_i K^T/sqrt(d)) V = \sum_{j=0}^{N-1} softmax(Q_i K_{j}^T/sqrt(d)) V_{j}
$$

注意这里的softmax是分块进行的， 而不是整个矩阵。因此需要不断的对softmax中的全局因子进行更新。为了简单起见，省略$sqrt(d)$因子。

核心就是来自于online的softmax merge。

W.l.o.g., suppose $O_i$ only has one row, (little subtle since in linear algebra the token dim is the colomn but in the context of attention it's the row), then we can only get the block unnormalized attention scores $A_i^{(j)} = Q_i K_{j}^T$, which is a $1 \times \frac{N}{P}$ matrix.

Recall the online softmax merge algorithm:

$$
softmax(u_{:k})_i = \frac{e^{u_i - max(u_{:k})}}{\sum_{j=0}^{k} e^{u_j - max(u_{:k})}} = \frac{e^{u_i - max(u_{:k})}}{s_k}
$$

$$
softmax(u_{:k+b})_i = \frac{e^{u_i - max(u_{:k+b})}}{\sum_{j=0}^{k+b} e^{u_j - max(u_{:k+b})}} = \frac{e^{u_i - max(u_{:k+b})}}{s_{k+b}} \\= \frac{e^{u_i - m_k} e^{m_k - m_{k+b}}}{s_k \times e^{m_{k} - m_{k+b}} + s_{k+b:k+b} \times e^{m_{k:k+b} - m_{k+b}}}
$$

where $m_k = max(u_{:k})$. Therefor we can update the softmax block by blcok.

This trick is also used in the implementation of the flash attention.

When the $O_i$ has multiple rows, just make the m be a vector.

Backward is similar, just recompute the attention scores and gradients.

**Problems**

The attention has masks, so the workload is unbalanced.

### Zigzag attention

Zigzag attention is a variant of the ring attention. It is more balanced in the workload. Just redistrubute the tokens to the cards in a zigzag manner. The everything is the same as the ring attention, except the token distribution.

### pipeline details

pipeline的重点在于如何实现overlap， 也就是说如何让计算和通信重叠。

**`AFAB` all forward and all backward.**

This means we can use many micro batches, when gpu 1 is processing batch2, gpu 2 can be processing batch1, and so on. Backward is the same fashion.

**`1F1B` one forward and one backward.**

This means when batch1 has finished forward, the last gpu can start backward on batch1, and so on. **This will not decrease the bubble time.** But it will **decrease the memory usage** since when batch 1 has been backwarded, the memory of activation has been freed.

**interleave**

If we distribute the layers to the gpus in a interleave manner, we can achieve the best overlap. For instance, if we have 4 gpus, we can distribute the layers to the gpus in the following manner:

gpu1: layer1, layer3, layer5, layer7

gpu2: layer2, layer4, layer6, layer8

This will increase the commucation cost since the forward and backward should exchange data between the gpus many times.

### pipeline schedule visualizer

下面这个小程序可以根据配置自动生成类似的流水线时间图（支持 interleaved 1F1B / AFAB）：

<iframe
  src="{{ '/files/pipeline-visualizer/?m=4&v=2&nmb=16&mode=1f1b' | relative_url }}"
  width="100%"
  height="760"
  style="border:none; border-radius:12px; overflow:hidden; min-height:680px;">
</iframe>

可以直接调 `m`、`v` 和 `micro-batches`；默认示例就是 `m=4, v=2`。




