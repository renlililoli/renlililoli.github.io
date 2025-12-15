---
title: "Sobolev imbedding and interpolation inequalities."
collection: blog
type: "blog"
date: 2025-12-13
excerpt: 'An overview of Sobolev imbedding and interpolation inequalities and their applications.'
location: "Shanghai, China"
---

索伯这块内容确实又繁琐又多, 所以这里妄图梳理一个快速查询的笔记.

## Marcinkiewicz插值定理

这是一个非常强大的插值定理, 允许我们通过弱型不等式来得到强型不等式. 这里放出定理的陈述和证明. 便于后续使用.

![marcinkiewicz1](/blog/pictures/sobolev/m1.png)

![marcinkiewicz2](/blog/pictures/sobolev/m2.png)

![marcinkiewicz3](/blog/pictures/sobolev/m3.png)

![marcinkiewicz4](/blog/pictures/sobolev/m4.png)

![marcinkiewicz5](/blog/pictures/sobolev/m5.png)

![marcinkiewicz6](/blog/pictures/sobolev/m6.png)

![marcinkiewicz7](/blog/pictures/sobolev/m7.png)

![marcinkiewicz8](/blog/pictures/sobolev/m8.png)

## Sobolev imbedding

首先, 空间的嵌入定理, 主要按照函数空间的奇性来划分. 由于是积分范数, 所以n维空间的积分可以提供$x^{n/p}$, 而求导数会损失$x^m$的奇性,
所以对于 $m,p$ 的Sobolev空间$W^{m,p}$, 其容纳的奇性大概为 $x^{n/p - m}$. 所以分类的临界值为 $mp = n$. $mp>n$ 时, 函数比较光滑, 可以嵌入到连续函数空间中; $mp<n$ 时只能嵌入普通的$L_q$空间. 具体不等式如下:

![imbedding1](/blog/pictures/sobolev/imbedding1.png)

![imbedding2](/blog/pictures/sobolev/imbedding2.png)

![imbedding3](/blog/pictures/sobolev/imbedding3.png)

![imbedding4](/blog/pictures/sobolev/imbedding4.png)

除了部分边界情况以及需要区域有lipshitz条件的第二个part, 其余证明利用了区域的cone condition, 然后使用cone上的积分平均值来控制函数值. 积分平均值来自于potential估计.

核心的不等式为

![potential1](/blog/pictures/sobolev/potential1.png)

![potential2](/blog/pictures/sobolev/potential2.png)

这个不等式来源为带积分余项的泰勒展开, 将函数值用导数展开后在cone上积分. 最终得到的结果类似于

$$
|u(x)| \le K \sum_{|\alpha| \le m-1} r^{|\alpha|-n} \chi_r * |D^\alpha u| (x) + K \sum_{|\alpha| = m}\chi_r \omega_{m} * |D^\alpha u| (x).
$$

对于$mp>n$, $p>1$的情况

$$
\chi_r * |D^\alpha u| (x) \le \|D^\alpha u\|_{p} r^{n/p'}.
$$

$$
\chi_r \omega_{m} * |D^\alpha u| (x) \le \|D^\alpha u\|_{p} \left(\int_{B(0,r)} x^{(m-n)p'} dx\right)^{1/p'}
$$

而$p=1$, $m=n$, $\omega_m = 1$, 不等式恰好是自然成立的.

对于k维超曲面的trace估计, 则是直接将上面的不等式的p次方在超曲面上积分即可, 然后用Holder的插值不等式进行估计即可.

对于$mp<n, p>1$的情况, 首先固定$r=1$, 由于 $\chi_r * |D^\alpha u| (x) \le \chi_r \omega_m * |D^\alpha u| (x)$, 所以只需要考虑后一项.

利用插值不等式, $p\le q \le p^* = \frac{kp}{n-mp}$, 则有
$$
\|u\|_{q, H} \le \|u\|_{p^*, H}^\theta \|u\|_{p, H}^{1-\theta} \\ \le K (\sum_{|\alpha|\le m} \|\chi_1 \omega_m * |D^\alpha u| (x)\|_{p^*,H})^{\theta} \\(\sum_{|\alpha|\le m} \|\chi_1 \omega_m * |D^\alpha u| (x)\|_{p,H})^{1-\theta}.
$$

也就是只需要证明$q=p$和$q=p^*$的边界情况. 核心的估计为对于$v \in L^p$, 有

$$
\|\chi_r \omega_m * v\|_{p,H} \le K r^{m - \frac{n-k}{p}}\|v\|_{p}, \quad \|\chi_r \omega_m * v\|_{p^*,H} \le K \|v\|_{p}.
$$

这两个不等式中的系数可以直接算出来. 第一个中, 左侧贡献 $m-k/p$, 右侧贡献 $n/p$, 所以出现一个 $m - \frac{n-k}{p}$.

第二个中, 左侧贡献 $m - \frac{k}{p^*} = \frac{n}{p}$

它们分别是直接进行估计和使用 Marcinkiewicz插值定理得到的. 这个插值定理非常强大的地方在于, 它允许我们只需要证明两个端点的弱型不等式, 就可以得到开区间的强型不等式. 如果弱不等式在某个区间上成立, 那么中间的强不等式也成立.

![mpn1](/blog/pictures/sobolev/mpn1.png)

![mpn2](/blog/pictures/sobolev/mpn2.png)

![mpn3](/blog/pictures/sobolev/mpn3.png)

![mpn4](/blog/pictures/sobolev/mpn4.png)

![mpn5](/blog/pictures/sobolev/mpn5.png)

$mp=n, p>1$的情况, 同样的考虑插值. 我们希望证明 $p\le q < \infty$ 的情况.

$$
\|\chi_1 \omega_m * v\|_{q,H} \le K \|v\|_{p}.
$$

选择 $1 < p_1 < p < p_2$, 由于 $n-mp_1 < k$, 因此有

$$
\|\chi_1 \omega_m * v\|_{p_1,H} \le K \|v\|_{p_1}.
$$

同时 $mp_2 > n$, 因此有

$$
\|\chi_1 \omega_m * v\|_{\infty,H} \le K \|v\|_{p_2}.
$$

因此如果

$$
\frac{1}{q} = \frac{\theta}{p_1} + \frac{1-\theta}{\infty} = \frac{\theta}{p_1}, (q<\infty \text{\;since\;} \theta>0)\\
\frac{1}{p} = \frac{\theta}{p_1} + \frac{1-\theta}{p_2} = \frac{1}{q} + \frac{1-\theta}{p_2} > \frac{1}{q},
$$

要证明的不等式就会成立. 而只要$p\le q < \infty$, 就总能找到合适的$p_1, p_2$使得上面的等式成立. 而$q=\infty$的情况则不成立. $p=q$的情况对应于$p_2 = \infty$, 对应也成立.

只剩下$p=1, mp<n$, 此时可以直接进行证明, 它的证明思路与索伯列夫不等式类似, 通过向量值holder不等式进行估计.

$p=1, n-mp < k \le n$, 则要证明 $W^{m,1} \to L^{\frac{k}{n-m}}(H)$. 但是 $W^{m,1} \to W^{m-1, p}$, $1\le p \le \frac{n}{n-1}$.

但是此时有 $k \ge n-m+1 > n - (m-1)p$, if $p>1$. 因此可以使用之前的结论, 有它可以嵌入 $L^{q}(H)$, $1 \le q \le \frac{kp}{n-(m-1)p} = \frac{k}{n-m}$.

最后的情况就是 $p=1, k=n-m$. 要证明 $W^{m,1} \to L^{1}(H)$. 用方块覆盖, 每个方块的前m维数用局部估计, 余下的维数积分恰好是k维的积分, 这样就可以得到结果.


剩余的就是嵌入到Holder空间的情况. 它的证明用到的技巧是Morrey不等式. 注意这时需要区域满足强lipschitz条件, 如区域是两个拼起来的方形, 中间不连接, 那么是不能嵌入这样的空间的.

![morrey](/blog/pictures/sobolev/morrey.png)

同样的, 指标也可以通过量纲计算. 比如 $mp > n >(m-1)p$, 那么有

$$
0 < \alpha = m - \frac{n}{p} < 1.
$$

$\alpha$ 就是对应的Holder空间的指数. 当 $p>1$, $n=(m-1)p$ 时, $\alpha = 1$, 则恰好不能嵌入到Lipschitz空间中. $p=1$ 时是可以的.

到目前为止, 有几个重要的不能进行嵌入的边界情况

$$
mp = n, p> 1,\quad  W^{m,p} \to L^\infty
$$

$$
mp > n > (m-1)p, p> 1, \quad W^{m,p} \to C^{0, \alpha}, \alpha > m - \frac{n}{p}
$$

$$
n = (m-1)p, p>1, \quad W^{m,p} \to C^{0,1}
$$

$$
mp < n, p > 1, \quad W^{m,p} \to L^{q},\quad  q > p^* = \frac{kp}{n-mp}
$$

前两个反例用单项式即可, 后两个用双对数函数.

还有一个有趣的例子, 即用半范数控制范数, 即

![semi1](/blog/pictures/sobolev/sobolev.png)

它只在临界情形成立. 因为回忆其它情形都是用到了插值.

## 插值定理

这里的插值定理是, 是否能用最高阶半范数和Lp范数来控制中间阶的半范数. 具体的定理如下:

![interpolation1](/blog/pictures/sobolev/inter1.png)

证明思路来自于从1维出发, 然后高维用方向导数推广, 最后用归纳法推广到任意阶导数.

![interpolation2](/blog/pictures/sobolev/inter2.png)

![interpolation3](/blog/pictures/sobolev/inter3.png)

![interpolation4](/blog/pictures/sobolev/inter4.png)

![interpolation5](/blog/pictures/sobolev/inter5.png)

![interpolation6](/blog/pictures/sobolev/inter6.png)

最后一个结果使用了Young不等式, 然后再用前面的插值.

## 紧嵌入

这里只放2个反例

![compact1](/blog/pictures/sobolev/compact1.png)

![compact2](/blog/pictures/sobolev/compact2.png)

![compact3](/blog/pictures/sobolev/compact3.png)

![compact4](/blog/pictures/sobolev/compact4.png)

![compact5](/blog/pictures/sobolev/compact5.png)

