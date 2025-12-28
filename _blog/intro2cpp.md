---
title: "Intro to C++"
collection: blog
type: "blog"
date: 2025-12-28
excerpt: '基本的C++介绍'
location: "Shanghai, China"
---

Tech Talk at 2026 Winter Hackathon - Introduction to C++

## Introduction to C++

这一部分可以学习师兄写过的[C++简介](https://xiangli.cyou/posts/2024/12/cpp-intro.html)文章.

## Compilation and Execution Process of C++

>Note:
>这一部分不是这次Tech Talk的重点内容, 一般来说OJ题目是单个源文件提交, 不涉及多文件编译和链接过程. 但是了解C++的编译和执行流程对于理解程序的运行机制, 以及调试和优化都有很大帮助.

---

C++是一种代表性的编译型语言. 编译型语言的特点是代码在运行前需要经过编译器编译成机器码, 然后直接由操作系统执行, 而非像解释型语言那样逐行由解释器执行. 这种方式通常能带来更高的执行效率, 因为编译器可以在编译阶段进行各种优化. **学习编程语言本质上是在了解它的编译规则**.

一个C++程序从编写到执行一共有以下几个主要步骤:
1. **编写源代码**: 使用文本编辑器编写C++源代码, 文件通常以`.cpp`为后缀. 此时代码还是纯粹的文本文件.
2. **预处理**: 使用预处理器处理源代码中的预处理指令, 例如`#include`和`#define`. 预处理器会将这些指令展开, 生成一个纯净的文本源代码文件.
3. **编译**: 编译器读取预处理后的源代码, 通过词法分析, 语义分析, 优化等步骤, 将其转换为中间代码或汇编代码. 此时, 编译器会检查代码的语法和类型是否正确. 这一步编译器会生成一个目标文件, 通常以`.o`为后缀, 此时它已经不是文本文件了, 更像是机器码的二进制文件.
4. **链接**: 如果程序由多个源文件组成, 每个源文件都已经被编译成目标文件, 链接器会将这些目标文件连接到一起. 如果它们还依赖于已经编译好的二进制库, 链接器也会将这些库文件链接进来. 最终生成一个可执行文件. 在Windows上通常以`.exe`为后缀, 在Linux或macOS上通常没有特定后缀.
5. **执行**: 操作系统加载可执行文件到内存中, 并开始执行程序的入口点, 对于C++程序来说是`main`函数.

接下来我们用一个简单的blas调用例子来展示C++代码的编写和执行过程. 它将会包含上面所有流程的步骤.

```cpp
// blas_test.cpp
#include <iostream>
#include <cblas.h>
#include <cstdio>


int main() {
    const int N = 5;
    float *A = new float[N * N];
    float *B = new float[N * N];
    float *C = new float[N * N];

    // Initialize matrices A and B
    for (int i = 0; i < N * N; ++i) {
        A[i] = static_cast<float>(i) / 10.;
        B[i] = static_cast<float>(i) / 10.;
        C[i] = 0.0f;
    }

    // Perform matrix multiplication C = A * B
    cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                N, N, N,
                1.0f,
                A, N,
                B, N,
                0.0f,
                C, N);

    std::cout << "Result matrix C:" << std::endl;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            printf("%2.2f ", C[i * N + j]);
        }
        std::cout << std::endl;
    }

    delete[] A;
    delete[] B;
    delete[] C;

    return 0;
}
```

```cpp
// util.h
#ifndef UTIL_H
#define UTIL_H
#include <string>
void foo(const std::string&);
#endif // UTIL_H
```

```cpp
// util.cpp
#include <string>
#include <iostream>
void foo(const std::string& str) {
    // Do nothing
    std::cout << "You called foo with: " << str << std::endl;
}
```

编译
```bash
# Compile util.cpp to util.o
g++ -c util.cpp -o util.o -I/path/to/include
# Compile blas_test.cpp to blas_test.o
g++ -c blas_test.cpp -o blas_test.o -I/path/to/include
# Link object files with OpenBLAS library to create executable
g++ blas_test.o util.o -o blas_test -lopenblas -L/path/to/lib
# Run the executable
./blas_test
```

```text
You called foo with: Testing BLAS SGEMM function
Result matrix C:
1.50 1.60 1.70 1.80 1.90 
4.00 4.35 4.70 5.05 5.40 
6.50 7.10 7.70 8.30 8.90 
9.00 9.85 10.70 11.55 12.40 
11.50 12.60 13.70 14.80 15.90
```

### 预处理

这一步主要处理`#include`和`#define`等预处理指令. 例如, `#include <iostream>`会被展开为iostream头文件的内容, 这样编译器在后续阶段就能看到完整的代码定义. 预处理器还会处理宏定义, 条件编译等指令. 这也就是为什么g++命令中没有把`.h`文件作为输入文件的原因. 这一步通常是隐式完成的, 不需要单独调用预处理器. 如果你的 `.h`文件不在标准路径下, 你可以使用 `-I` 选项指定头文件搜索路径.

### 编译

C++为了模块化编程和编译, 它允许将代码拆分成多个源文件. 每个源文件可以单独编译成目标文件. 例如, 上面的例子中, `util.cpp` 和 `blas_test.cpp` 分别被编译成 `util.o` 和 `blas_test.o`. 编译器会检查每个源文件的语法和类型是否正确, 并生成对应的目标文件. 这一步使用 `-c` 选项告诉g++只进行编译, 不进行链接.

这个目标文件是机器码的二进制文件, 不能直接阅读. 它包含了编译器生成的机器指令, 以及一些符号表和调试信息等. 除此之外, 如果源文件中引用了其他模块的函数或变量, 这些引用在目标文件中会以未定义符号的形式存在, 等待链接器在链接阶段解析. 

例如, `blas_test.o` 中对 `foo` 函数的调用在编译时并不知道 `foo` 的具体实现, 因此在目标文件中会有一个未定义符号 `foo`, 链接器会在链接阶段找到 `util.o` 中的 `foo` 实现并将其链接进来. 这里核心的机制在于函数调用只需要知道函数的签名(返回值类型, 参数类型).

通常这些签名都会放在头文件中, 这样就非常方便多个源文件之间的引用和调用.

### 链接

链接器的任务是将多个目标文件和库文件连接成一个完整的可执行文件. 它会解析目标文件中的未定义符号, 并将它们与其他目标文件或库文件中的定义进行匹配. 例如, `blas_test.o` 中对 `foo` 函数的调用会被链接器解析为 `util.o` 中的 `foo` 实现. 链接器还会处理库文件的引用, 例如上面的例子中使用了OpenBLAS库进行矩阵乘法运算. 链接器会将OpenBLAS库中的相关函数链接进来, 使得最终的可执行文件能够调用这些库函数. 本质上库文件也是一种特殊的目标文件, 它们通常以`.a`或`.so`为后缀(静态库和动态库). 这里使用 `-lopenblas` 选项告诉链接器链接OpenBLAS库, 即告诉连接器遇到目标文件中查询不到的符号时去哪些库中查找.

如果库文件不在标准路径下, 你可以使用 `-L` 选项指定库文件搜索路径.

### 执行

执行阶段是操作系统加载可执行文件到内存中, 并开始执行程序的入口点, 对于C++程序来说是`main`函数. 操作系统会为程序分配内存空间, 设置堆栈等运行环境, 然后跳转到`main`函数开始执行程序逻辑. 在这个阶段, 程序已经完全转换为机器码, 可以直接由CPU执行.

需要注意的是, 尽管程序入口是`main`函数, 但在实际执行过程中, 操作系统会先执行一些初始化代码, 例如设置C++运行时环境, 初始化全局变量等, 然后才跳转到`main`函数. 程序执行完毕后, 操作系统还会执行一些清理工作, 例如释放内存, 关闭文件等.

## 总结

几乎所有编译型语言都遵循类似的编译和执行流程, 只是具体的实现细节可能有所不同. 了解这个流程有助于我们更好地理解程序的运行机制, 以及如何进行调试和优化.