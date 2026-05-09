---
title: "DLM: Whale-4B-Base"
collection: blog
type: "blog"
date: 2026-05-09
excerpt: 'Whaletech open-source DLM model.'
location: "Shanghai, China"
---

去了一家初创大模型公司面试。他们发了一个[开源的小模型](https://github.com/whaletech-ai/W1-4B-dLLM-Base)，看看他们使用的架构是什么样子的。（本来想继续面的可惜已经找到了满意的地方就决定不继续了。。。

## 基本架构

首先架构核心采用的是经典的transformer DIT做序列建模。整个架构的流程大概是：

### Main

```mermaid
flowchart TD

    %% ===== Input =====
    P["Prompt text"]
    T["Timesteps t"]

    %% ===== Token pipeline =====
    P --> TOK["Tokenizer"]

    TOK --> IDS["input_ids<br/>prompt tokens + MASK tokens"]

    IDS --> EMB["TokenEmbedding"]

    EMB --> X["x: token hidden states"]

    %% ===== Time conditioning =====
    T --> TEMB["TimestepEmbedding"]

    TEMB --> C["c: conditioning vector"]

    %% ===== Transformer backbone =====
    X --> BLOCKS["DiT Blocks × depth"]

    C --> BLOCKS

    %% ===== Final conditioning =====
    BLOCKS --> FINAL["FinalAdaLN"]

    C --> FINAL

    %% ===== LM head =====
    FINAL --> H["hidden states"]

    H --> HEAD["lm_head Linear"]

    HEAD --> LOGITS["logits<br/>B × T × vocab_size"]

    %% ===== Sampling =====
    LOGITS --> SAMPLER["Diffusion Sampler<br/>standard / jump / GIDD"]

    IDS --> SAMPLER
    T --> SAMPLER

    %% ===== Token update =====
    SAMPLER --> UPDATE["Update editable tokens only<br/>keep prompt prefix fixed"]

    UPDATE --> OUT["Generated text"]

    %% ===== Styles =====

    %% Raw input
    classDef input fill:#ECECEC,stroke:#666,color:#000;

    %% Token processing
    classDef token fill:#E8F0FE,stroke:#4A90E2,color:#000;

    %% Conditioning
    classDef cond fill:#F3E5F5,stroke:#8E44AD,color:#000;

    %% Core transformer compute
    classDef core fill:#D5F5E3,stroke:#27AE60,color:#000;

    %% Sampling process
    classDef sample fill:#FFF3CD,stroke:#F39C12,color:#000;

    %% Output
    classDef output fill:#FDEDEC,stroke:#C0392B,color:#000;

    class P,T input;

    class TOK,IDS,EMB,X token;

    class TEMB,C cond;

    class BLOCKS,FINAL,H,HEAD,LOGITS core;

    class SAMPLER,UPDATE sample;

    class OUT output;
```

### DIT block
```mermaid
flowchart TD

    %% ===== Inputs =====
    X[x input]
    C[c conditioning]
    ROPE[RoPE]

    %% ===== AdaLN condition branch =====
    C --> ADA["adaLN MLP<br/>SiLU + Linear"]
    ADA --> SPLIT["Split into 6 vectors"]

    SPLIT --> SMSA["shift_msa"]
    SPLIT --> SCSA["scale_msa"]
    SPLIT --> GMSA["gate_msa"]

    SPLIT --> SMLP["shift_mlp"]
    SPLIT --> SCMLP["scale_mlp"]
    SPLIT --> GMLP["gate_mlp"]

    %% ===== Attention branch =====
    X --> N1["RMSNorm"]

    N1 --> MOD1["AdaLN Modulate<br/>x * (1+scale) + shift"]

    SMSA --> MOD1
    SCSA --> MOD1

    MOD1 --> ATTN["Self Attention"]

    ROPE --> ATTN

    ATTN --> GM1["Multiply gate_msa"]

    GMSA --> GM1

    X --> RES1["Residual Add"]

    GM1 --> RES1

    %% ===== MLP branch =====
    RES1 --> N2["RMSNorm"]

    N2 --> MOD2["AdaLN Modulate<br/>x * (1+scale) + shift"]

    SMLP --> MOD2
    SCMLP --> MOD2

    MOD2 --> FFN["SwiGLU FFN"]

    FFN --> GM2["Multiply gate_mlp"]

    GMLP --> GM2

    RES1 --> RES2["Residual Add"]

    GM2 --> RES2

    RES2 --> OUT["Block Output"]

    %% ===== Styles =====

    %% Norm
    classDef norm fill:#E8F0FE,stroke:#4A90E2,color:#000;

    %% Conditioning
    classDef cond fill:#F3E5F5,stroke:#8E44AD,color:#000;

    %% AdaLN modulation
    classDef mod fill:#FFF3CD,stroke:#F39C12,color:#000;

    %% Core transformer compute
    classDef core fill:#D5F5E3,stroke:#27AE60,color:#000;

    %% Residual / gating
    classDef residual fill:#FDEDEC,stroke:#C0392B,color:#000;

    %% Output
    classDef output fill:#ECECEC,stroke:#666,color:#000;

    class N1,N2 norm;
    class ADA,SPLIT,SMSA,SCSA,GMSA,SMLP,SCMLP,GMLP,C cond;
    class MOD1,MOD2 mod;
    class ATTN,FFN,ROPE core;
    class GM1,GM2,RES1,RES2 residual;
    class OUT output;
```

### config

```yaml
model:
  vocab_size: 64512
  hidden_size: 2048
  attn_dim: 3072
  ffn_dim: 7168
  depth: 48
  num_heads: 24
  head_dim: 128
  max_seq_len: 4096
  timestep_freq_dim: 256
  rope_theta: 10000.0
  cond_dim: 256
  dropout: 0.0
  attn_dropout: 0.0

diffusion:
  mask_token_id: 14
```

## 采样

模型使用了两种方式进行生成，一种是启发式的，每次从$x_t$进入模型得到$x_0$,固定最高置信度的部分token，迭代生成；另一种就是使用GIDD，真正的离散扩散采样。

### Jump

```mermaid
flowchart TD

    X0["x_t<br/>prompt + MASK tokens"]

    T["timestep t"] --> MODEL
    X0 --> MODEL

    MODEL["LangDiT model"] --> LOGITS["token logits"]

    LOGITS --> SAMPLE["Sample candidate tokens"]

    SAMPLE --> CONF["Compute confidence"]

    CONF --> PICK["Pick highest-confidence MASK positions"]

    PICK --> FILL["Fill selected MASK tokens"]

    %% Jump phase
    FILL --> JUDGE{"Late jump phase?"}

    JUDGE -- yes --> LOWCONF["Find low-confidence generated tokens"]

    LOWCONF --> ALT["Resample alternative tokens"]

    ALT --> UPDATE["Update uncertain tokens"]

    JUDGE -- no --> UPDATE

    UPDATE --> FIX["Keep prompt prefix fixed"]

    FIX --> NEXT["x_s<br/>more refined tokens"]

    NEXT --> LOOP{"More timesteps?"}

    LOOP -- yes --> X0

    LOOP -- no --> OUT["Final generated text"]

    %% ===== Styles =====

    classDef state fill:#E8F0FE,stroke:#4A90E2,color:#000;
    classDef model fill:#D5F5E3,stroke:#27AE60,color:#000;
    classDef heuristic fill:#FFF3CD,stroke:#F39C12,color:#000;
    classDef output fill:#FDEDEC,stroke:#C0392B,color:#000;

    class X0,NEXT state;
    class MODEL,LOGITS model;
    class SAMPLE,CONF,PICK,FILL,LOWCONF,ALT,UPDATE,FIX heuristic;
    class OUT output;
```

### GIDD

```mermaid
flowchart TD

    XT["x_t<br/>current noisy tokens"]

    T["current timestep t"]
    S["next timestep s"]

    XT --> MODEL
    T --> MODEL

    MODEL["LangDiT model"] --> P0["Predict p_theta(x0 | x_t)"]

    %% Forward distributions
    P0 --> QT["Construct q_t<br/>alpha_t * p0 + noise"]

    P0 --> QS["Construct q_s<br/>alpha_s * p0 + noise"]

    T --> QT
    S --> QS

    %% Posterior
    QT --> POST["Compute reverse posterior<br/>q(x_s | x_t, x0)"]

    QS --> POST
    XT --> POST

    %% Sampling
    POST --> SAMPLE["Sample x_s from posterior"]

    SAMPLE --> FIX["Keep prompt prefix fixed"]

    FIX --> XS["x_s<br/>cleaner token state"]

    XS --> LOOP{"More timesteps?"}

    LOOP -- yes --> XT

    LOOP -- no --> OUT["Final generated text"]

    %% ===== Styles =====

    classDef state fill:#E8F0FE,stroke:#4A90E2,color:#000;
    classDef model fill:#D5F5E3,stroke:#27AE60,color:#000;
    classDef diffusion fill:#F3E5F5,stroke:#8E44AD,color:#000;
    classDef posterior fill:#FFF3CD,stroke:#F39C12,color:#000;
    classDef output fill:#FDEDEC,stroke:#C0392B,color:#000;

    class XT,XS state;

    class MODEL,P0 model;

    class QT,QS diffusion;

    class POST,SAMPLE,FIX posterior;

    class OUT output;
```