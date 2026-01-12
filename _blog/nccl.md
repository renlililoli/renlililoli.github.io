---
title: "NCCL Basics"
collection: blog
type: "blog"
date: 2026-01-09
excerpt: 'An introduction to NVIDIA Collective Communications Library (NCCL) for efficient multi-GPU communication.'
location: "Shanghai, China"
---

NCCL库是多GPU通信的高性能库, 用C++编写, 其中封装了多种通信协议下的集合通信原语, 例如Bcast, AllReduce, Reduce, AllGather等。

它支持多种拓扑结构, 包括单机多卡, 多机多卡, 以及NVLink, PCIe, InfiniBand等高速互联技术。相比于MPI, 其主要针对的是GPU通信, 并主要优化的是一部分特定的集合通信.

参考文献:
- [Demystifying NCCL: An In-depth Analysis of GPU
Communication Protocols and Algorithms](https://arxiv.org/abs/2507.04786)

- [Official NCCL Documentation](https://developer.nvidia.com/nccl)

- [NCCL GitHub Repository](https://github.com/NVIDIA/nccl/tree/master)

### Bcast

```cpp

template<typename T, typename RedOp, typename Proto>
  __device__ __forceinline__ void runRing(int tid, int nthreads, struct ncclDevWorkColl* work) {
    ncclRing *ring = &ncclShmem.channel.ring;
    const int rank = ring->userRanks[0];
    const int nextRank = ring->userRanks[1];
    const int root = work->root;
    ssize_t chunkCount;
    ssize_t channelCount;
    ssize_t gridOffset;
    ncclCollCbdPart(work, ncclShmem.channelId, Proto::Id, sizeof(T), (ssize_t*)nullptr, &gridOffset, &channelCount, &chunkCount);
    size_t offset;
    int nelem;
    int workNthreads;
    bool isNetOffload = work->isOneRPN && work->netRegUsed;

    T *inputBuf = (T*)work->sendbuff;
    T *outputBuf = (T*)work->recvbuff;
    workNthreads = isNetOffload ? WARP_SIZE : nthreads;

    if (tid < workNthreads) {
      // Coverity reports that the callee treats &ring->next as an array.  However, due to the use of
      // FanSymmetric<1>, only the first element is ever accessed, so it's fine.
      // coverity[callee_ptr_arith:FALSE]
      Primitives<T, RedOp, FanSymmetric<1>, 1, Proto, 0>
        prims(tid, workNthreads, &ring->prev, &ring->next, inputBuf, outputBuf, work->redOpArg, 0, 0, 0, work);

      for (size_t elemOffset = 0; elemOffset < channelCount; elemOffset += chunkCount) {
        offset = gridOffset + elemOffset;
        nelem = min(chunkCount, channelCount - elemOffset);

        if (rank == root) {
          if (inputBuf == outputBuf || isNetOffload) {
            prims.directSend(offset, offset, nelem);
          } else {
            prims.directCopySend(offset, offset, nelem);
          }
        } else if (nextRank == root) {
          prims.directRecv(offset, nelem);
        } else {
          prims.directRecvCopyDirectSend(offset, offset, nelem);
        }
      }
    } else if (inputBuf != outputBuf && rank == root) {
      inputBuf = inputBuf + gridOffset;
      outputBuf = outputBuf + gridOffset;
      reduceCopy<COLL_UNROLL, RedOp, T, 0, 1, 1, 0, 1, 1, /*PreOpSrcs=*/0>
        (tid - workNthreads, nthreads - workNthreads, work->redOpArg, false, 1, (void**)&inputBuf, 1, (void**)&outputBuf, channelCount);
    }
    if (isNetOffload) barrier_sync(14, nthreads);
  }
```

可以看到这里面只是外层的通信逻辑, 具体的通信细节在Primitives类里面实现, 这里面会根据不同的通信协议实现不同的通信细节. 看一个具体的协议, 以nvlink为例:

| 层级        | 含义                  | 示例                     |
| --------- | ------------------- | ---------------------- |
| 物理链路协议    | NVLink 自身的链路编码      | NVLink 3.0 flit/credit |
| 传输层协议     | 是否 TCP/IB/UCX       | 否                      |
| NCCL 通信协议 | LL / LL128 / Simple | 是                      |

经验规则:

| 消息大小        | NCCL 协议 |
| ----------- | ------- |
| ≤ 几 KB      | LL      |
| 几 KB ~ 几 MB | LL128   |
| ≥ 几 MB      | Simple  |

| NVLink 特性  | LL128 对应         |
| ---------- | ---------------- |
| 极低延迟       | warp 同步 pipeline |
| 高带宽        | 128-bit 对齐传输     |
| GPU-GPU 直连 | 不经过 host         |

| 特性       | NVLink              | InfiniBand         |
| -------- | ------------------- | ------------------ |
| 物理层      | NVLink flit/credit  | IB link layer      |
| 传输栈      | GPU 内部 load/store   | RDMA verbs         |
| NCCL 协议  | LL / LL128 / Simple | LL / Simple（但实现不同） |
| 是否经过 CPU | 否                   | 通常要注册内存、走 NIC      |
| 延迟       | 极低                  | 高于 NVLink          |
| 带宽       | 极高                  | 受 NIC 限制           |

`infiniBand` 作为跨节点通信的主要手段, 其性能和特性与 `NVLink` 有显著差异:

| 维度             | NVLink              | InfiniBand                 |
| -------------- | ------------------- | -------------------------- |
| GPU-GPU 单跳带宽   | 极高（600GB/s 级别 / 节点） | 受 NIC 限制（~25–50GB/s / GPU） |
| 延迟             | 极低（亚微秒级）            | 高于 NVLink（几微秒）             |
| 拓扑范围           | 仅限单节点               | 可跨节点扩展到上万 GPU              |
| 可扩展性           | 差（受主板/机箱限制）         | 极强（HPC/AI 超算核心）            |
| 可靠性            | 节点内高                | 网络级高可靠                     |
| 价格/功耗          | 昂贵但局部               | 昂贵但可规模化                    |
| 编程复杂度          | 透明                  | 需要网络栈、RDMA、注册              |
| NCCL 性能（小/中消息） | 更快                  | 略慢                         |
| NCCL 性能（大规模系统） | 不适用                 | 唯一可行                       |

