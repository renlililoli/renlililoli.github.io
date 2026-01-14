---
title: "LLM"
collection: blog
type: "blog"
date: 2025-11-02
excerpt: '学点大模型'
location: "Shanghai, China"
---

## Inference

大模型推理相关.

最近在看 [llama.cpp](https://github.com/ggml-org/llama.cpp), 感觉是相当有趣的项目, 纯c++实现了llama模型的推理, 并且支持量化. 最重要的是完全不依赖于blas库, 纯手搓算子. 内部不包含任何的卷积等不会在transformers模型中出现的操作.

### 快速上手

`llama.cpp`使用非常的简单, 从源仓库clone下来, 然后编译, 因为是完全独立的, 所以也不需要任何别的库, 尽管可以link blas 或者cublas等.

主要的功能在`llama-cli`中暴露了接口, 直接运行
```bash
./llama-cli --model ./models/7B/ggml-model-q4_0.ggml -t <core> --context-shifted -n <max context len>
```
就能进入交互式的对话模式, 其中`-t`指定使用的cpu核心数, `--context-shifted`表示使用shifted的上下文机制, `-n`表示上下文的最大长度.

我个人使用体验是7B模型在使用EPYC9754的128核心上非常流畅.

但是比较奇怪的是Q4_0量化的模型效果非常差, 几乎全是乱码, Q8就正常了, 感觉是量化的bug或者是cpu不支持某些指令集的缘故.

`llama.cpp`还支持server和webui模式,都很好用.


## LLM-RL

本科的时候学过一点强化学习, 所以想看看大模型和强化学习结合的东西. 之前看过很多qwen系列的文章和相关的博客,
也看过deepseek的一些介绍, 所以想看看LLM-RL的东西, 具体是什么样子的.

## 相关工作

找了一些知名高star的项目, 包括:
- [verl](https://github.com/volcengine/verl)
- [rllm](https://github.com/rllm-org/rllm)
- [ROLL](https://github.com/alibaba/ROLL)
- [lamorel](https://github.com/flowersteam/lamorel)
- [verifiers](https://github.com/PrimeIntellect-ai/verifiers)

当然目前准备看的是
[DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/pdf/2501.12948)

## 基本概念

- PPO (Proximal Policy Optimization) and GRPO (Generalized Ratio Policy Optimization)
- Reward Model (RM)
- Policy Model (PM)
- Supervised Fine-Tuning (SFT)
- Reinforcement Learning with Human Feedback (RLHF)

首先对于强化学习而言, 通常我们假设有一个策略, agent 根据当前的状态选择一个动作, 然后环境根据这个动作反馈一个奖励, 并且进入下一个状态. 这个过程不断重复, 直到达到某个终止条件. 强化学习的目标是学习一个最优的策略, 使得在长期内获得的累积奖励最大化.

通常深度强化学习使用神经网络来表示策略和价值函数. 比如当前的状态作为输入, 神经网络输出每个可能动作的概率分布(策略 $\pi_\theta(a|s)$)或者每个状态的预期奖励($V(s, a)$).

在LLM-RL中, 大语言模型(LLM)被用作策略网络, 生成文本作为动作. 状态可以是对话历史或者上下文信息. 奖励模型(RM)用于评估生成文本的质量, 并提供奖励信号.

### PPO算法

PPO是一种常用的强化学习算法, 其核心思想是通过限制策略更新的幅度来稳定训练过程. 具体来说,PPO通过引入一个剪切函数来限制新旧策略之间的差异, 避免策略更新过大导致训练不稳定. 

下面是策略梯度的基本公式推导.

---

$$
\nabla_\theta \mathbb{E}_{a\sim \pi_\theta}[R]
= \mathbb{E}_{a\sim \pi_\theta}[R \nabla_\theta \log \pi_\theta(a)]
$$

---
强化学习中的目标是最大化期望累积奖励:

$$
J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}[R(\tau)]
$$

其中$\tau$表示轨迹, $R(\tau)$表示轨迹的累积奖励. 对参数求导：

$$
\nabla_\theta J = \nabla_\theta \int p_\theta(\tau) R(\tau) d\tau
$$

$$
\nabla_\theta p_\theta(\tau) = p_\theta(\tau) \nabla_\theta \log p_\theta(\tau)
$$

代入：

$$
\nabla_\theta J = \int p_\theta(\tau) R(\tau) \nabla_\theta \log p_\theta(\tau) d\tau
$$

$$
= \mathbb{E}_{\tau \sim \pi_\theta}[R(\tau) \nabla_\theta \log p_\theta(\tau)]
$$

$$
p_\theta(\tau) = \prod_t \pi_\theta(a_t|s_t) P(s_{t+1}|s_t,a_t)
$$

环境转移不依赖 (\theta)，所以：

$$
\nabla_\theta \log p_\theta(\tau) = \sum_t \nabla_\theta \log \pi_\theta(a_t|s_t)
$$

代入得到最终的策略梯度公式：

$$
\nabla_\theta J = \mathbb{E}\left[\sum_t R(\tau)\nabla_\theta \log \pi_\theta(a_t|s_t)\right]
$$

引入 baseline 得：

$$
\nabla_\theta J = \mathbb{E}\left[\sum_t A_t\nabla_\theta \log \pi_\theta(a_t|s_t)\right]
$$


* $\pi_\theta(a_t|s_t)$ 是 softmax 输出概率
* $\log \pi_\theta$ 是 log-softmax
* 优化时就是对 token-level logprob 做加权最大化

---

而对于PPO而言, 其目标函数引入了一个剪切项, 同时使用优势函数(Advantage Function)来减少方差. 除此之外, PPO的对于 $\nabla_\theta \log \pi_\theta(a|s)$ 用了 重要性采样(importance sampling) 来计算: $\nabla_\theta\frac{\pi_\theta(a|s)}{\pi_{\theta_{old}}(a|s)}$. 当 $\frac{\pi_\theta(a|s)}{\pi_{\theta_{old}}(a|s)}$ 超过某个阈值时, 会被裁剪掉, 以防止策略更新过大. 此时用old作为分母是合理的.

重要性采样的目标是通过在一个分布下采样来估计另一个分布下的期望. 在PPO中, 我们希望估计新策略 $\pi_\theta$ 下的期望奖励, 但为了节省采样成本, 同一批样本多次训练, 
我们只能从旧策略 $\pi_{\theta_{old}}$ 下采样. 通过引入重要性权重 $\frac{\pi_\theta(a|s)}{\pi_{\theta_{old}}(a|s)}$, 我们可以调整旧策略下的样本以反映新策略下的分布.

```python
import torch
import torch.nn as nn
import torch.optim as optim

# =========================
# 1. 模型与环境
# =========================
policy = PolicyNetwork()      # 策略模型 pi_theta(a|s)
value_fn = ValueNetwork()     # critic V(s)
optimizer_policy = optim.Adam(policy.parameters(), lr=3e-6)
optimizer_value  = optim.Adam(value_fn.parameters(), lr=1e-3)

# 超参数
clip_epsilon = 0.2
gamma = 0.99
lambda_gae = 0.95

# =========================
# 2. Rollout 收集样本
# =========================
# 假设我们有 batch_size 个环境 / prompt
states, actions, rewards, dones, log_probs_old = [], [], [], [], []

for s in env_batch:   # 伪代码：每个环境/问题
    state = s.reset()
    done = False
    traj_reward = 0
    while not done:
        # 策略采样动作
        dist = policy(state)
        action = dist.sample()
        log_prob = dist.log_prob(action)

        next_state, reward, done, info = env.step(action)

        # 保存轨迹
        states.append(state)
        actions.append(action)
        rewards.append(reward)
        dones.append(done)
        log_probs_old.append(log_prob)

        state = next_state

# =========================
# 3. 计算 Advantage (GAE)
# =========================
advantages = []
returns = []
gae = 0
next_value = 0
for t in reversed(range(len(rewards))):
    delta = rewards[t] + gamma * next_value * (1 - dones[t]) - value_fn(states[t])
    gae = delta + gamma * lambda_gae * (1 - dones[t]) * gae
    advantages.insert(0, gae)
    returns.insert(0, gae + value_fn(states[t]))
    next_value = value_fn(states[t])

advantages = torch.tensor(advantages)
returns = torch.tensor(returns)
log_probs_old = torch.tensor(log_probs_old)

# =========================
# 4. PPO surrogate loss
# =========================
for _ in range(ppo_epochs):
    dist = policy(states)
    log_probs = dist.log_prob(actions)
    ratio = (log_probs - log_probs_old).exp()   # pi_theta / pi_old

    # clipped surrogate objective
    surr1 = ratio * advantages
    surr2 = torch.clamp(ratio, 1.0 - clip_epsilon, 1.0 + clip_epsilon) * advantages
    policy_loss = -torch.min(surr1, surr2).mean()

    # value function loss
    value_loss = nn.MSELoss()(value_fn(states), returns)

    # optimize
    optimizer_policy.zero_grad()
    policy_loss.backward()
    optimizer_policy.step()

    optimizer_value.zero_grad()
    value_loss.backward()
    optimizer_value.step()
```

### GRPO算法

GRPO (Generalized Ratio Policy Optimization) 是PPO的一种扩展, 其主要思想是通过引入更一般化的比例函数来替代PPO中的优势函数. 这样可以更灵活地调整策略更新的幅度, 以适应不同的任务和环境.

对于PPO而言, 每次动作是产生一个token, 但是GRPO可以把一段文本作为一个整体动作. 这样的好处是使得训练更加稳定. 某种意义上, GRPO是一个单步的决策.

```python

# 假设策略和旧策略已经定义好
policy = ...       # 任何策略模型，返回 logits
pi_old = ...       # 旧策略，复制 policy 参数

optimizer = torch.optim.Adam(policy.parameters(), lr=lr)

# 假设 reward_model 已经定义好
def reward_model(states, actions):
    return torch.rand(len(actions))  # 仅示意

# 训练循环（单步示意）
for batch in range(100):
    states = torch.randn(batch_size, state_dim)

    all_advantages, all_log_probs_old, all_actions = [], [], []

    for state in states:
        dist_old = pi_old.get_dist(state)
        actions = dist_old.sample((G,))
        rewards = reward_model(state.repeat(G,1), actions)

        baseline = rewards.mean()
        advantages = rewards - baseline

        all_advantages.append(advantages)
        all_log_probs_old.append(dist_old.log_prob(actions))
        all_actions.append(actions)

    all_advantages = torch.cat(all_advantages)
    all_log_probs_old = torch.cat(all_log_probs_old)
    all_actions = torch.cat(all_actions)

    # 新策略
    dist_new = policy.get_dist(states.repeat(G,1))
    log_probs_new = dist_new.log_prob(all_actions)

    # ratio 和 clip
    ratio = torch.exp(log_probs_new - all_log_probs_old)
    surr1 = ratio * all_advantages
    surr2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * all_advantages
    policy_loss = -torch.min(surr1, surr2).mean()

    # KL penalty
    kl = torch.distributions.kl_divergence(dist_old, dist_new).mean()
    loss = policy_loss + kl_beta * kl

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

### Reward Model

奖励模型用于评估生成文本的质量, 并提供奖励信号. 通常奖励模型是一个预训练的语言模型, 通过监督学习或者对比学习进行微调, 使其能够区分高质量和低质量的文本.

在`Deepseek-R1-Zero`中, 奖励并非来自训练的模型, 而是使用基于规则的评分, 例如数学题的正确性, 编程题的通过率等. 除此之外还有一些格式上的要求. 准确性和格式正确性等权相加权重作为最终的奖励.

具体而言，他们在 DeepSeek-V3 基座模型之上应用强化学习技术来训练 DeepSeek-R1-Zero。在训练过程中，要求 DeepSeek-R1-Zero 先生成推理过程，再给出最终答案。有意将约束限制在这种结构化格式层面，而避免施加任何内容相关的偏置，以确保能够真实地观察模型在强化学习过程中的自然演化轨迹。

## Deepseek-R1

`Deepseek-R1-Zero`已经有很强的推理能力, 然而它有一些问题, 包括回答可读性差, 推理混杂不同语言.

Updating...




