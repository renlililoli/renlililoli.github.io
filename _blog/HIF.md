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

## 2D 串行

### 2分树

Hypoctree在下面将会被称为T

T的数据结构为

```cpp
struct T {

    // 网格点结构
    using v2d = Eigen::Vector2d<double>;

    int* nodes; // 节点指针数组
    int num_nodes; // 节点数量

    // 每个节点的子节点列表
    // children[i] 存储第 i 个节点的所有子节点索引
    std::vector<std::vector<int>> children;


    // 每个节点的父节点索引
    std::vector<int> parent;

    // 每个level的节点范围
    // [lvlptr[i], lvlptr[i+1]) 表示第 i+1 层的节点索引范围
    std::vector<int> lvlptr;

    // 每个节点中的网格点坐标
    // xis[i] 存储第 i 个节点中的所有网格点坐标
    // 只有叶子节点才有实际的坐标数据
    std::vector<std::vector<v2d>> xis;

    // 每个节点对应的区域中心
    // centers[i] 存储第 i 个节点对应区域的中心坐标
    std::vector<v2d> centers;

    // 每个level中区域的半径
    // lsize[i] 存储第 i 层中区域的半径
    std::vector<double> lsize;

    // 每个节点的邻居节点列表
    // neighbors[i] 存储第 i 个节点的所有邻居节点索引
    std::vector<std::vector<int>> neighbors;
}
```

![2D 四叉树](/blog/pictures/hif-2d.png)