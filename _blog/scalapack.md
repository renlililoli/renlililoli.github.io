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

对于 `Cblacs_gridmap` , 这个函数将会把抽象网格映射到实际的rank上. 用户需要提供一个一维数组 `map`, 其长度为 `nprow * npcol`, 用来指定每个网格位置对应的rank. 具体来说, `map[i*ldumap + j]` 表示网格位置 (i, j) 上的rank.
然后调用 `Cblacs_gridmap` 来创建进程网格. 注意, CBLACS 内部会访问 map[i*ldumap + j], 其中 ldumap 是 map 数组的 leading dimension, 所以要小心.
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

### 块循环分布与Array Descriptor

参考: [ScaLAPACK Users' Guide](https://netlib.org/scalapack/slug/node77.html)

