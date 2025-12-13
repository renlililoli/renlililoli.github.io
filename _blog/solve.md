---
title: "Solve sparse linear systems with iterative methods."
collection: blog
type: "blog"
date: 2025-11-30
excerpt: 'How to use iterative methods to solve sparse linear systems efficiently.'
location: "Shanghai, China"
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


## 常见迭代法 Krylov 子空间法

### FOM GMRES

两种方法都是在Krylov子空间中寻找解的近似.

$$
x = x_0+ V_m y_m, r_m = b - A x = r_0 - A V_m y_m = V_{m+1}(\beta e_1 - \bar{H}_m y_m).
$$

对于FOM, 希望 $r_m \perp V_m$ , 则有
$$
H_m y_m = \beta e_1.
$$

它等价于极小化 $||x_m - x_*||_A$ .

而对于GMRES, 希望极小化 $||r_m||_2$ , 则有
$$
y_m = \arg\min_y ||\beta e_1 - \bar{H}_m y||_2.
$$

我们希望能迭代的求出新的近似解, 而不是每次从头开始求解线性方程组或者最小二乘法.

迭代的求解就是每次计算$\bar{H}_m$的的新的一列, 然后用Givens旋转消去最后一个元素, 从而更新QR分解. 对于GMRES, 残差的范数就是$g_m = Q_m^T \beta e_1$的最后一个元素. 这个元素会在第m次迭代时被乘上$s_m$. 因此有

$$ \rho_m^G = |g_{m+1}^{(m)}| = |s_m| \rho_{m-1}^G.$$

对于FOM, 残差则是
$$
\rho_m^F = b - A x_m = b - A (x_0 + V_m y_m) \\= r_0 - A V_m y_m = V_{m+1} (\beta e_1 - \bar{H}_m y_m) = h_{m+1, m} e_{m}^T y_m \\= h_{m+1, m}  \beta e_m^T H_m^{-1}e_1.
$$

考虑$w = H_m^{-1}e_1$. 它满足 $H_m w = e_1$. 对它做QR分解得到的恰好是GMRES中用到的Givens旋转除了最后一个旋转外的所有旋转. 因此有
$$
\rho_m^F = h_{m+1, m} g_m^{(m-1)} / h_{m, m}^{(m-1)} = s_m / c_m \rho_{m-1}^G = \rho_m^G / |c_m|.
$$

在使用迭代法的时候, 还有一个要考虑的是每次更新的大小

$$
x_m^G - x_{m-1}^G = c_m^2 (x_m^F - x_{m-1}^G).
$$

证明并不困难, 按照定义展开即可.

### IOM QGMRES DIOM DQGMRES

由于 Krylov 子空间方法每次迭代都需要存储所有的基向量, 因此可以选择局部正交化, 就是只存储最近的 $k$ 个基向量. 每次正交化的时候, 只和最近的 $k$ 个基向量正交化.

对于 IOM 和 QGMRES, 他们分别是 FOM 和 GMRES 的局部正交化版本. DIOM 和 DQGMRES 则是他们的迭代版本

对于DIOM, 
$$
x_m = x_0 + V_m H_m^{-1} e_1 \beta = x_0 + V_m U_m^{-1} L_m^{-1} e_1 \beta = x_0 + P_m z_m.
$$

其中 $P_m = V_m U_m^{-1}$ , $z_m = L_m^{-1} e_1 \beta$ . 迭代的更新LU分解. 则$z_m$ 可以迭代的计算出来.

$$
z_m = \begin{bmatrix} z_{m-1} \\ l_{m, m-1}z_{m-1;m-1} \end{bmatrix}
$$
以及
$$
P_m = [P_{m-1}, p_m], p_m = \frac{1}{u_{m,m}}(v_m - P_{m-1} u_{1:m-1, m}).
$$

因此有
$$
x_m = x_{m-1} + z_{m;m} p_m.
$$

注意到FOM每一步的残差 $r_m^F$ 都平行于 $v_{m+1}$, 因此残差互相正交.

> remark: 除此之外
$$
P_m^T A P_m = U_m^{-T} V_m^T A V_m U_m^{-1} = U_m^{-T} H_m U_m^{-1} = U_m^{-T} L_m.
$$
> 因此在A对称下, $P_m$ 是A正交的.

对于DQGMRES, 也是类似的过程. 只不过此时
$$
x_m = x_0 + V_{m} y_m, y_m = R_m^{-1} Q_m^T \beta e_1, P_m = V_m R_m^{-1}.
$$

### 对称情况 - CG GCR

对称情况恰好H是三对角矩阵, 因此递推变成仅有三个向量的线性组合. 结合p的A正交性和残差的正交性, 可以得到CG算法.

还可以选择用互相正交的Ap作为基向量来寻找最优解, 这就是GCR算法.


## Lanczos 双正交化

为了节省计算量, 可以在多项式空间中定义特殊的双线性形式.

$$
(p_i(x), p_j(x) ) = (p_i(A^T)w, p_j(A)v) = w^T p_i(A) p_j(A) v.
$$

这是一个对称的双线性形式. 基于这个双线性形式, 可以定义一组正交多项式 $\{ q_i(x) \}$ , 使得
$$
(q_i(x), q_j(x)) = 0, i \neq j.
$$

并且在这个双线性形式下, 
$$
(x q_i(x), q_j(x)) = (q_i(x), x q_j(x)).
$$
可以得到$x$在这组基下的三对角矩阵的递推关系:

$$
x q_{i}(x) = \sum_{j=1}^{i+1} h_{ij} q_{j}(x), h_{ij} = \frac{(x q_i(x), q_j(x))}{(q_j(x), q_j(x))} \Rightarrow q_{i+1}(x) = \frac{1}{h_{i+1,i}}(x q_i(x) -  h_{ii} q_i(x) - h_{i,i-1}q_{i-1}(x)).
$$

双正交向量组可以被分别定义为
$$
v_i = q_{i-1}(A)v, w_i = q_{i-1}(A^T)w.
$$

其中可能有一些正负号的差异, 来源是内积的非正定性. 但是总是在没有breakdown的情况下, 让 $(w_i, v_j) = \delta_{ij}$.

### BiCG

类似于CG, 同时在 $K_m(A,v)$ 和 $K_m(A^T,w)$ 上寻找两个系统的近似解. 两个系统的残差互相正交.
而每一步的共轭方向在A意义下正交.

$$
P_m = V_mU_m^{-1}, Q_m = W_m L_m^{-T}.\\
Q_m^T A P_m = L_m^{-T} W_m^T A V_m U_m^{-1} = L_m^{-T} H_m U_m^{-1} = I_m.
$$

### CGS BiCGSTAB

这两种方法都是在充分利用多项式的结构.

我们知道
$$
r_m = \phi_m(A) r_0, p_m = \pi_m(A) r_0\\
r_m^* = \phi_m(A^T) r_0^*, p_m^* = \pi_m(A^T) r_0^*.
$$

而递推关系为
$$
\phi_{m+1}(x) = \phi_m(x) - \alpha_m x \pi_m(x)\\
\pi_{m+1}(x) = \phi_{m+1}(x) + \beta_m \pi_m(x).
$$

$$
\alpha_m = \frac{(\phi_m(A)r_0, \phi_m(A^T) r_0^*)}{(A \pi_m(A) r_0, \pi_m(A^T) r_0^*)} = \frac{(\phi_m(A)^2r_0, r_0^*)}{(A \pi_m(A)^2 r_0, r_0^*)},\\
\beta_m = \frac{(\phi_{m+1}(A) r_0, \phi_{m+1}(A^T) r_0^*)}{(\phi_m(A) r_0, \phi_m(A^T) r_0^*)} = \frac{(\phi_{m+1}(A)^2 r_0, r_0^*)}{(\phi_m(A)^2 r_0, r_0^*)}.
$$

为了直接计算, 可以写出$\phi_m(x)^2$ 和 $\pi_m(x)^2$ 的递推关系.

$$
r_j = \phi_j(A)^2 r_0, p_j = \pi_j(A)^2 r_0, q_j = \phi_{j+1}(A)\pi_j(A) r_0.\\
$$

用这些量来表示 $\alpha_m$ 和 $\beta_m$和递推关系即可.

将CGS视为BiCG的一种变形, 通过将残差多项式平方来加速收敛, 而BiCGSTAB则通过引入一个平滑步骤来稳定收敛过程, 即光滑因子不是自身.

$$
r_m = \psi_m(A) \phi_m(A) r_0, p_m = \psi_m(A) \pi_m(A)  r_0.
$$

其中 $\psi_m(x) = (1 - \omega_m x) \psi_{m-1}(x)$ , $\psi_0(x) = 1$.

但是目前问题在于如何计算$\alpha_m, \beta_m, \omega_m$.

对于 $\alpha_m$ 和 $\beta_m$,
$$
\rho_m = (\phi_m(A)r_0, \phi_m(A^T) r_0^*) = (\phi_m(A)r_0, \psi_m(A^T) r_0^*) * \frac{l1}{l2} = \tilde{\rho}_m * \frac{l1}{l2}.\\
\beta_{j-1} = \frac{\rho_m}{\rho_{m-1}} = \frac{\tilde{\rho}_m}{\tilde{\rho}_{m-1}} * \frac{\alpha_{m-1}}{\omega_{m-1}}.
$$
$\alpha_m$ 的计算类似, $\alpha_j = \frac{\tilde{\rho}_j}{(Ap_j, r_0^*)}$.

对于 $\omega_m$ , 通过最小化 $||r_{m+1}||_2$ 可得
$$
\omega_m = \frac{(A s_m, s_m)}{(A s_m, A s_m)}.\\
s_m = r_m - \alpha_m A p_m = \psi_m(A) \phi_{m+1}(A) r_0.
$$

## Preconditioned Iterative Methods

### PCG FGMRES

比较简单, 主要是要搞明白CG预条件后新矩阵在什么意义下是对称的.