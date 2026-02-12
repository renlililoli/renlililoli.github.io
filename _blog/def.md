---
title: "DEF file in EDA"
collection: blog
type: "blog"
date: 2026-02-12
excerpt: 'An in-depth look at DEF files in EDA and their role in the design process.'
location: "Shanghai, China"
---

在EDA中, DEF（Design Exchange Format）文件是一种用于描述集成电路设计的标准格式。它包含了设计的物理布局、连接信息以及其他相关数据。DEF文件通常由设计工具生成，并被用于后续的设计验证、布局优化和制造流程中。

## HEADER

```
VERSION 5.8 ;
DIVIDERCHAR "/" ;
BUSBITCHARS "[]" ;
DESIGN top_name ;
UNITS DISTANCE MICRONS 1000 ;
DIEAREA ( 0 0 ) ( 200000 200000 ) ;
```

其中dividerchar指定路径分隔符, 如 `top/module1/instanceA`. 而busbitchars指定总线位的表示方式, 如 `data[0]`, `data[1]` 等, 因为总线信号通常包含多个位, 可以想象是多条线的集合.

## ROW

```nginx
ROW R_even core 0 0 N  DO 100 BY 1 STEP 2000 0 ;
ROW R_odd  core 0 200 FS DO 100 BY 1 STEP 2000 0 ;

ROW <rowName> <siteName> <origX> <origY> <orient>
    DO <numX> BY <numY>
    STEP <stepX> <stepY> ;
```

前两行表示两个对顶的row, 分别在y=0和y=200的位置, 每行有100个site, 每个site宽2000, 高200. 朝向相反通常是为了供电和信号完整性考虑.

```nginx
SITE core
  SIZE 2000 BY 200 ;
  CLASS CORE ;
  SYMMETRY Y ;
END core
```

这个 ROW 定义本质是：

$$
(x,y)=(origX+i⋅stepX,origY+j⋅stepY)\\
0≤i<DO,0≤j<BY
$$

orientation 决定变换矩阵。

| 方向 | 含义     |
| -- | ------ |
| N  | 正向     |
| S  | 旋转180° |
| FN | 水平翻转   |
| FS | 垂直翻转   |


ROW定义了芯片布局中的行信息, 包括行名称、类型、起始坐标、方向以及重复模式等. 这些行通常用于放置标准单元, 并且通过DO和STEP参数指定了行的重复方式, 以便在芯片上均匀分布标准单元.

我们知道, 在芯片设计中, 标准单元通常被排列在预定义的行中. 通过ROW定义, 我们可以清晰地描述这些行的布局和分布方式, 这对于后续的布局优化和设计验证非常重要. 对于通常的2D设计, ROW只有X和Y坐标, 因此通常会把Y方向/垂直row方向称为cell的height方向, 而X方向/水平row方向称为cell的width方向.

ROW一般用来对齐标准单元的放置, 在placement中被称作legalization.

## TRACK

TRACKS 是 routing grid 的定义，它描述的是：

在某一金属层上，允许布线的“离散轨道位置”。

和 ROW 不同：

ROW → 给标准单元放置用（placement lattice）

TRACKS → 给导线走线用（routing lattice）

```nginx
TRACKS X 190 DO 3158 STEP 380 LAYER metal1 ;
TRACKS X 190 DO 3158 STEP 380 LAYER metal1 ;
TRACKS Y 140 DO 2857 STEP 280 LAYER metal1 ;
TRACKS Y 140 DO 2857 STEP 280 LAYER metal1 ;
TRACKS X 190 DO 3158 STEP 380 LAYER metal2 ;
TRACKS X 190 DO 3158 STEP 380 LAYER metal2 ;
TRACKS Y 140 DO 2857 STEP 280 LAYER metal2 ;
...
```

```php-template
TRACKS <dir> <start> DO <num> STEP <pitch> LAYER <layerName> ;
```

TRACKS定义了芯片设计中布线的轨道信息, 包括轨道的方向、起始位置、重复模式以及所在的金属层等. 这些轨道信息对于后续的布线优化和设计验证非常重要, 因为它们决定了导线的走线方式和布局.

```nginx
TRACKS X 0 DO 5 STEP 80 LAYER M1 ;
```

```cpp
--------------------------------  y=320
--------------------------------  y=240
--------------------------------  y=160
--------------------------------  y=80
--------------------------------  y=0
```

可以注意到, TRACKS定义中包含了多个金属层的轨道信息, 即布线是分层进行的, 而cell的放置是平面的. 

**和 pitch 的关系**:

通常：
track pitch=metal pitch

其中：
metal pitch=wire width+spacing

比如：
width = 40nm, spacing = 40nm,
则 pitch = 80nm, TRACKS STEP 就是 80。

## GCELLGRID

GCELLGRID是： 全局布线阶段使用的 coarse partition 网格（routing bin / tile）

它的作用是把整个芯片区域离散成一个二维网格图，用于：

- 估计拥塞 (congestion)

- 进行 Steiner tree 近似

- 建立 routing graph

- 计算边容量与 demand

```php-template
GCELLGRID <dir> <start> DO <num> STEP <size> ;
```

```nginx
GCELLGRID X 0 DO 285 STEP 4200 ;
GCELLGRID Y 0 DO 190 STEP 4200 ;
```

也就是本质上2D芯片并不是按照track来离散的，而是按照一个更粗的网格来离散的. 这个网格每个格子是一个图的节点, 连接两个格子的边的容量就是这个格子之间的track数量. 这个网格的大小是设计者根据经验设置的, 一般来说越大越粗糙, 越小越精细. 一般来说是为了减小图的规模, 先在粗粒度上进行全局布线, 然后再在细粒度上进行详细布线.

## VIA

Via（过孔）是连接两层金属（或金属与扩散/栅）的垂直导通结构. 因为单个metal layer上的tracks通常只有一种方向, 
所以需要通过vias来实现不同层之间的连接. VIAS定义了芯片设计中vias的信息, 包括via的名称、所在层、尺寸、间距以及排列方式等. 这些信息对于后续的布线优化和设计验证非常重要, 因为它们决定了不同层之间的连接方式和布局. 

via 必须对齐到 track 交点, 满足 enclosure 规则.

```nginx
VIA VIA12
  LAYER M1 ;
    RECT 0 0 80 80 ;
  LAYER VIA12 ;
    RECT 20 20 60 60 ;
  LAYER M2 ;
    RECT 0 0 80 80 ;
END VIA12
```

| 层     | 作用    |
| ----- | ----- |
| 下金属   | 提供接触面 |
| cut 层 | 真正导通孔 |
| 上金属   | 连接上层  |


```nginx
VIAS 6 ;
    - via1_2_960_340_1_3_300_300 + VIARULE Via1Array-0 + CUTSIZE 140 140  + LAYERS metal1 via1 metal2  + CUTSPACING 160 160  + ENCLOSURE 70 100 70 70  + ROWCOL 1 3  ;
    - via2_3_960_340_1_3_320_320 + VIARULE Via2Array-0 + CUTSIZE 140 140  + LAYERS metal2 via2 metal3  + CUTSPACING 180 180  + ENCLOSURE 70 70 70 70  + ROWCOL 1 3  ;
    - via3_4_960_340_1_3_320_320 + VIARULE Via3Array-0 + CUTSIZE 140 140  + LAYERS metal3 via3 metal4  + CUTSPACING 180 180  + ENCLOSURE 70 70 90 70  + ROWCOL 1 3  ;
    - via4_5_960_2800_5_2_600_600 + VIARULE Via4Array-0 + CUTSIZE 280 280  + LAYERS metal4 via4 metal5  + CUTSPACING 320 320  + ENCLOSURE 40 0 0 0  + ROWCOL 5 2  ;
    - via5_6_960_2800_5_2_600_600 + VIARULE Via5Array-0 + CUTSIZE 280 280  + LAYERS metal5 via5 metal6  + CUTSPACING 320 320  + ENCLOSURE 0 0 0 0  + ROWCOL 5 2  ;
    - via6_7_960_2800_4_1_600_600 + VIARULE Via6Array-0 + CUTSIZE 280 280  + LAYERS metal6 via6 metal7  + CUTSPACING 320 320  + ENCLOSURE 0 0 260 360  + ROWCOL 4 1  ;
END VIAS
```

```nginx
- via1_2_960_340_1_3_300_300 
  + VIARULE Via1Array-0 
  + CUTSIZE 140 140  
  + LAYERS metal1 via1 metal2  
  + CUTSPACING 160 160  
  + ENCLOSURE 70 100 70 70  
  + ROWCOL 1 3  ;
```

### 规则解释

1️⃣ via1_2_960_340_1_3_300_300

这是 via 的实例名。命名通常编码：
```php-template
via<lower>_<upper>_<width>_<height>_<row>_<col>_<pitchX>_<pitchY>
```

例如：

- 1_2 → metal1 到 metal2

- 1_3 → 1 行 3 列

- 300_300 → 阵列 pitch

2️⃣ + VIARULE Via1Array-0

引用一个 LEF 中定义的 VIARULE。VIARULE 描述：

- 默认 enclosure

- 默认 cut 规则

- 默认 pitch

这里是在 DEF 中基于规则生成具体实例。

3️⃣ + CUTSIZE 140 140

每个 cut（单个 via 孔）的尺寸：

- width = 140
- height = 140


单位：DBU。

4️⃣ + LAYERS metal1 via1 metal2

表示三层结构：

| 层      | 作用    |
| ------ | ----- |
| metal1 | 下层金属  |
| via1   | cut 层 |
| metal2 | 上层金属  |

5️⃣ + CUTSPACING 160 160

多个 cut 之间的间距。

如果是 array：

[cut]--160--[cut]

6️⃣ + ENCLOSURE 70 100 70 70

这是关键。

语法：
```php-template
ENCLOSURE <lowerX> <lowerY> <upperX> <upperY>
```

表示：

下层 metal 对 cut 的包围尺寸

上层 metal 对 cut 的包围尺寸

举例：

70 100


表示：

左右各 70

上下各 100

不同层可以不同。

7️⃣ + ROWCOL 1 3

表示：

1 行 × 3 列


也就是 3 个 cut 并排。

示意：
```css
[■][■][■]
```

这是 multi-cut via，用于降低电阻。

### 几何尺寸计算示例

以第一条为例：

cut = 140

spacing = 160

3 列

总宽度：

$$
140\times 3+160\times 2=420+320=740
$$

再加 enclosure：

左右各 70：

$$
740+140=880
$$

这就是金属最小包围宽度。

五、看高层 via 的区别

例如：

- via4_5_960_2800_5_2_600_600
  + CUTSIZE 280 280
  + CUTSPACING 320 320
  + ROWCOL 5 2


特点：

cut 更大（280）

spacing 更大（320）

5 × 2 阵列

说明：

高层 metal 更厚，需要更大 via。

### ENCLOSURE 差异的物理意义

比如：
```nginx
ENCLOSURE 40 0 0 0
```

说明：

下层 metal 需要 40 enclosure

上层不需要

这通常表示：

上层是 thick metal

工艺规则 asymmetric

### 为什么有不同 via 定义的原因

原因：

1️⃣ 不同 metal pitch

M1~M3 pitch 小
M4 以上 pitch 大

2️⃣ 电流能力

power net 使用 multi-cut via

3️⃣ timing 优化

critical net 使用 larger via

### 多种 via 定义的设计流程意义

```markdown
工艺库（LEF）
 ├── 固定 VIA
 └── VIARULE（生成规则）

设计（DEF）
 └── 基于 VIARULE 生成具体 VIA 类型
       └── router 实际使用
```

## COMPONENT

COMPONENT 定义了芯片设计中的组件信息, 包括组件的名称、类型、位置、方向以及其他相关属性等. 这些信息对于后续的设计验证、布局优化和制造流程中非常重要, 因为它们决定了芯片设计中各个组件的放置方式和连接关系.

```nginx
- _105_ INV_X16_bottom + PLACED ( 700720 501200 ) N ;
- _108_ OR2_X4_bottom + PLACED ( 771780 397600 ) N ;
```

## PIN

这里的 PINS 不是 standard cell 内部 pin，
而是 芯片/block 边界上的物理 I/O 端口定义。

```markdown
- bp_fe_cmd_i[0]
  + NET bp_fe_cmd_i[0]
  + DIRECTION INPUT
  + USE SIGNAL
  + PORT
    + LAYER metal5 ( -140 -140 ) ( 140 140 )
    + PLACED ( 140 403340 ) N ;
```

| 值        | 含义 |
| -------- | -- |
| INPUT    | 输入 |
| OUTPUT   | 输出 |
| INOUT    | 双向 |
| FEEDTHRU | 穿越 |

| 类型     | 含义   |
| ------ | ---- |
| SIGNAL | 普通信号 |
| POWER  | 电源   |
| GROUND | 地    |
| CLOCK  | 时钟   |
| ANALOG | 模拟   |

### PORT 内部结构
```markdown
+ LAYER metal5 ( -140 -140 ) ( 140 140 )
```

表示：

在 metal5 层上定义一个矩形。

坐标：
```css
(-140, -140) 到 (140, 140)
```

注意：

这是 相对于 pin 原点的局部坐标。

尺寸：


280×280
```markdown
+ PLACED ( 140 403340 ) N
```
表示：

pin 原点放在：

(140, 403340)


方向为 N。

### 几何计算

绝对矩形范围：

局部：

(-140, -140) → (140, 140)


原点：

(140, 403340)


所以全局坐标：

(0, 403200) → (280, 403480)


即：

x: 0 ~ 280
y: 403200 ~ 403480

### 你给的几条差异

注意这两条：
```markdown
+ LAYER metal5
```

vs
```markdown
+ LAYER metal6
```

说明：

不同 bit 的 pin 被放在不同 metal 层。

这通常是：

为了缓解 routing congestion

或者是 top-level bump / pad 结构限制

## NET

| 场景             | 是否严格在 track  |
| -------------- | ------------ |
| 教科书模型          | 是            |
| 28nm 数字 SoC    | 基本是          |
| 7nm FinFET     | 高度受限，但仍可能有例外 |
| Analog routing | 完全不一定        |
| Special nets   | 不一定          |

```markdown
- N7 ( bp_fe_pc_gen_1_genblk1_branch_prediction_1__0893_ A ) ( bp_fe_pc_gen_1_genblk1_branch_prediction_1__0754_ A1 ) ( bp_fe_pc_gen_1_genblk1_branch_prediction_1__0688_ A1 ) ( bp_fe_pc_gen_1_genblk1_branch_prediction_1__0587_ B2 ) ( _111_ ZN ) + USE SIGNAL
      + ROUTED metal2 ( 756390 496020 ) ( * 499100 )
      NEW metal3 ( 749550 496020 ) ( 756390 * )
      NEW metal2 ( 749550 494340 ) ( * 496020 )
      NEW metal2 ( 749550 494340 ) ( 749930 * )
      NEW metal3 ( 755250 499100 ) ( 756390 * )
      NEW metal2 ( 761330 496020 ) ( * 496580 )
      NEW metal3 ( 756390 496020 ) ( 761330 * )
      NEW metal2 ( 755250 499940 ) ( * 501620 )
      NEW metal3 ( 752210 501620 ) ( 755250 * )
      NEW metal2 ( 752210 499940 ) ( * 501620 )
      NEW metal2 ( 755250 499100 ) ( * 499940 )
      NEW metal1 ( 756390 499100 ) via1_4
      NEW metal2 ( 756390 496020 ) via2_5
      NEW metal2 ( 749550 496020 ) via2_5
      NEW metal1 ( 749930 494340 ) via1_4
      NEW metal2 ( 755250 499100 ) via2_5
      NEW metal2 ( 756390 499100 ) via2_5
      NEW metal1 ( 761330 496580 ) via1_4
      NEW metal2 ( 761330 496020 ) via2_5
      NEW metal1 ( 755250 499940 ) via1_4
      NEW metal2 ( 755250 501620 ) via2_5
      NEW metal2 ( 752210 501620 ) via2_5
      NEW metal1 ( 752210 499940 ) via1_4 ;
```