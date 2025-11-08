---
title: "CPU-Arch-Opt"
collection: blog
type: "blog"
date: 2025-11-07
excerpt: 'An in-depth look at CPU architecture optimizations and their impact on performance.'
location: "Shanghai, China"
---

# CPU-Arch-Opt

## Introduction

最近在读 [Performance Analysis and Tuning on Modern CPU](https://book.easyperf.net/perf_book), 写点笔记.

- 这本书的作者是 Intel 的工程师, 所以主要涉及 Intel X86 CPU 的架构和优化, 而不包括 ARM 等其他架构. 

- 本书内容不超过单个cpu插槽, 既不涉及 NUMA, 异构计算, MPI 等多节点多机的内容.

## 性能分析

### Noise

CPU 性能分析中, 有许多环境是无法控制的, 可能来自硬件, 也可能来自软件.

- CPU的频率调节. 具体来说, 现代 CPU 都有动态频率调节(DFS), "冷"的时候会自动超频, "热"的时候会降频.
- software的cache
- UNIX的环境大小(存储env var的bytes数)和给linker提供目标文件的顺序都会以不可预测的方式影响性能.
- 内存布局: 内存布局带来的影响可以通过运行时重复的随机化代码, 堆栈和堆对象的放置来消除. 但是后续该技术没有充分的发展.

![DFS](pictures/dfs.png)

> remark: 甚至开top/htop等监控工具也会影响性能分析的结果.

### timer

现代 CPU 的高分辨率计时器有两种:

- **系统范围的高分辨率定时器**: 例如 Linux 下的 `clock_gettime(CLOCK_MONOTONIC, ...)`, 系统定时器具有纳秒级分辨率，
在所有 CPU 之间保持一致，并且与 CPU 频率无关。虽然系统定时器可以返回纳秒精度的时间戳，但由于通
过clock_gettime系统调用获取时间戳需要很长时间，因此不适合测量短时间内发生的事件。但是对于持续时
间超过一微秒的事件来说，这是可以接受的。在 C++ 中访问系统定时器的de facto标准是使用std::chrono.

- **时间戳计数器(TSC)**: TSC 是 CPU 提供的一个寄存器, TSC 是单调的, 并且具有恒定的速率，即不考虑频率变化. 每个 CPU 都有自己的 TSC，它只是已经过去的参考周期数. 适用于持续时间从纳秒到一分钟的短事件的测量. 可以使用编译器内置函数`__rdtsc()`来获取 TSC 的值, 如 Listing 25所示，该函数在底层使用RDTSC汇编指令。有关使用RDTSC汇编指令对代码进行基准测试的更低级别的详细信息, 可以参考白皮书. 调用该函数的开销大约为 20 个 CPU 周期. 而`clock_gettime`调用的开销大约为数百个 CPU 周期.

## CPU Architecture Overview

### ISA (Instruction Set Architecture)



