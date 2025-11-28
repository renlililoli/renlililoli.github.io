---
title: "ScaLAPACK"
collection: blog
type: "blog"
date: 2025-11-26
excerpt: 'How to use ScaLAPACK for parallel linear algebra computations on distributed-memory systems.'
location: "Shanghi, China"
---

由于最近要写一些分布式线性代数的代码, 所以要学一下ScaLAPACK. 这玩意难用的要死, 源码是fortran的, 极度逆天. 所以写一个笔记记录一下学习过程.

[官方仓库](https://github.com/Reference-ScaLAPACK/scalapack)

## Introduction

首先, ScaLAPACK是一个分布式内存下的线性代数库, 它是基于BLAS和LAPACK的. 它分为通信层和计算层, 通信层使用MPI实现,
封装为 BLACS (Basic Linear Algebra Communication Subprograms), 计算层使用PBLAS (Parallel Basic Linear Algebra Subprograms)
和ScaLAPACK本身的例程.

## 存储格式

ScaLAPACK使用块循环分布(block-cyclic distribution)来存储矩阵. 师兄做了有趣的小程序, 可以可视化矩阵的分布情况.
[网页](https://xiangli.cyou/posts/2025/04/block-cyclic-visualization.html)

## BLACS

### 上下文

参考: [BLACS Users' Guide](https://netlib.org/scalapack/slug/node71.html)

BLACS是ScaLAPACK的通信层. 在一般的并行程序中, 进程常常是1维排列的, 或者说只用rank来标识进程, 然而为了方便矩阵的分布和通信, BLACS引入了2维进程网格(process grid)的概念.

BLACS对通信器进行了封装, 将它称为context. 创建上下文有两个subroutine:
`BLACS_GRIDINIT` 和 `BLACS_GRIDMAP`. 前者是根据进程数目自动创建一个最接近方形的进程网格, 后者则是用户自定义进程网格的形状.

```cpp
// function prototype
extern "C" {
    void Cblacs_pinfo(int* mypnum, int* nprocs);

    void Cblacs_get(int ictxt, int what, int* val);

    void Cblacs_pcoord(int ictxt, int pnum, int* prow, int* pcol);

    void Cblacs_gridmap(int* ictxt, int* usermap,
                        int ldumap, int nprow, int npcol);

    void Cblacs_gridinit(int* ictxt, const char* order,
                         int nprow, int npcol);

    void Cblacs_gridinfo(int ictxt,
                         int* nprow, int* npcol,
                         int* myrow, int* mycol);

    void Cblacs_gridexit(int ictxt);

    void Cblacs_exit(int cont);
}
```

```cpp
// main

int main(int argc, char** argv) {

    MPI_Init(&argc, &argv);              // 初始化 MPI
    int mypnum, nprocs;
    Cblacs_pinfo(&mypnum, &nprocs);    // 获取 BLACS rank 和总进程数

    int ictxt;
    Cblacs_get(-1, 0, &ictxt);         // 获取一个 context

    int nprow = 2, npcol = 2;          // 创建 2×2 网格
    Cblacs_gridinit(&ictxt, "Row", nprow, npcol);

    int myrow, mycol;
    Cblacs_gridinfo(ictxt, &nprow, &npcol, &myrow, &mycol);

    std::cout << "Rank " << mypnum << " in BLACS grid at position ("
              << myrow << "," << mycol << ")\n";

    Cblacs_gridexit(ictxt);            // 删除 context
    Cblacs_exit(0);                    // 退出 BLACS
    // MPI_Finalize() is called inside Cblacs_exit

    return 0;
}
```

```bash
# output
Rank 3 in BLACS grid at position (1,1)
Rank 2 in BLACS grid at position (1,0)
Rank 1 in BLACS grid at position (0,1)
Rank 0 in BLACS grid at position (0,0)
```

对于 `Cblacs_gridmap` , 这个函数将会把抽象网格映射到实际的rank上. 用户需要提供一个一维数组 `map`, 其长度为 `nprow * npcol`, 用来指定每个网格位置对应的rank. 具体来说, `map[i+ j*ldumap ]` 表示网格位置 (i, j) 上的rank.
然后调用 `Cblacs_gridmap` 来创建进程网格. 注意, CBLACS 内部会访问 map[i + j*ldumap], 其中 ldumap 是 map 数组的 leading dimension, 所以要小心的是, 这里的 map 数组是按列优先存储的, leading dimension 是行数而不是列数.
> ScaLAPACK中所有的矩阵都是按列优先存储的, 即leading dimension是行数.

```cpp
// gridmap example
int main(int argc, char** argv)
{
    MPI_Init(&argc, &argv);

    int myid, nprocs;
    Cblacs_pinfo(&myid, &nprocs);

    /* Suppose we want a 2×3 grid (nprow=2, npcol=3) */
    int nprow = 2, npcol = 3;
    if (nprocs != nprow * npcol) {
        if (myid == 0)
            printf("Need %d processes.\n", nprow * npcol);
        MPI_Finalize();
        return 0;
    }

    /* ====== 1. 定义 map ======
       map 是一维数组，长度 = nprow * npcol
       map(i,j) = map[i*npcol + j] 是那个网格位置上的 rank
    */

    int map[6] = {
        0, 3,
        1, 4,
        2, 5
    };

    /* ====== 2. 初始化 BLACS 上下文 ====== */
    int ictxt;
    Cblacs_get(-1, 0, &ictxt);

    /* ====== 3. 用 map 建立进程网格 ====== */
    Cblacs_gridmap(&ictxt, map, nprow, nprow, npcol);

    /* ====== 4. 获取信息 ====== */
    int myrow, mycol;
    int r, c;
    Cblacs_gridinfo(ictxt, &r, &c, &myrow, &mycol);

    printf("Rank %d -> (row=%d, col=%d)\n", myid, myrow, mycol);

    /* ====== 5. 退出 ====== */
    Cblacs_gridexit(ictxt);
    Cblacs_exit(0);
    return 0;
}
```

```bash
# output
Rank 3 -> (row=1, col=0)
Rank 5 -> (row=1, col=2)
Rank 4 -> (row=1, col=1)
Rank 1 -> (row=0, col=1)
Rank 2 -> (row=0, col=2)
Rank 0 -> (row=0, col=0)
```

这里还有一个让人困惑的地方就是`Cblacs_get` 的第一个参数 `ictxt`. 当 `ictxt = -1` 时, 它表示获取一个新的context. 但是当 `ictxt != -1` 时, 它表示获取已经存在的context中的某个属性(由第二个参数指定). 具体来说, 第二个参数 `what` 可以取以下值:
- `what = 0`: 获取 context 的标识符 (handle)
- `what = 1`: 获取 context 中的进程总数
- `what = 2`: 获取 context 中的当前进程的 rank

当然可以，我帮你整理成清晰、层次分明的 Markdown 版本：

---

### BLACS Context 与自定义 MPI_Comm 的关系

#### 1. BLACS 不接受用户自定义的 MPI_Comm

* `Cblacs_gridinit`、`Cblacs_gridmap` 都只能 **在 BLACS 内部创建自己的通信器**。
* 它 **永远不会直接使用**你 `MPI_Comm_split` 生成的 `newcomm`。
* 因此，你无法“强行替换” BLACS 的通信器。

#### 2. 使用 `gridmap` 限制进程组

* 假设你想在一个 4×4 的 BLACS 网格里 **只让部分 rank 参与**。
* 你可以用 `Cblacs_gridmap` 指定一个数组，列出这些 rank 在 `MPI_COMM_WORLD` 中的编号。
* BLACS 内部会用这些 ranks **新建自己的 context（通信器）**。
* **条件**：这些 ranks 必须可以被索引，不能太散乱，否则 BLACS 的映射逻辑会出问题。

#### 3. BLACS Context 的本质

* BLACS 的 context 本质上是一个 **子通信器 + 网格拓扑 + rank 映射表**。
* 你可以控制“只用部分进程”，但底层通信器仍然是 **BLACS 自己创建的**，不是外部 split 出来的 `newcomm`。

---

### BLACS Context 与通信器的关系

#### 1. 总是基于 `MPI_COMM_WORLD` 创建

* 无论你只使用部分进程，BLACS 会在内部从 `MPI_COMM_WORLD` **派生新的通信器**。
* 这个通信器是 **全局可见的**，所有调用 `Cblacs_gridinit` 或 `Cblacs_gridmap` 的进程都必须在 `MPI_COMM_WORLD` 中。

#### 2. 局部进程参与网格

* 通过 `Cblacs_gridmap` 或 `Cblacs_gridinit` 可以让 **只有部分进程“活跃”**，形成局部网格。
* BLACS 会自动把没有参与的进程排除掉（在 context 中的 rank 会被标记为 -1 或类似标记）。

#### 3. 底层通信器仍然由 BLACS 创建

* 外部的 `MPI_Comm_split` 或自定义通信器 **不能直接代入** BLACS。
* BLACS 只认它自己创建的 context 内通信器。
* 你可以通过 **rank 映射** 实现“只让局部进程参与计算”的效果。

---


### 块循环分布与Array Descriptor

参考: [ScaLAPACK Users' Guide](https://netlib.org/scalapack/slug/node77.html)

在ScaLAPACK中, 矩阵是以块循环分布(block-cyclic distribution)的方式存储在进程网格中的. 这种分布方式有助于负载均衡和减少通信开销. 对于某个特定的维度, 假设块大小为 `n`, 进程数为 `p`, 矩阵对应的维度为 `N`, 那么`i`元素对应的进程号为:
```
proc(i) = floor(i / n) mod p
```
每个维度都同理.

为了描述一个分布式矩阵, ScaLAPACK使用了一个称为Array Descriptor的结构. 这个描述符包含了矩阵的全局信息, 以及它在进程网格中的分布方式. 一个典型的Array Descriptor包含以下字段:

<table border="1" cellspacing="0" cellpadding="4">
  <thead>
    <tr>
      <th>序号</th>
      <th>Symbolic Name</th>
      <th>Scope</th>
      <th>Definition</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>DTYPE_A</td>
      <td>(global)</td>
      <td>Descriptor type <strong>DTYPE_A=1</strong> for dense matrices.</td>
    </tr>
    <tr>
      <td>2</td>
      <td>CTXT_A</td>
      <td>(global)</td>
      <td>BLACS context handle, indicating the BLACS process grid over which the global matrix A is distributed. The context itself is global, but the handle (the integer value) may vary.</td>
    </tr>
    <tr>
      <td>3</td>
      <td>M_A</td>
      <td>(global)</td>
      <td>Number of rows in the global array A.</td>
    </tr>
    <tr>
      <td>4</td>
      <td>N_A</td>
      <td>(global)</td>
      <td>Number of columns in the global array A.</td>
    </tr>
    <tr>
      <td>5</td>
      <td>MB_A</td>
      <td>(global)</td>
      <td>Blocking factor used to distribute the rows of the array.</td>
    </tr>
    <tr>
      <td>6</td>
      <td>NB_A</td>
      <td>(global)</td>
      <td>Blocking factor used to distribute the columns of the array.</td>
    </tr>
    <tr>
      <td>7</td>
      <td>RSRC_A</td>
      <td>(global)</td>
      <td>Process row over which the first row of the array A is distributed.</td>
    </tr>
    <tr>
      <td>8</td>
      <td>CSRC_A</td>
      <td>(global)</td>
      <td>Process column over which the first column of the array A is distributed.</td>
    </tr>
    <tr>
      <td>9</td>
      <td>LLD_A</td>
      <td>(local)</td>
      <td>Leading dimension of the local array. <strong>LLD_A ≥ MAX(1, LOCr(M_A))</strong>.</td>
    </tr>
  </tbody>
</table>


> 这里LLD_A是本地存储的leading dimension, LOCr(M_A)表示本地进程上矩阵A的行数. 两者的不一致是某些情况下为了内存对齐或者性能优化而引入的.

> 除此之外, init descriptor也不涉及通信.

```cpp
// function prototype
// ScaLAPACK descriptor init
void descinit_(int *desc, const int *m, const int *n, const int *mb, const int *nb,
            const int *irsrc, const int *icsrc, const int *ictxt,
            const int *lld, int *info);

// Helper to compute local matrix size
int numroc_(const int *n, const int *nb, const int *iproc,
        const int *isrcproc, const int *nprocs);
```

```cpp
// init desc
int main(int argc, char** argv)
{
    MPI_Init(&argc, &argv);

    int ictxt, nprow = 2, npcol = 2;
    int myrow, mycol, myrank;

    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    // 创建 BLACS context
    Cblacs_get(-1, 0, &ictxt);
    Cblacs_gridinit(&ictxt, "Row", nprow, npcol);
    Cblacs_gridinfo(ictxt, &nprow, &npcol, &myrow, &mycol);

    if (myrow < 0) {
        // not part of the grid
        MPI_Finalize();
        return 0;
    }


    // Global matrix information
    int M = 16, N = 8;
    int MB = 2, NB = 2;

    int RSRC = 0; // Row source process
    int CSRC = 0; // Column source process

    // 计算本地矩阵行列数
    int mloc = numroc_(&M, &MB, &myrow, &RSRC, &nprow);
    int nloc = numroc_(&N, &NB, &mycol, &CSRC, &npcol);


    // 本地存储 LLD 必须 ≥ max(1, mloc)
    int lld = std::max(1, mloc);

    // 创建 descriptor
    int descA[9];
    int info;
    descinit_(descA, &M, &N, &MB, &NB,
              &RSRC, &CSRC,
              &ictxt, &lld, &info);

    if (info != 0) {
        std::cerr << "descinit failed on rank " << myrank
                  << " with info = " << info << std::endl;
    }

    // 输出 descriptor 信息
    std::cout << "Rank " << myrank
              << " (row=" << myrow << ", col=" << mycol << ")"
              << "  local matrix = " << mloc << " x " << nloc
              << "  LLD=" << lld
              << std::endl;

    Cblacs_gridexit(ictxt);
    MPI_Finalize();
    return 0;
}
```

```bash
mpirun -np 4 ./desc.x
Rank 1 (row=0, col=1)  local matrix = 8 x 4  LLD=8
Rank 3 (row=1, col=1)  local matrix = 8 x 4  LLD=8
Rank 0 (row=0, col=0)  local matrix = 8 x 4  LLD=8
Rank 2 (row=1, col=0)  local matrix = 8 x 4  LLD=8
```

由于矩阵是块循环分布在processor grid上的, 所以我们需要知道局部的行列号对应的全局行列号.
这里有一个简单的小函数.
```cpp
// function prototype
static inline int loc2glb(
  const int i_loc, const int rsrc, const int myrow, const int nprow, const int MB
) {

  int brow = i_loc / MB;          // 是第几个 block-row（局部）
  int off  = i_loc % MB;          // 在 block 里的偏移

  int global_i =
      (brow * nprow + (myrow - src + nprow) % nprow) * MB + off;
  return global_i
}
```
由这个小函数我们就能正确的给局部的矩阵初始化正确的值, 和从局部的结果中提取需要的元素.

## PBLAS

PBLAS 是 Parallel BLAS, 即分布式的BLAS库, 它实现了所有分布式的BLAS运算. 它的基本命名规则和LAPACK基本相同, 除了在对应routine前加了P.

下面是一个调用`pdgemm_`的例子

```cpp
// function prototype
// PDGEMM(TRANSA, TRANSB, M, N, K,
//    ALPHA, A, IA, JA, DESCA,
//           B, IB, JB, DESCB,
//    BETA,  C, IC, JC, DESCC)
void pdgemm_(char*, char*, int*, int*, int*,
                double*, double*, int*, int*, int*,
                         double*, int*, int*, int*,
                double*, double*, int*, int*, int*);
```


```cpp
#include <mpi.h>
#include <iostream>
#include <vector>
#include "interface.h"

int main(int argc, char** argv)
{
    MPI_Init(&argc, &argv);

    int myrank, nprocs;
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);

    // ---- BLACS 初始化 ----
    int ictxt, nprow = 2, npcol = 2;  // 2x2 进程网格
    Cblacs_get(-1, 0, &ictxt);
    Cblacs_gridinit(&ictxt, "Row", nprow, npcol);

    int myrow, mycol;
    Cblacs_gridinfo(ictxt, &nprow, &npcol, &myrow, &mycol);

    // ---- 全局矩阵尺寸 ----
    int M = 4, N = 4, K = 4;
    int MB = 2, NB = 2; // block size

    // ---- 每个进程的局部矩阵大小 ----
    int zero = 0, one = 1;
    int mA = numroc_(&M, &MB, &myrow, &zero, &nprow);
    int kA = numroc_(&K, &NB, &mycol, &zero, &npcol);

    int kB = numroc_(&K, &MB, &myrow, &zero, &nprow);
    int nB = numroc_(&N, &NB, &mycol, &zero, &npcol);

    int mC = numroc_(&M, &MB, &myrow, &zero, &nprow);
    int nC = numroc_(&N, &NB, &mycol, &zero, &npcol);

    // ---- 分配本地矩阵 ----
    double *A = (double*)malloc(mA * kA * sizeof(double));
    double *B = (double*)malloc(kB * nB * sizeof(double));
    double *C = (double*)malloc(mC * nC * sizeof(double));

    // 初始化 A, B, C
    for (int i = 0; i < mA*kA; ++i) A[i] = 1.0;
    for (int i = 0; i < kB*nB; ++i) B[i] = 1.0;
    for (int i = 0; i < mC*nC; ++i) C[i] = 0.0;

    // ---- 初始化 ScaLAPACK 描述符 ----
    int descA[9], descB[9], descC[9], info;
    int rsrc = 0, csrc = 0;  // block cyclic source process

    descinit_(descA, &M, &K, &MB, &NB, &rsrc, &csrc, &ictxt, &mA, &info);
    descinit_(descB, &K, &N, &MB, &NB, &rsrc, &csrc, &ictxt, &kB, &info);
    descinit_(descC, &M, &N, &MB, &NB, &rsrc, &csrc, &ictxt, &mC, &info);

    // ---- 调用 pdgemm ----
    double alpha = 1.0, beta = 0.0;
    char trans = 'N';

    // pdgemm_(&trans, &trans,
    //         &M, &N, &K,
    //         &alpha,
    //         A, &zero, &zero, descA,
    //         B, &zero, &zero, descB,
    //         &beta,
    //         C, &zero, &zero, descC);
    pdgemm_(&trans, &trans,
            &M, &N, &K,
            &alpha,
            A, &one, &one, descA,
            B, &one, &one, descB,
            &beta,
            C, &one, &one, descC);

    // ---- 打印局部矩阵 ----
    MPI_Barrier(MPI_COMM_WORLD);
    printf("Rank %d (%d,%d) local C (%d x %d):\n",
           myrank, myrow, mycol, mC, nC);
    for (int i = 0; i < mC; ++i) {
        for (int j = 0; j < nC; ++j)
            printf(" %g", C[i + j*mC]);
        printf("\n");
    }
    printf("\n");

    free(A);
    free(B);
    free(C);

    Cblacs_gridexit(ictxt);
    return 0;
}
```

要注意的是这里传入的IA,JA...是全局矩阵的起始坐标, 而不是本地矩阵. 即`pdgemm_`处理的
块对于A来说是`IA:IA+M-1, JA:JA+K-1`. 这是一个全局调用.