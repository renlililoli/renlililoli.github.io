---
title: "Solve sparse linear systems with iterative methods."
collection: blog
type: "blog"
date: 2025-11-30
excerpt: 'How to use iterative methods to solve sparse linear systems efficiently.'
location: "Shanghi, China"
---

这学期选了变分迭代法, 马上要期末了, 这里总结一下重要的内容. 所有的迭代法都基于 `Krylov` 子空间.

## Arnodi

Arnodi 是寻找Krylov子空间的正交基的方法

对于空间 `K_m(A, v) = span{v, Av, A^2v, ..., A^{m-1}v}` , 我们希望找到一组正交基 `V_m = [v1, v2, ..., vm]` , 和对应的上Hessenberg矩阵 m+1 x m `U_m`, 满足 `AV_m = V_{m+1} U_m` . 其中 `U_m` 的每一列可以看作A作用在 `v_k` 上在 `V_{m+1}` 上的投影. 

进行Arnodi可以基于Gram-Schmidt正交化过程, 具体算法如下:
```python
# Algorithm 6.1
def Arnoldi(A, v, m):
    """Arnoldi method to find orthogonal basis of Krylov subspace.

    Args:
        A: Coefficient matrix.
        v: Initial vector.
        m: Dimension of Krylov subspace.

    Returns:
        Q: Orthonormal basis of Krylov subspace.
        H: Upper Hessenberg matrix.
    """
    n = A.shape[0]
    Q = np.zeros((n, m + 1))
    H = np.zeros((m + 1, m))

    # v1
    Q[:, 0] = v / np.linalg.norm(v)

    for k in range(m):
        w = A @ Q[:, k]
        # Gram-Schmidt process instead modified Gram-Schmidt
        for j in range(k + 1):
            H[j, k] = np.dot(Q[:, j], A @ Q[:, k])
            w = w - H[j, k] * Q[:, j]
        H[k + 1, k] = np.linalg.norm(w)
        if H[k + 1, k] != 0 and k + 1 < m:
            Q[:, k + 1] = w / H[k + 1, k]

    return Q, H

```

同样的, 也可以使用 `Modified Gram-Schmidt` 方法来进行Arnodi过程.

```python
# Algorithm 6.2
def Modified_Arnoldi(A, v, m):
    """Modified Arnoldi method to find orthogonal basis of Krylov subspace.

    Args:
        A: Coefficient matrix.
        v: Initial vector.
        m: Dimension of Krylov subspace.
    Returns:
        Q: Orthonormal basis of Krylov subspace.
        H: Upper Hessenberg matrix.
    """
    n = A.shape[0]
    Q = np.zeros((n, m + 1))
    H = np.zeros((m + 1, m))
    # v1
    Q[:, 0] = v / np.linalg.norm(v)
    for k in range(m):
        w = A @ Q[:, k]
        for j in range(k + 1):
            H[j, k] = np.dot(Q[:, j], w)
            w = w - H[j, k] * Q[:, j]
        H[k + 1, k] = np.linalg.norm(w)
        if H[k + 1, k] != 0 and k + 1 < m:
            Q[:, k + 1] = w / H[k + 1, k]
    return Q, H
```

同样的, 也可以使用 `Householder` 方法来进行Arnodi过程. 因为本质上就是在求解上Heissenberg矩阵.

## FOM(Full Orthogonalization Method)

做完arnodi之后, 直接解方程组

### 重启动

内存限制

### IOM and DIOM

同样为了减少内存开销, 只对最近的 `k` 个向量进行正交化. 得到的是一个带状矩阵.(上对角线上有 `k-1` 个非零元素, 即带宽度为k+1)
