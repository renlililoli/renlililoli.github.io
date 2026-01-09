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
