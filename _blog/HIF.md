---
title: "HIF"
collection: blog
type: "blog"
date: 2025-11-06
excerpt: '层次插值分解'
location: "Shanghi, China"
---

# HIF

学一下层次插值分解(Hierarchical Interpolative Factorization, HIF).

## 例子

考虑一个2D区域上的PDE, 网格是 $\sqrt{N}\times \sqrt{N}$ 的, 离散化后得到一个 $N$ 维线性系统:
$$Ax = b.$$

通常的LU分解会直接对这个 $N$ 维系统进行分解, 但这在计算上可能非常昂贵. HIF的思路是利用层次结构来降低计算复杂度.

具体来说, HIF将原始问题分解为多个子问题, 每个子问题在一个较小的网格上求解.

具体的数学步骤已经有很清楚的文献了, 这里主要想具体看一个例子.

假设我们有一个 $10 \times 1
