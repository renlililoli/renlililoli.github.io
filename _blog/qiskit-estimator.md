---
title: "Why Qiskit Estimator is Fast?"
collection: blog
type: "blog"
date: 2025-11-15
excerpt: 'Discover the speed advantages of Qiskit Estimator for quantum computing tasks. Learn how it optimizes performance and efficiency in quantum simulations.'
location: "Shanghai, China"
---

一直困扰我的一个问题是:为什么 Qiskit Estimator 来计算类似于 $\bra{\psi}H\ket{\psi}$ 这样简单的期望值时, 速度会比直接用量子电路模拟器来得更快?

## 代码

我看到 `EstimatorV2` 里的核心在于根据 `SparsePauliOp` 来构造要运行的量子电路, 代码如下

```python
for pauli in paulis:
    circuit.save_expectation_value(
        Pauli(pauli), qubits=range(circuit.num_qubits), label=pauli
    )
result = self._backend.run(
    circuit, parameter_binds=[parameter_binds], **self.options.run_options
).result()
```

这里我猜测重点在于 `circuit.save_expectation_value` 这一行, 它会直接在量子电路里插入计算期望值的指令, 这样就避免了我们自己去测量然后再计算期望值的过程. 也就是本质上, 它把测量和计算期望值的步骤合并到了量子电路的执行过程中, 从而节省了时间. 因此只有1个量子线路就能计算出所有 Pauli 项的期望值, 而不需要为每个 Pauli 项都运行一次量子电路.

## 实验

我们使用 Qiskit 里的 Aer 模拟器来计算一个 8 qubits 的量子态在一个化学哈密顿量下的期望值. 具体的代码如下:

### `EstimatorV2`

```python
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper

from qiskit import QuantumCircuit, transpile
from qiskit.circuit import random
from qiskit_aer import Aer, AerSimulator
from qiskit_aer.primitives import EstimatorV2

import time

mapper=JordanWignerMapper()

driver = PySCFDriver(atom=f'H 0 0 0; H 0 0 {0.735}',
                     charge=0,
                     spin=0,
                     unit=DistanceUnit.ANGSTROM,
                     basis='6-31g')

es_problem = driver.run()
second_q_ops = es_problem.second_q_ops()
pauli_op = mapper.map(second_q_ops[0])

thr = 1
N = 10

estimator = EstimatorV2(
    options= {
        'backend_options': {
            'max_parallel_threads': thr,
            'max_parallel_experiments': thr, # defalut set to thr is passed 0
            'max_parallel_shots': thr,
            'method': 'statevector',
            'shots': 1,
        }
    }
)
backend = Aer.get_backend('statevector_simulator')

rand_stat = random.random_circuit(num_qubits=pauli_op.num_qubits, depth=1000, seed=42)
rand_stat = transpile(rand_stat, backend=backend)

print("Number of qubits:", pauli_op.num_qubits)
print("Number of Pauli terms:", len(pauli_op.to_list()))


# Warm up
job = estimator.run([
        (rand_stat, pauli_op),
        ])
result = job.result()

t = time.time()

job = estimator.run([(rand_stat, pauli_op),] * N)
result = job.result()

print("Elapsed time for total Pauli:", (time.time() - t) / N)
t = time.time()
job = estimator.run([(rand_stat, pauli_op[0]),] * N)
result = job.result()

print("Elapsed time for single Pauli:", (time.time() - t) / N)
```

运行上面的代码, 我们可以得到如下的结果:

```
Number of qubits: 8
Number of Pauli terms: 185
Elapsed time for total Pauli: 0.33776164054870605
Elapsed time for single Pauli: 0.25511369705200193
```

符合预期.

> 好吧调的过程中又遇到了奇怪的问题, 只有seed=42能跑通, 其他的seed都会报错, 这里就先凑合着用42吧. 太诡异了... 这个 42 还是自动补全帮我生成的, 不得不感慨qiskit就是一大坨.

```python
backend = Aer.get_backend('statevector_simulator')

rand_stat = random.random_circuit(num_qubits=pauli_op.num_qubits, depth=1000, seed=42)
rand_stat = transpile(rand_stat, backend=backend)
```

### `save_expectation_value`

`circuit.save_expectation_value` 这个方法会在线路中插入 [`SaveExpectationValue`](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.library.SaveExpectationValue.html#qiskit_aer.library.SaveExpectationValue)

它的具体实现在 `qiskit_aer`中的 `simulators/statevector/statevector_executor.hpp`
```cpp
template <class state_t>
double Executor<state_t>::expval_pauli(const reg_t &qubits,
                                       const std::string &pauli) {
  reg_t qubits_in_chunk;
  reg_t qubits_out_chunk;
  std::string pauli_in_chunk;
  std::string pauli_out_chunk;
  uint_t n;
  double expval(0.);

  // get inner/outer chunk pauli string
  n = pauli.size();
  for (uint_t i = 0; i < n; i++) {
    if (qubits[i] < BasePar::chunk_bits_) {
      qubits_in_chunk.push_back(qubits[i]);
      pauli_in_chunk.push_back(pauli[n - i - 1]);
    } else {
      qubits_out_chunk.push_back(qubits[i]);
      pauli_out_chunk.push_back(pauli[n - i - 1]);
    }
  }

  if (qubits_out_chunk.size() > 0) { // there are bits out of chunk
    std::complex<double> phase = 1.0;

    std::reverse(pauli_out_chunk.begin(), pauli_out_chunk.end());
    std::reverse(pauli_in_chunk.begin(), pauli_in_chunk.end());

    uint_t x_mask, z_mask, num_y, x_max;
    std::tie(x_mask, z_mask, num_y, x_max) =
        AER::QV::pauli_masks_and_phase(qubits_out_chunk, pauli_out_chunk);

    AER::QV::add_y_phase(num_y, phase);

    if (x_mask != 0) { // pairing state is out of chunk
      bool on_same_process = true;
#ifdef AER_MPI
      uint_t proc_bits = 0;
      uint_t procs = Base::distributed_procs_;
      while (procs > 1) {
        if ((procs & 1) != 0) {
          proc_bits = 0;
          break;
        }
        proc_bits++;
        procs >>= 1;
      }
      if ((x_mask & (~((1ull << (Base::num_qubits_ - proc_bits)) - 1))) !=
          0) { // data exchange between processes is required
        on_same_process = false;
      }
#endif

      x_mask >>= BasePar::chunk_bits_;
      z_mask >>= BasePar::chunk_bits_;
      x_max -= BasePar::chunk_bits_;

      const uint_t mask_u = ~((1ull << (x_max + 1)) - 1);
      const uint_t mask_l = (1ull << x_max) - 1;
      if (on_same_process) {
        auto apply_expval_pauli_chunk = [this, x_mask, z_mask, x_max, mask_u,
                                         mask_l, qubits_in_chunk,
                                         pauli_in_chunk, phase](int_t iGroup) {
          double expval_t = 0.0;
          for (uint_t iChunk = Base::top_state_of_group_[iGroup];
               iChunk < Base::top_state_of_group_[iGroup + 1]; iChunk++) {
            uint_t pair_chunk = iChunk ^ x_mask;
            if (iChunk < pair_chunk) {
              uint_t z_count, z_count_pair;
              z_count = AER::Utils::popcount(iChunk & z_mask);
              z_count_pair = AER::Utils::popcount(pair_chunk & z_mask);

              expval_t += Base::states_[iChunk - Base::global_state_index_]
                              .qreg()
                              .expval_pauli(qubits_in_chunk, pauli_in_chunk,
                                            Base::states_[pair_chunk].qreg(),
                                            z_count, z_count_pair, phase);
            }
          }
          return expval_t;
        };
        expval += Utils::apply_omp_parallel_for_reduction(
            (BasePar::chunk_omp_parallel_ && Base::num_groups_ > 1), 0,
            Base::num_global_states_ / 2, apply_expval_pauli_chunk);
      } else {
        for (uint_t i = 0; i < Base::num_global_states_ / 2; i++) {
          uint_t iChunk = ((i << 1) & mask_u) | (i & mask_l);
          uint_t pair_chunk = iChunk ^ x_mask;
          uint_t iProc = BasePar::get_process_by_chunk(pair_chunk);
          if (Base::state_index_begin_[Base::distributed_rank_] <= iChunk &&
              Base::state_index_end_[Base::distributed_rank_] >
                  iChunk) { // on this process
            uint_t z_count, z_count_pair;
            z_count = AER::Utils::popcount(iChunk & z_mask);
            z_count_pair = AER::Utils::popcount(pair_chunk & z_mask);

            if (iProc == Base::distributed_rank_) { // pair is on the
                                                    // same process
              expval +=
                  Base::states_[iChunk - Base::global_state_index_]
                      .qreg()
                      .expval_pauli(
                          qubits_in_chunk, pauli_in_chunk,
                          Base::states_[pair_chunk - Base::global_state_index_]
                              .qreg(),
                          z_count, z_count_pair, phase);
            } else {
              BasePar::recv_chunk(iChunk - Base::global_state_index_,
                                  pair_chunk);
              // refer receive buffer to calculate expectation value
              expval +=
                  Base::states_[iChunk - Base::global_state_index_]
                      .qreg()
                      .expval_pauli(
                          qubits_in_chunk, pauli_in_chunk,
                          Base::states_[iChunk - Base::global_state_index_]
                              .qreg(),
                          z_count, z_count_pair, phase);
            }
          } else if (iProc == Base::distributed_rank_) { // pair is on
                                                         // this process
            BasePar::send_chunk(iChunk - Base::global_state_index_, pair_chunk);
          }
        }
      }
    } else { // no exchange between chunks
      z_mask >>= BasePar::chunk_bits_;
      if (BasePar::chunk_omp_parallel_ && Base::num_groups_ > 1) {
#pragma omp parallel for reduction(+ : expval)
        for (int_t ig = 0; ig < (int_t)Base::num_groups_; ig++) {
          double e_tmp = 0.0;
          for (uint_t iChunk = Base::top_state_of_group_[ig];
               iChunk < Base::top_state_of_group_[ig + 1]; iChunk++) {
            double sign = 1.0;
            if (z_mask && (AER::Utils::popcount(
                               (iChunk + Base::global_state_index_) & z_mask) &
                           1))
              sign = -1.0;
            e_tmp += sign * Base::states_[iChunk].qreg().expval_pauli(
                                qubits_in_chunk, pauli_in_chunk);
          }
          expval += e_tmp;
        }
      } else {
        for (uint_t i = 0; i < Base::states_.size(); i++) {
          double sign = 1.0;
          if (z_mask &&
              (AER::Utils::popcount((i + Base::global_state_index_) & z_mask) &
               1))
            sign = -1.0;
          expval += sign * Base::states_[i].qreg().expval_pauli(qubits_in_chunk,
                                                                pauli_in_chunk);
        }
      }
    }
  } else { // all bits are inside chunk
    if (BasePar::chunk_omp_parallel_ && Base::num_groups_ > 1) {
#pragma omp parallel for reduction(+ : expval)
      for (int_t ig = 0; ig < (int_t)Base::num_groups_; ig++) {
        double e_tmp = 0.0;
        for (uint_t iChunk = Base::top_state_of_group_[ig];
             iChunk < Base::top_state_of_group_[ig + 1]; iChunk++)
          e_tmp += Base::states_[iChunk].qreg().expval_pauli(qubits, pauli);
        expval += e_tmp;
      }
    } else {
      for (uint_t i = 0; i < Base::states_.size(); i++)
        expval += Base::states_[i].qreg().expval_pauli(qubits, pauli);
    }
  }

#ifdef AER_MPI
  BasePar::reduce_sum(expval);
#endif
  return expval;
}
```

### 解释(来自于AI)

生成 bit-mask

Aer 为 Pauli 字符串生成三个重要掩码:

✔ x_mask:所有需要被 X/Y 翻转的 qubit

对应 Pauli 中 X 或 Y

✔ z_mask:所有需要检查 sign 的位

对应 Pauli 中 Z 或 Y

✔ num_y:遇到的 Y 个数

这些掩码帮助 Aer 确定哪些 qubit 需要翻转以及在计算期望值时需要考虑的符号变化.

| qubit | P | x_mask | z_mask | y_count |
| ----- | - | ------ | ------ | ------- |
| 0     | Y | flip   | sign   | +1      |
| 1     | I | -      | -      | 0       |
| 2     | Z | -      | sign   | 0       |
| 3     | X | flip   | -      | 0       |

#### 🎯 Case 1: 没有 X/Y(Z-only Pauli)
```cpp
double exp = 0;
for (i=0; i < dim; i++) {
    double sign = ((popcount(i & z_mask) & 1) ? -1.0 : +1.0);
    exp += sign * std::norm(data[i]);
}
return exp;
```
对于仅包含 Z 的 Pauli 字符串, 计算期望值相对简单. Aer 遍历所有状态向量的幅度, 使用 z_mask 来确定每个基态的符号贡献. 如果与 z_mask 的位与运算结果中 1 的数量是奇数, 则该基态贡献 -1, 否则贡献 +1. 最终将所有基态的贡献累加得到期望值.

#### 🎯 Case 2: 含有 X/Y (General Pauli)
```cpp
double exp = 0;
for (i=0; i < dim; i++) {
    j = i ^ x_mask;     // find paired state

    if (i < j) {
        int z1 = popcount(i & z_mask);
        int z2 = popcount(j & z_mask);
        double sign = ((z1 + z2) & 1? -1: +1);

        exp += 2 * real( conj(data[i]) * (phase * sign) * data[j] );
    }
}
return exp;
```

解释:

✔ i < j 避免重复计算

因为 (i,j) 和 (j,i) 会出现重复.

✔ multiply the real part ×2

因为:

$$
    \psi_i^\dagger\psi_j + \psi_j^\dagger\psi_i = 2 \cdot \text{Re}(\psi_i^\dagger\psi_j)
$$
✔ Z mask sign

如果 Pauli 有 Z 或 Y，要检查 sign:

$$
(-1)^{\text{popcount}(i \& z_{\text{mask}})}
$$
✔ Y 的相位(i 或 -i)

已预先合并在 phase 中.

### 总结

很有趣的实现, 通过位运算和掩码来高效地计算期望值, 避免了显式地构造测量电路和多次运行量子电路的开销. 这正是 Qiskit Estimator 能够在计算期望值时表现出色性能的关键原因之一.