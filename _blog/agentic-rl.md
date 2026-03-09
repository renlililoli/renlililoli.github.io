---
title: "Agentic RL"
collection: blog
type: "blog"
date: 2026-03-06
excerpt: 'Playing with agentic RL.'
location: "Shanghai, China"
---

当前大模型后训练主要是通过RL来实现的，所以这个博客主要介绍一些agentic RL相关的知识。以下是AI总结的内容。每一个内容我自己也会写点总结。

---

## 1️⃣ RL 在 LLM 后训练中的核心目标

LLM 后训练中使用 RL 的核心目的通常是：

1. **Align LLM with Human Preferences（HRA / RLHF）**

   * 调整模型输出，使其更符合人类价值观、道德规范或偏好。
   * 核心思路：使用 RL 优化 **reward model** 得分，而非直接最大化语言模型对数似然。

2. **控制输出风格或约束**

   * 避免毒性内容（toxicity）、敏感信息泄露或不符合安全策略的生成。
   * 通过 RL 奖励合规输出、惩罚违规输出。

3. **改善任务完成度与实用性**

   * 在复杂任务中，例如代码生成、推理、多步决策，RL 可以鼓励更高效或更正确的输出。

---

## 2️⃣ 主要 RL 方法分类

### 2.1 RLHF（Reinforcement Learning from Human Feedback）

* **流程**：

  1. 用人工标注的示例训练 **Reward Model (RM)**。
  2. 让 LLM 生成输出，RM 对输出评分。
  3. 用 RL 优化 LLM，使其生成更高 RM 分数的输出。

* **常用算法**：

  * **PPO (Proximal Policy Optimization)**：OpenAI GPT 系列常用。
  * **A2C / TRPO / REINFORCE**：早期研究中也有使用。

* **关键文献**：

  * Christiano et al., 2017, *Deep Reinforcement Learning from Human Preferences*
  * OpenAI Blog, 2022, *Training language models to follow instructions with human feedback*

* **注意点**：

  * Reward Hacking 风险：模型可能找到投机取巧策略。
  * RLHF 主要在“后训练”阶段，不改变原始预训练权重结构。

---

### 2.2 RLAIF（RL from AI Feedback）

* **思路**：使用 AI 模型（而非人类）生成奖励信号，减少人工成本。
* **方法**：

  * 使用强大 LLM 作为“评判模型”，对候选输出打分。
  * RL 训练主模型优化分数。
* **应用**：可用于代码生成、文案生成、对话优化。
* **参考**：

  * Bai et al., 2023, *Training a Helpful and Harmless Assistant with RL from AI Feedback*

---

### 2.3 RL for Safety / Toxicity Avoidance

* **目标**：让模型主动避免生成不安全或有毒内容。
* **方法**：

  * 构建奖励函数：正向奖励安全输出，负向惩罚违规输出。
  * 可与 RLHF 结合。
* **参考**：

  * OpenAI, 2023, *Aligning Language Models to Avoid Harmful Content*
  * Perez et al., 2022, *Red Teaming Language Models with RL*

---

### 2.4 RL for Task-Specific Optimization

* **目标**：提升特定任务的完成度。
* **应用案例**：

  1. **代码生成**：用 RL 优化生成的代码是否能通过测试用例。
  2. **数学/逻辑推理**：奖励模型给出正确推理步骤。
  3. **对话任务**：奖励连贯性、信息量或用户满意度。
* **方法**：

  * Reward 可以是自动化程序（如单元测试）、评分模型或模拟环境反馈。
* **参考**：

  * Nakano et al., 2021, *WebGPT: Browser-assisted question answering with human feedback*
  * Hendrycks et al., 2021, *Aligning AI with human values via benchmarks and RL*

---

### 2.5 Agentic / Intrinsic Motivation RL in LLMs

* **思路**：

  * 给 LLM 添加 **自主探索能力**：

    * 自主生成问题 → 自我回答 → 自我奖励。
    * 内在奖励：信息增益、好奇心、能力提升。
* **目标**：

  * 增强模型在稀疏反馈环境下学习能力。
  * 可用于多步任务、规划型对话。
* **参考**：

  * Gato / DeepMind 多任务 agent 模型
  * OpenAI “AutoGPT / Reflexion” 系列探索自主反思 RL

---

### 2.6 RL for Multi-Modal / Grounded LLMs

* **目标**：让 LLM 在与外部环境交互时做出优化决策。
* **应用**：

  * 文本-代码-机器人控制任务
  * 文本-图像-交互系统
* **方法**：

  * 使用 RL 优化模型与外部环境交互的长期回报。
* **参考**：

  * OpenAI, 2023, *Training language models to interact with environments with RL*

---

## 3️⃣ 总结表格（Post-Training RL 在 LLM 的应用）

| 类别               | Reward 来源             | 算法                     | 应用        | 核心目标                        |
| ---------------- | --------------------- | ---------------------- | --------- | --------------------------- |
| RLHF             | 人类评分                  | PPO / TRPO / REINFORCE | 对话、指令遵循   | Align with human preference |
| RLAIF            | AI 模型评分               | PPO / REINFORCE        | 对话、生成任务   | 降低人工成本，优化输出                 |
| Safety RL        | 安全检测模型                | PPO / A2C              | 去毒性、合规性   | 避免违规内容                      |
| Task-Specific RL | 自动化测试/环境反馈            | PPO / REINFORCE        | 代码、推理、QA  | 提升任务完成度                     |
| Agentic RL       | 内在奖励（好奇心/empowerment） | PPO / intrinsic reward | 多步任务、自主探索 | 自主性、稀疏奖励学习                  |
| Multi-Modal RL   | 环境交互反馈                | PPO / Actor-Critic     | 文本-代码-环境  | 强化长期决策与规划                   |

---

## PPO

1. **采样（Generate batch）**

   * 使用当前策略 LLM（(\pi_\theta)）生成一批 prompt + completion：

     * prompt 固定
     * completion 是 model 逐 token 生成的 logits （注意这里尽管保留每个logits，但是还是要每次产生确定的token，即整个过程是autoregressive的）
   * 同时，每个 token 的 hidden state 输入 **value head** → 预测 token-level value (V(s_t))

2. **计算 reward**

   * Reward model 对整个生成序列打分 → 得到 **total reward (r_T)**
   * 其他 token reward (r_{t<T}=0)

3. **计算折算回报 / advantage（GAE）**

   * 对每条生成序列，计算 token-level **return 或 GAE**：
  $$
    \delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)
  $$
  $$
  A_t = \delta_t + (\gamma \lambda) \delta_{t+1} + ...
  $$
   * 这样即使 reward 稀疏，也能为每个 token 分配梯度信号

4. **计算 PPO loss**

   * **Policy loss**：clip probability ratio × advantage
      $$
      L_\text{policy} = \mathbb{E}_t[\min(r_t(\theta) A_t, \text{clip}(r_t(\theta),1-\epsilon,1+\epsilon) A_t)]
      $$
   * **Value loss**：MSE loss between value head output (V(s_t)) 和 GAE target
     $$
     L_\text{value} = \frac{1}{T} \sum_t (V(s_t) - \hat{V}_t)^2
     $$
   * **KL penalty**：限制策略漂移
     $$
     L_\text{KL} = \beta \cdot \text{KL}(\pi_\theta || \pi_\text{SFT})
     $$

5. **梯度更新**

   * 总 loss：
     $$
     L_\text{total} = L_\text{policy} + c_1 L_\text{value} - c_2 H + L_\text{KL}
     $$

     * (H) 是 entropy bonus，鼓励探索
     * (c_1, c_2) 是超参数
   * 对 LLM 权重做反向传播，更新策略和 value head 参数

6. **循环迭代**

   * 更新后的 LLM 再生成下一批序列 → 重复步骤 2~5
   * reward model 固定（一般不训练）

---

### 🔹 工程要点

* **prompt 不参与 value loss**：只对生成 token 做 loss mask
* **reward sparse** → GAE 或折扣回报传播优势
* **value head** 和 policy head **共享 Transformer** backbone，计算效率高
* **KL penalty** 防止模型“为了高 reward”生成奇怪输出
* **entropy bonus** 防止过早收敛，保证探索多样性

---

## DPO

DPO (Direct Preference Optimization) 是一种基于偏好学习的强化学习方法，旨在直接优化模型在特定偏好下的行为。与传统的 RL 方法不同，DPO 不使用奖励函数，而是直接学习模型在给定偏好下的最优行为。

DPO 的训练流程如下：

1. 收集偏好数据集 $D = \{(x_i, y_i, z_i)\}_i$, 在用LLM生产数据的时候要保存每个token对应的logits，用来之后计算损失函数。

2. 计算损失函数：
  $$
  L_\text{DPO} = \mathbb{E}_{(x, y, z) \sim D} [\log \pi_\theta(y|x) - \log \pi_{\theta}(z|x)]
  $$

3. 梯度更新：
  $$
  \nabla_\theta L_\text{DPO} = \mathbb{E}_{(x, y, z) \sim D} [\nabla_\theta \log \pi_\theta(y|x) - \nabla_\theta \log \pi_{\theta}(z|x)]
  $$  

为了训练的稳定性, 通常会加入一个KL散度约束:
  $$
  L_\text{DPO} = \mathbb{E}_{(x, y, z) \sim D} [\log \pi_\theta(y|x) - \log \pi_{\theta}(z|x)] + \beta \cdot \text{KL}(\pi_\theta || \pi_{\theta})
  $$

4. 梯度更新：
  $$
  \nabla_\theta L_\text{DPO} = \mathbb{E}_{(x, y, z) \sim D} [\nabla_\theta \log \pi_\theta(y|x) - \nabla_\theta \log \pi_{\theta}(z|x)] + \beta \cdot \nabla_\theta \text{KL}(\pi_\theta || \pi_{\theta})
  $$

5. 循环迭代：
  $$
  \theta_{t+1} = \theta_t - \alpha \cdot \nabla_\theta L_\text{DPO}
  $$

## GRPO

### GRPO 的数学形式

GRPO 的核心 surrogate objective（假设用组优势 + PPO clip + KL 正则）为：

$$
\mathcal{J}_\text{GRPO}(\theta) = \sum_{i=1}^G \min\big( r_i A_i, \operatorname{clip}(r_i,1-\epsilon,1+\epsilon) A_i \big)
- \beta D_\mathrm{KL}(\pi_\theta | \pi_\text{ref})
$$
  

$$
r_i = \frac{\pi_\theta(y_i|x)}{\pi_{\theta_\text{old}}(y_i|x)}
$$

```pythonlog_r = 0
for t, y_t in enumerate(sequence):
    logits_theta = model_theta.forward(seq[:t])
    logits_old = model_old.forward(seq[:t])
    
    p_theta = softmax(logits_theta)[y_t]
    p_old = softmax(logits_old)[y_t]
    
    log_r += log(p_theta) - log(p_old)

r = exp(log_r)
```

$$
A_i = R_i - \bar R
$$
 （组内标准化优势，或归一化）

---

## 3️⃣ 两样本 + 奖励为 ±1 时的退化

假设：

1. 组大小 (G = 2)
2. 奖励设为 (R(y_1) = +1, R(y_2) = -1)
3. 没有 clip（$(\epsilon\to\infty)$）和 KL 正则 ($(\beta = 0)$)

那么：

* 组平均 $(\bar R = (1 + (-1))/2 = 0)$
* 优势 $(A_1 = 1 - 0 = 1)，(A_2 = -1 - 0 = -1)$

代入 GRPO surrogate term：

$$
\mathcal{L}_\text{GRPO} \sim - \big[ r_1 \cdot 1 + r_2 \cdot (-1) \big] = - (r_1 - r_2)
$$

---

### 4️⃣ 用序列概率比表示

如果再把 $(r_i = \pi_\theta(y_i|x)/\pi_\text{ref}(y_i|x))$（假设 $(\pi_{\theta_\text{old}} = \pi_\text{ref})$），则：

$$
\mathcal{L}_\text{GRPO} \sim - \bigg( \frac{\pi_\theta(y_1|x)}{\pi_\text{ref}(y_1|x)} - \frac{\pi_\theta(y_2|x)}{\pi_\text{ref}(y_2|x)} \bigg)
$$

这个形式就是 DPO 的本质目标：**让模型相对参考模型在偏好输出上概率更高**。

如果进一步用 sigmoid 或 log-sigmoid 表示，就完全退化成 DPO：

$$
\mathcal{L}_\text{DPO} = - \log \sigma \Big( \log \frac{\pi_\theta(y_1|x)}{\pi_\text{ref}(y_1|x)} - \log \frac{\pi_\theta(y_2|x)}{\pi_\text{ref}(y_2|x)} \Big)
$$

✅ 所以结论是：

> **当 GRPO 的组大小为 2，奖励取 ±1，并且去掉 clip/KL 正则时，它严格退化为 DPO。**

---

也就是说 GRPO 是 DPO 的一个 **广义推广**：

* 多样化奖励（连续或多维） → GRPO
* 两样本 ±1 偏好 → DPO

## GSPO

GSPO是对GRPO的进一步正则化，核心在于由于长序列中概率连乘积会趋近于0，导致优势函数不稳定。因此GSPO将这个概率
$$
s_i = (\frac{\pi_\theta(y_i|x)}{\pi_{\theta_\text{old}}(y_i|x)})^{1/T}
$$
其中$T$是序列长度。

这样就可以避免概率连乘积趋近于0的问题。 但是问题在于这个并不是无偏的梯度的估计。 但是会极大增加训练的稳定性。


## PPO代码

1️⃣ 采样
2️⃣ reward + KL
3️⃣ GAE advantage
4️⃣ PPO loss

---

### 1 数据结构

一条 sample：

```text
prompt: x
completion: y = [y1 ... yT]

logprob_old[t]      # old policy log π_old(y_t|s_t)
logprob_ref[t]      # reference model log π_ref
value[t]            # value head V(s_t)
reward_model_score  # RM(x,y)
```

---

### 2 采样阶段

```python
for prompt in batch:

    completion, logprob_old, value = model.generate(prompt)

    logprob_ref = ref_model.logprob(prompt, completion)

    reward = reward_model(prompt, completion)

    store(
        prompt,
        completion,
        logprob_old,
        logprob_ref,
        value,
        reward
    )
```

**注意这里**： we use $\pi_\text{old}$ for pure inference, this combine prefill and decode stages. All logprob_old are saved. Then use the $\pi_\text{ref}$ to compute the logprob_ref. This only need to do prefill stage. No need to save compute graph. (Can this stage use quantized model?)

---

### reward shaping

RLHF 通常先把 KL 加进 reward。

```python
rewards = [0]*T
rewards[T-1] = shaped_reward
```

****

---

### 4 重新计算当前策略 logprob

PPO update 时需要 **新策略概率**：

```python
logprob_new = model.logprob(prompt, completion)
```

**注意这里**： 计算logprob_new，must use the new model and save compute graph. This need backward!!!(bf16 model need this). Alse the
value head are generated per token.

---

### 5 GAE 计算 advantage

Generalized Advantage Estimation：

```python
advantages = []
returns = []

gae = 0

for t in reversed(range(T)):

    delta = rewards[t] + gamma * values[t+1] - values[t]

    gae = delta + gamma * lambda_gae * gae

    advantages[t] = gae

    returns[t] = advantages[t] + values[t]
```

通常会做 **advantage normalization**：

```python
advantages = (advantages - mean) / (std + 1e-8)
```


---

### 6 PPO policy loss

importance ratio：

```python
ratio = exp(logprob_new - logprob_old)
```

clip：

```python
ratio_clipped = clip(ratio, 1-eps, 1+eps)
```

policy loss：

```python
loss_policy = -mean(
    min(
        ratio * advantage,
        ratio_clipped * advantage
    )
)
```

---

### 7 value loss

```python
loss_value = mean(
    (value_new - returns)**2
)
```

有些实现会 **clip value update**：

```python
value_clipped = value_old + clip(
    value_new - value_old,
    -value_clip,
    value_clip
)

loss_value = max(
    (value_new - returns)^2,
    (value_clipped - returns)^2
)
```

---

### 8 entropy bonus

鼓励 exploration：

```python
entropy = -sum(p * log p)

loss_entropy = -entropy_coef * entropy
```

---

### 9 总 loss

```python
loss =
    loss_policy
  + c1 * loss_value
  + loss_entropy
  + loss_kl(pi_theta, pi_ref)
```

注意：

KL **已经在 reward 里**。

---

### 10 完整 PPO step 伪代码

```python
for batch in rollout_buffer:

    logprob_new, value_new = model.forward(batch)

    ratio = exp(logprob_new - batch.logprob_old)

    ratio_clipped = clip(ratio, 1-eps, 1+eps)

    loss_policy = -mean(
        min(
            ratio * batch.advantage,
            ratio_clipped * batch.advantage
        )
    )

    loss_value = mean(
        (value_new - batch.return)**2
    )

    entropy = compute_entropy(logprob_new)
    loss_kl = compute_kl(logprob_new, logprob_ref)
    loss =
        loss_policy \
        + c1 * loss_value \
        - c2 * entropy \
        + loss_kl

    optimizer.step(loss)
```

---

### 11 LLM PPO 的几个关键工程细节

### 1 prompt token 不参与 loss

```python
mask = completion_mask
loss *= mask
```

---

### 2 每个 batch 会 update 多次

```python
for epoch in range(K_epochs):
    ppo_update()
```

常见：

```text
K_epochs = 4
```

---

### 3 adaptive KL coefficient

目标：

```text
target KL ≈ 0.1
```

动态调整：

```python
if kl > target:
    beta *= 1.5
else:
    beta /= 1.5
```

---

# 12 RLHF PPO pipeline 总流程

```text
SFT model
   │
   ▼
generate samples
   │
   ▼
reward model scoring
   │
   ▼
KL penalty
   │
   ▼
GAE advantage
   │
   ▼
PPO update
   │
   ▼
repeat
```

---

### 细节：

用专用的inference engine 来rollout和计算pi_ref。
不用save compute graph，只save logprob_old。这里为了加速pi_ref和pi_old都是低精度！它们可以单独使用gpu进行rollout，和训练gpu形成流水线。

单独用gpu来算reward model，这个模型可以用一个小模型。

用主要的gpu来存放训练模型，训练模型要求计算value head和logprob_new。

---
```text
┌─────────────────────────────────────────────────────────────────┐
│  Driver / Actor Trainer（控制流）                                  │
└─────────────────────────────────────────────────────────────────┘
         │
         │  1. prompts（list[str] 或 token_ids）
         ▼
┌─────────────────┐     Ray.remote() / ray.put()     ┌──────────────┐
│  Rollout (vLLM) │ ◄───────────────────────────────│  Prompt 池   │
│  GPU 0,1        │                                 │  (可来自     │
└────────┬────────┘                                 │   DataLoader)│
         │                                          └──────────────┘
         │  2. completion, logprob_old（序列化后放入 Ray Object Store）
         ▼
┌─────────────────┐     ray.get() / .remote()       ┌──────────────┐
│  Ref Model      │ ◄──────────────────────────────│ completions  │
│  GPU 2          │     (prompt + completion)       │ + prompts    │
└────────┬────────┘                                 └──────────────┘
         │
         │  3. logprob_ref
         ▼
┌─────────────────┐     .remote(prompt, completion)  ┌──────────────┐
│  Reward Model   │ ◄───────────────────────────────│ 同一批数据   │
│  GPU 3          │                                 │              │
└────────┬────────┘                                 └──────────────┘
         │
         │  4. reward scores
         ▼
┌─────────────────┐
│  Replay Buffer  │  ← 汇总：prompt, completion, logprob_old, 
│  (CPU / 共享)   │       logprob_ref, value, reward
└────────┬────────┘
         │
         │  5. 采样 batch，送入 PPO
         ▼
┌─────────────────┐
│  Actor + Critic │  训练 GPU（可单独一组，如 GPU 4,5,6,7）
│  (DeepSpeed)    │  - forward：logprob_new, value_new
│                 │  - backward：更新策略和 value head
└─────────────────┘

```