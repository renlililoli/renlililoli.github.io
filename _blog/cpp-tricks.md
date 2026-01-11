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

| 项目    | 名称                              | 标准含义        | 关键约束              | 是否允许 |
| ----- | ------------------------------- | ----------- | ----------------- | ---- |
| 主模板   | Primary template                | 模板族的基准定义    | 只能引入模板参数，不能施加结构约束 | ✔    |
| 全特化   | Explicit specialization         | 针对具体实参的完全定义 | 必须匹配主模板参数数目       | ✔    |
| 偏特化   | Partial specialization          | 针对参数子集的模式匹配 | 只能用于类模板           | ✔    |
| 函数偏特化 | Function partial specialization | 函数模板的偏特化    | 标准禁止              | ❌    |
| 模板族   | Template family                 | 同名模板与其特化的集合 | 名字 + 作用域必须一致      | ✔    |


| 项目      | 函数模板 | 类模板 |
| ------- | ---- | --- |
| 有调用语境   | ✔    | ❌   |
| 有参数推导   | ✔    | ❌   |
| 有重载决议   | ✔    | ❌   |
| 需要偏特化   | ❌    | ✔   |
| 标准允许偏特化 | ❌    | ✔   |

对于类模板而言：

只有**主模板（primary template）**在声明 / 定义时写成 template<...> class Name，类名后面不写 <…>；

所有偏特化和全特化在声明 / 定义时，都必须在类名后显式写出 <…> 实参形式。

类模板特化实例化时, 参数数量必须和主模板一致.

```cpp
#include <iostream>
#include <utility>
#include <vector>
#include <array>

template <typename T1, typename T2>
class test {};

template <typename T1>
class test<T1, int> {
    public:
    test() {
        std::cout << "Specialized template instantiated with int as second type." << std::endl;
    }
};

template <template <typename> class T1, typename T2, typename T3>
class test<T1<T2>, T3> {
    public:
    test() {
        std::cout << "Generic template instantiated with a template class as first type." << std::endl;
    }
};

template <typename T1, typename T2>
class test<std::array<T1, 5>, T2> {
    public:
    test() {
        std::cout << "Specialized template instantiated with std::array of size 5 as first type." << std::endl;
    }
};

int main() {
    test<int, double> defaultInstance; // This will use the primary template
    test<double, int> specializedInstance; // This will trigger the specialized template
    test<std::vector<int>, double> genericInstance; // This will use the generic template
    // test<std::vector, int, int> anotherGenericInstance; // 类模板 "test" 的参数太多
    test<std::array<float, 5>, char> arraySpecializedInstance; // This will trigger the array specialization
    test<float, float> anotherDefaultInstance; // This will use the primary template, will not trigger test<std::array<T1, 5>, T2>
    // test<int>; // wrong number of template arguments

    return 0;
}
```

### 模板惰性实例化

#### 1️⃣ 模板实例化时机

类模板本身不会立即生成代码，只是编译器知道有一个模板定义。

成员函数模板（或者类模板的成员函数）也不会立即生成代码。

只有当你真正调用这个函数，编译器才会实例化模板：

也就是把模板参数替换成实际类型，然后生成对应的函数代码

理解起来也是容易的, 因为我们知道成员函数是可以单独定义的, 比如`mystruct::func()` , 这个函数的定义可以在类外部, 所以编译器不可能在类定义时就生成所有成员函数的代码.  

#### 例子

```cpp
template<typename T>
struct MyAllocator {
    T* allocate(size_t n) { ... }
    void deallocate(T* p, size_t n) { ... }

    // 构造对象
    template<typename U, typename... Args>
    void construct(U* p, Args&&... args) {
        ::new (static_cast<void*>(p)) U(std::forward<Args>(args)...);
    }
};
```

一部分模板参数在类模板定义时就确定了, 另一部分模板参数在成员函数调用时才确定. 它允许这样的调用:

```cpp
MyAllocator<int> alloc;
alignas(int) char buffer[sizeof(int)];

// 构造 int
alloc.construct(reinterpret_cast<int*>(buffer), 42);

// 构造 int 的派生类
struct MyInt : int { MyInt(int x): int(x){} };
alloc.construct(reinterpret_cast<MyInt*>(buffer), 123);
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

>关键点: 引用本身不拷贝，但是 STL 容器要存储自己的元素副本，所以传左值引用时必须拷贝。右值引用 + move 是 STL 提供的 唯一“安全窃取资源”的方式”，避免额外拷贝

也就是说stl容器在插入元素时, 如果传入的是左值引用, 它会拷贝该对象到自己的存储空间中; 如果传入的是右值引用并使用 `std::move`, 它会“窃取”该对象的资源, 避免拷贝开销. 当然可以自己定义传入左值引用时不拷贝, 直接存储指针或者引用的容器, 但这样做会带来生命周期管理的问题, 容器中的对象可能会变成悬空指针. 为了安全起见, STL 容器默认会拷贝左值引用.


| 方式                  | 拷贝？ | 移动？ | 容器安全？ | 典型场景                    |
| ------------------- | --- | --- | ----- | ----------------------- |
| `const T&`          | 否   | 否   | 高     | 只读访问、传参数                |
| `T&`                | 否   | 否   | 高     | 修改外部对象                  |
| `T&&` + `std::move` | 否   | 是   | 高     | 临时对象或可移动对象传入容器、函数“窃取”资源 |
| 左值引用传给容器            | 是   | 否   | 高     | 外部对象不能被窃取，容器拷贝安全        |


## [[attribute]] 语法

C++11 引入了属性语法 `[[attribute]]`, 用于向编译器提供额外的信息或指令. 这些属性可以影响编译器的行为, 优化代码生成, 或者提供警告信息. 常见的属性包括:
- `[[nodiscard]]`: 指示函数的返回值不应被忽略.
- `[[maybe_unused]]`: 指示变量或函数可能未被使用, 避免编译器警告.
- `[[deprecated]]`: 标记某个实体已过时, 使用时会产生警告.
- `[[fallthrough]]`: 指示 switch 语句中的 case 语句故意落空, 避免警告.
- `[[noreturn]]`: 指示函数不会返回, 例如抛出异常或终止程序.

## 智能指针

updating...