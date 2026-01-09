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

Updating...