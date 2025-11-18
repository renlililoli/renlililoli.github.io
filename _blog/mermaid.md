---
title: "使用mermaid画出好看的图"
collection: blog
type: "blog"
date: 2025-11-18
excerpt: '太好用了, 快速画图的神'
location: "Sanya, China"
---

在用ai写文档的时候发现它会生成一些非常好看的图, 值得仔细研究一下.

但是主页好像渲染不了, 必须在vscode里下载mermaid插件才行.

## render test
<div class="mermaid">
graph TD
    A --> B
</div>


## 流程图

基本语法是

```
obj[descriptor] --> |arrow descriptor| obj[description]
```
其中mermaid提供了不同的样式

{% raw %}
```mermaid
graph TD
    A[方框] -.-> B(圆角)
    B ==> C((圆形))
    C --- D[[子程序]]
    D --> E[/输入/]
    E --o A{判断?}
    F --x G{{数据}}
    G --> H[(数据库)]
```
{% endraw %}

```mermaid
graph TD
    A[开始] --> B[处理数据]
    B --> C{条件?}
    C -->|是| D[动作1]
    C -->|否| E[动作2]
    D --> F[结束]
    E --> F
    F --> |循环| A
```

## 流程图
```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    note over A: test
    note over A,B: test
    B->>B: test
    A->>B: 你好
    note over B: test
    B-->>A: 收到
```

## 甘特图
```mermaid
gantt
    title 项目计划
    section 开发
    设计       :done, d1, 2025-01-01, 7d
    实现       :active, d2, 2025-01-08, 10d
```

## 状态
```mermaid
stateDiagram
    A --> B: 条件
    B --> C
```

## 树
```mermaid
mindmap
  root
    test-1
    子节点1
      test0
    子节点2
      test
      test1
```

## circuit

好像用sequence没办法画circuit, 因为没办法指向用来做gate的note框

```mermaid
sequenceDiagram
    participant 0 as q0
    participant 1 as q1
    participant 2 as q2
    participant 3 as q3

    note over 0: X
    note over 0,2: CCX
```