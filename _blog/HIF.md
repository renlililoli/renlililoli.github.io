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

### 2分树数据结构

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

除了上述数据结构, 还需要下一个层次中的EdgeTree, 用于dim1消元

```cpp
struct EdgeTree {
    std::vector<int> lvlptr; // 每个level的边范围, 其实是假的, 本质上只存了这一层的边
    std::vector<v2d> centers; // 每条边的中心位置
    std::vector<std::vector<v2d>> xis; // 每条边上的网格点坐标
    std::vector<std::vector<int>> neighbors; // 每条边的邻居边列表
    std::vector<std::vector<int>> parents; // 每条边的父边列表


};
```

![2D 四叉树](/blog/pictures/hif-2d.png)

### HIF 算法流程

需要存储的数据
```cpp

struct HIF2D {
    T tree; // 四叉树数据结构

    using HIFFactor2DNode = struct {
        // 骨架点索引
        std::vector<int> sk;

        // 冗余点索引
        std::vector<int> rd;

        // 插值矩阵 T
        SparseMatrix<double> T;

        // LU 分解结果
        SparseMatrix<double> L;
        SparseMatrix<double> U;
        std::vector<int> P; // 置换矩阵, 存储行交换信息

        // E 和 F 矩阵
        SparseMatrix<double> E;
        SparseMatrix<double> F;
    };

    // 原始矩阵, 稀疏格式存储, csr
    SparseMatrix<double> A;

    // 所有的更新
    SparseMatrix<double> M;

    // IJV 列表
    std::vector<int> IJV_I;
    std::vector<int> IJV_J;
    std::vector<double> IJV_V;

    // 每个节点的HIF分解结果
    std::vector<HIFFactor2DNode> factors;
    // 每个level的节点范围
    // [factor_node_lvlptr[i], factor_node_lvlptr[i+1])
    // 表示第 i+1 层的节点索引范围
    std::vector<int> factor_node_lvlptr;

    // 未消去的节点列表
    // remains[i] = 0 表示第 i 个节点已被消去
    std::vector<int> remains;
};
```

最外层循环 --- 对于每一个level进行处理

1. 从子level收集所有的未消去网格点
2. 删除子节点的所有网格点

3. 对于当前层的每个节点进行dim2消元
4. 对于当前层的每个节点进行dim1消元

内层循环 --- 对于每一个节点进行处理

expand of 3: dim2 elimination

1. 对该节点负责的所有网格点进行插值分解, 得到骨架点sk和冗余点rd以及插值矩阵T. 将树的remains对应的rd点标记为已消去.
2. 将矩阵A与M在当前节点上对应的子矩阵进行相加得到真实的目前的子矩阵A_node. 对A_node用对应的插值矩阵T进行消元更新, 得到更新后的子矩阵A_node_new.

以下是矩阵的变化过程：

初始矩阵：
$$
\begin{bmatrix}
A(\text{rd}, \text{rd}) & A(\text{rd}, \text{sk}) & A(\text{rd}, \text{oth}) \\
A(\text{sk}, \text{rd}) & A(\text{sk}, \text{sk}) & A(\text{sk}, \text{oth}) \\
A(\text{oth}, \text{rd}) & A(\text{oth}, \text{sk}) & A(\text{oth}, \text{oth})
\end{bmatrix}
$$

经过消元后变为：
$$
\begin{bmatrix}
A_{\text{new}}(\text{rd}, \text{rd}) & 0 & 0 \\
0 & A_{\text{new}}(\text{sk}, \text{sk}) & A(\text{sk}, \text{oth}) \\
0 & A(\text{oth}, \text{sk}) & A(\text{oth}, \text{oth})
\end{bmatrix}
$$

3. 将更新后的子矩阵A_node_new进行LU分解, 得到 P, L, U 三个矩阵. 并计算对应的E和F矩阵. 同时保存[rd], 
4. 计算(sk, sk)上的舒尔补 X = -E * F, 并将X更新到IJV列表中.
> 每次回传的舒尔补都是针对当前节点的sk点的, 因为rd点已经被消去掉了.

5. 将当前level的所有节点的更新都应用到M矩阵上. 具体操作为: 找到M的所有非零元, 将其更新到IJV列表中. 然后清空M矩阵.从IJV列表中重新构建M矩阵.

> dim1 elimination 并没有和dim2有什么区别, 只是树是边构成的. 这个由边构成的树只有一层.

