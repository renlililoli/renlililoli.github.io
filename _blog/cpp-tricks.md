---
title: "Cpp Tricks"
collection: blog
type: "blog"
date: 2026-01-09
excerpt: 'A collection of useful C++ tricks and tips for developers.'
location: "Shanghai, China"
---

主要是一些 C++ 语言的高级特性和技巧.

## template 元编程

看到了一些好玩的特性和语法

首先template是一种编译器匹配函数的机制, 本质上就是带参数的函数重载.

template 有几种参数类型, 分别是
- `typename` 或 `class` , 用于表示类型参数
- 非类型参数, 用于表示值参数, 例如 `int N`
- `concept` , 用于表示类型约束, C++20 引入

### 模板匹配机制

模板匹配的过程类似于函数重载解析, 编译器会根据传入的模板参数类型和数量来选择最合适的模板实例化. 具体规则包括:
- 精确匹配优先于模糊匹配
- 特化模板优先于通用模板

注意的是所有模板声明的参数数量必须相同, 比如只允许
```cpp
template<typename T, typename U>
class MyClass {};

template<typename T>
class MyClass<T, int> {}; // 合法, 特化版本

template<typename T>
class MyClass<T> {}; // 非法, 参数数量不匹配
```

`template<...>`只是一个模板参数声明, 表明哪些是可变的, 而具体匹配是发生在后面的函数或者类定义上.

```cpp

template<typename A, typename B>
class wrapper {};

template<typename T, typename U>
class test {};

template<typename T, typename A, typename B>
class test<wrapper<A, B>, T> {}; // 合法, 参数数量匹配
```

### 可变参数模板

可变参数模板允许我们定义接受任意数量参数的模板. 语法是使用 `...` 来表示参数包. 例如:
```cpp
template<typename... Args>
void func(Args... args) {
    // 可以使用 sizeof...(Args) 获取参数数量, 编译期计算
    std::cout << "Number of arguments: " << sizeof...(Args) << std::endl;
}

func(1, 2.5, "hello"); // 输出: Number of arguments: 3

template<int... Ns>
struct Sum {
    static constexpr int value = (Ns + ... + 0); // 折叠表达式
};

Sum<1, 2, 3, 4, 5>::value; // 15 compile time computed
```

一个pack在匹配上被视作一个整体.

### SFINAE

SFINAE (Substitution Failure Is Not An Error) 是 C++ 模板编程中的一个重要概念. 它允许我们在模板实例化过程中, 如果某个模板参数的替换失败, 编译器不会报错, 而是会尝试其他重载或特化. 例如:
```cpp
template<typename T>
auto func(T t) -> decltype(t.size(), void()) { // 如果 T 有 size
    std::cout << "T has size: " << t.size() << std::endl;
}

template<typename T>
void func(T t) { // 其他情况
    std::cout << "T has no size" << std::endl;
}
```

这个技巧也被用来实现类型特征 (type traits) 和条件编译.

```cpp
template<bool B, typename T = void>
struct enable_if {};

template<typename T>
struct enable_if<true, T> { using type = T; };


template<typename T>
typename enable_if<std::is_integral<T>::value, T>::type
foo(T t) {
    // 仅当 T 是整数类型时才启用
    return t;
}
```

### constexpr if

`constexpr if` 是 C++17 引入的一个特性, 允许我们在编译期根据条件选择代码路径. 例如:
```cpp
template<typename T>
void func(T t) {
    if constexpr (std::is_integral<T>::value) {
        std::cout << "T is an integral type" << std::endl;
    } else {
        std::cout << "T is not an integral type" << std::endl;
    }
}
```

### 概念 (Concepts)

C++20 引入了概念 (Concepts), 用于对模板参数进行约束. 这使得模板代码更具可读性和可维护性. 例如:
```cpp
template<typename T>
concept Integral = std::is_integral<T>::value;

template<Integral T>
T add(T a, T b) {
    return a + b;
}
```

概念是一个编译期可求的bool值, 可以用来限制模板参数的类型. 如果不满足概念约束, 编译器会给出更清晰的错误信息. 本质上模板会被约束条件替代, 不满足条件的模板实例化会被忽略.

### requires 子句

`requires` 子句是 C++20 引入的另一个特性, 用于在模板定义中指定约束条件. 例如:
```cpp
template<typename T>
requires std::is_integral<T>::value
T multiply(T a, T b) {
    return a * b;
}
```

不满足 `requires` 条件的模板实例化会被忽略, 类似于 SFINAE 的行为.

requires 表达式:
```cpp
requires (parameter_list) { requirement_seq }
```

- parameter_list：可选，用来声明临时变量类型（通常是模板参数实例）

- requirement_seq：大括号里写“要求”，每一条都是一个 requirement

- 作用：在编译期检查类型是否满足某些操作或特性

- 返回值：布尔值（编译期可判断 true/false）

| 类型                         | 语法                                       | 说明                 |
| -------------------------- | ---------------------------------------- | ------------------ |
| **expression requirement** | `{ expr }` 或 `{ expr } -> concept`       | 检查表达式是否可用，并可约束返回类型 |
| **type requirement**       | `typename name` 或 `typename name = type` | 检查类型是否存在或是否有效      |
| **nested requirement**     | `requires concept<T>`                    | 嵌套调用 concept 来检查类型 |

```cpp
// matrix concept

template<typename T>
concept DMatrix = requires(T a, size_t i, size_t j) {
    { a(i, j) } -> std::convertible_to<double>; // 支持 () 操作符, 返回 double
    { a.rows() } -> std::convertible_to<size_t>; // 有 rows() 方法
    { a.cols() } -> std::convertible_to<size_t>; // 有 cols() 方法
};

template<DMatrix Mat>
void printMatrixInfo(const Mat& m) {
    std::cout << "Matrix size: " << m.rows() << " x " << m.cols() << std::endl;
}

```

### 模板变量模板

变量模板允许我们定义模板化的变量, 语法类似于函数模板. 例如:
```cpp
template<typename T>
constexpr T pi = T(3.1415926535897932385);
double myPi = pi<double>; // 3.141592653589793
float myPiF = pi<float>;   // 3.1415927f
```

### CRTP (Curiously Recurring Template Pattern)

CRTP 是一种模板编程技巧, 告诉编译器在基类中使用派生类作为模板参数. 例如:
```cpp
template<typename Derived>
class Base {
public:
    void interface() {
        static_cast<Derived*>(this)->implementation();
    }
};

class Derived : public Base<Derived> {
public:
    void implementation() {
        std::cout << "Derived implementation" << std::endl;
    }
};
```

这个技巧使得编译期多态成为可能, 提高了运行时性能.

### decltype(auto)

int x = 5;
int& r = x;

auto a = r;         // a 是 int（引用消失）
decltype(auto) b = r; // b 是 int&（保留引用）

### 模板模板参数

模板模板参数允许我们将模板作为参数传递给另一个模板. 例如:
```cpp
template<template<typename> class Container, typename T>
class Wrapper {
public:
    Container<T> data;
};

Wrapper<std::vector, int> intVecWrapper; // 使用 std::vector 作为容器
```

### 模板别名(using)

模板别名允许我们为复杂的模板类型定义简短的别名. 例如:
```cpp
template<typename T>
using Vec = std::vector<T>;
Vec<int> intVec; // 等同于 std::vector<int>
```



### 总结

以上所有的一切都是编译期特性.

## 左值右值

C++ 引入了左值 (lvalue) 和右值 (rvalue) 的概念, 用于区分不同类型的表达式. 了解它们对于理解引用折叠和完美转发非常重要.

- 左值 (lvalue): 表示有持久存储地址的对象, 可以出现在赋值语句的左侧. 例如变量名, 数组元素等.
- 右值 (rvalue): 表示临时对象或字面值, 通常不能出现在赋值语句的左侧. 例如字面值, 临时对象等.
- xvalue (expiring value): 一种特殊的右值, 表示即将被销毁的对象, 通常与移动语义相关.

鉴别就是能否取地址 & , 能取地址的是左值, 不能取地址的是右值.


两个重要的函数:
- forward<T>(u): 根据 T 的类型特性完美转发 u, 保留其左值或右值属性.
- move(u): 将 u 转换为右值引用, 表示 u 的资源可以被移动.

由于引用折叠规则, 当我们使用模板参数 T 来声明引用时, 需要特别注意:
- `T& &` 会折叠为 `T&`
- `T& &&` 会折叠为 `T&`
- `T&& &` 会折叠为 `T&`
- `T&& &&` 会折叠为 `T&&`

经历过一次传参, 右值引用就变成了左值. 所以对性能敏感的代码, 一般会使用 `std::forward<T>(arg)` 来完美转发参数, 避免产生拷贝.

对于move来说, 它总是将参数转换为右值引用, 以便触发移动语义. 被移动后的对象通常处于一种有效但未定义的状态, 只能被赋值或销毁.

```cpp

void f(int& x)  { std::cout << "lvalue\n"; }
void f(int&& x) { std::cout << "rvalue\n"; }

template<typename T>
void wrapper(T&& arg) {
    f(std::forward<T>(arg)); // 完美转发
}

template<typename T>
void wrapper_no_forward(T&& arg) {
    f(arg); // 未使用std::forward，始终作为左值处理
}

int main() {
    int a = 10;
    wrapper(a);          // 传递左值
    wrapper(20);        // 传递右值
    wrapper_no_forward(a); // 传递左值
    wrapper_no_forward(20); // 传递右值
    return 0;
}

```

```bash
lvalue
rvalue
lvalue
lvalue
```