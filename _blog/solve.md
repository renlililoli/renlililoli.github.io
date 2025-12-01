---
title: "Solve sparse linear systems with iterative methods."
collection: blog
type: "blog"
date: 2025-11-30
excerpt: 'How to use iterative methods to solve sparse linear systems efficiently.'
location: "Shanghi, China"
---

这学期选了变分迭代法, 马上要期末了, 这里总结一下重要的内容. 

## M矩阵

M矩阵是指满足以下条件的矩阵:
1. 所有的非对角线元素都是非正的.
2. 非奇异
3. 其逆矩阵是非负的.

### Property 1

$A_{ii} > 0, \forall i$.

**Proof:** $C = A^{-1}$, 则 $AC = I$ , 即 $\sum_{j} A_{ij} C_{ji} = 1$ , 因为 $A_{ij} \leq 0, \forall i \neq j$ , 所以 $A_{ii} C_{ii} \geq 1$ , 因为 $C_{ii} \geq 0$ , 所以 $A_{ii} > 0$ .

### Theorem 2 (Perron-Frobenius)

设A是一个非负不可约矩阵, 则A有一个正的特征值 $\rho(A)$ 和一个正的特征向量 $x > 0$. 对应的特征子空间是1维的.

### Lemma 3

$O\le A \le B$ , 则 $\rho(A) \le \rho(B)$ .

**proof:** 只需使用谱半径公式与1范数即可证明.

### Lemma 4

设 $B \ge O$, 则 $\rho(B) < 1$ 当且仅当 $(I - B)^{-1} \ge 0$.

**proof:**

- 若 $\rho(B) < 1$ , 则 $(I - B)^{-1} = \sum_{k=0}^{\infty} B^k \ge 0$ .
- 若 $(I - B)^{-1} \ge 0$ , 则由 Theorem 2 可知取 $u$ 为正特征向量, 则 $Bu = \rho(B) u$ , 则 $(I - B)u = (1 - \rho(B)) u \ge 0$, $(I - B)^{-1}u = \frac{1}{1 - \rho(B)} u \ge 0$ , 则 $1 - \rho(B) > 0$ , 即 $\rho(B) < 1$ .

### Theorem 5

设A是一个对角线严格正, 非对角线非正矩阵, 则以下命题等价:
1. A是M矩阵.
2. $\rho(I - D^{-1}A) < 1$ , 其中D为A的对角线矩阵.

**proof:**

因为A是M矩阵, 则 $A^{-1} \ge 0$ , 则 $(I - (I - D^{-1}A))^{-1} = A^{-1} D \ge 0$ , 则由 Lemma 4 可知 它等价于$\rho(I - D^{-1}A) < 1$.

### Theorem 6

设 $A$, $B$ 满足 $A \le B$ 且 $B$ 的非对角线元素非正. 则若 $A$ 是M矩阵, 则 $B$ 也是M矩阵.

**proof:**

设 $D_A$, $D_B$ 分别为A和B的对角线矩阵, 则由 Theorem 5 可知 $\rho(I - D_A^{-1} A) < 1$ . 因为 $A \le B$ , 则 $I - D_A^{-1} A \ge I - D_B^{-1} B \ge O$ , 则由 Lemma 3 可知 $\rho(I - D_B^{-1} B) < 1$ , 则由 Theorem 5 可知B是M矩阵.

## 离散格式与有限元矩阵装配

过于简单

## 稀疏矩阵的消元顺序

### CMK

CMK (Cuthill-McKee)算法是一种用于减少稀疏矩阵带宽的重排序算法。其基本思想是通过重新排列矩阵的行和列，使得非零元素尽可能靠近主对角线，从而减少矩阵的带宽，提高数值计算的效率。

本质上是用queue进行广度优先搜索, 每次加入子节点的时候按照度从小到大排序.

### RCMK

RCMK (Reverse Cuthill-McKee)算法是CMK算法的逆过程。其基本思想是先使用CMK算法对稀疏矩阵进行重排序，然后将得到的顺序反转，从而进一步减少矩阵的带宽。

### Minimum Degree Ordering

Minimum Degree Ordering (MDO)算法是一种用于减少稀疏矩阵填充的重排序算法。其基本思想是通过选择当前度数最小的节点进行消元，从而减少在消元过程中引入的非零元素数量，提高数值计算的效率。

### ISO

最大的两两不相邻节点集合.

独立集里的节点可以同时消元, 因为它们之间没有边相连, 所以不会引入新的非零元素.

贪心法: 每次选择一个节点, 并删除它的所有邻居节点, 直到图中没有节点为止.

### 染色

图的染色问题是指将图的顶点涂上不同的颜色，使得相邻的顶点颜色不同。

贪心法: 每次选择一个顶点, 并为其分配一个与其相邻顶点不同的颜色, 直到所有顶点都被染色为止.

相同颜色的节点可以同时消元, 因为它们之间没有边相连, 所以不会引入新的非零元素.

## 对角占优

### 圆盘定理

设A为n阶复矩阵, 则A的每个特征值都位于$\cup_{i=1}^{n} D(a_{ii}, R_i)$中, 其中 $D(a_{ii}, R_i) = \{ z \in \mathbb{C} : |z - a_{ii}| \le R_i \}$ , $R_i = \sum_{j \neq i} |a_{ij}|$ .

**proof:**

设 $\lambda$ 为A的一个特征值, 则存在非零向量 $x = (x_1, x_2, \ldots, x_n)^T$ 使得 $Ax = \lambda x$ . 设 $|x_k| = \max_{1 \le i \le n} |x_i|$ , 则有

$$\sum_{j=1}^{n} a_{kj} x_j = \lambda x_k$$

则有

$$|\lambda - a_{kk}| |x_k| = |\sum_{j \neq k} a_{kj} x_j| \le \sum_{j \neq k} |a_{kj}| |x_j| \le R_k |x_k|.
$$

### Corollary 1

假设A不可约且有一个特征值 $\lambda$ 满足 $|\lambda - a_{ii}| = R_i$ , 则 $\lambda$ 位于所有圆盘的公共边界上, 且对应的特征向量 $x$ 满足 $|x_1| = |x_2| = \ldots = |x_n|$.

**proof:**

设 $|x_k| = \max_{1 \le i \le n} |x_i|$ , 则由圆盘定理可知
$$|\lambda - a_{kk}| |x_k| = |\sum_{j \neq k} a_{kj} x_j| \le \sum_{j \neq k} |a_{kj}| |x_j| \le R_k |x_k|.$$
因为 $|\lambda - a_{kk}| = R_k$ , 则有
$$|\sum_{j \neq k} a_{kj} x_j| = \sum_{j \neq k} |a_{kj}| |x_j| = R_k |x_k|.$$

因此, 对于所有 $j$ 满足 $a_{kj} \neq 0$ , 有 $|x_j| = |x_k|$ . 由于A不可约, 则对于任意 $i$ , 存在一条从k到i的路径, 因此 $|x_i| = |x_k|$ , 即 $|x_1| = |x_2| = \ldots = |x_n|$ .

### Corollary 2

设A为严格对角占优矩阵或对角占优且不可约矩阵, 则A非奇异.

**proof:**

$0$ 不在任何一个圆盘内, 因此A非奇异.


## 投影法

