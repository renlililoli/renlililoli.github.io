---
title: "Sobolev imbedding and interpolation inequalities."
collection: blog
type: "blog"
date: 2025-11-30
excerpt: 'An overview of Sobolev imbedding and interpolation inequalities and their applications.'
location: "Shanghai, China"
---

索伯这块内容确实又繁琐又多, 所以这里妄图梳理一个快速查询的笔记.

## Sobolev imbedding

首先, 空间的嵌入定理, 主要按照函数空间的奇性来划分. 由于是积分范数, 所以n维空间的积分可以提供$x^{n/p}$, 而求导数会损失$x^m$的奇性,
所以对于 $m,p$ 的Sobolev空间$W^{m,p}$, 其容纳的奇性大概为 $x^{n/p - m}$. 所以分类的临界值为 $mp = n$. $mp>n$ 时, 函数比较光滑, 可以嵌入到连续函数空间中; $mp<n$ 时只能嵌入普通的$L_q$空间. 具体不等式如下:

![imbedding1](/blog/pictures/sobolev/imbedding1.png)

![imbedding2](/blog/pictures/sobolev/imbedding2.png)

![imbedding3](/blog/pictures/sobolev/imbedding3.png)

![imbedding4](/blog/pictures/sobolev/imbedding4.png)

每个情况的证明都使用了不同的技巧.

首先是除了部分边界情况以及需要区域有lipshitz条件的第二个part, 其余证明利用了区域的cone condition, 然后使用cone上的积分平均值来控制函数值. 积分平均值来自于potential估计.

核心的不等式为

![potential1](/blog/pictures/sobolev/potential1.png)

![potential2](/blog/pictures/sobolev/potential2.png)