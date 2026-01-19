---
title: "实现一个简单的 eval 函数"
collection: blog
type: "blog"
date: 2026-01-19
excerpt: '在本文中，我们将探讨如何实现一个简单的 eval 函数，能够解析并计算基本的数学表达式。我们将使用抽象语法树（AST）来表示表达式，并通过递归下降解析器来构建 AST。最后，我们将实现一个评估函数来计算表达式的值。'
location: "Shanghai, China"
---

最近在刷 leetcode, 遇到一个经典题目

```
给你一个字符串表达式 s ，请你实现一个基本计算器来计算并返回它的值。

注意:不允许使用任何将字符串作为数学表达式计算的内置函数，比如 eval() 。
```

经典的做法就是双栈, 一个存数字, 一个存运算符. 这里除了双栈, 再给一个递归的做法

```cpp
// Tokenize the input string
int calculate(string s) {
        

        vector<string> tokens;
        
        // Preprocess the string to handle spaces and unary operators
        for (Lint i = 0; i < s.size(); i++) {
            if (s[i] == ' ') continue;

            if (isdigit(s[i])) {
                string num;
                while (i < s.size() && isdigit(s[i])) {
                    num += s[i++];
                }
                tokens.push_back(num);
                i--; // Adjust for the outer loop increment
            } else if (s[i] == '+' || s[i] == '-') {
                // Handle unary operators
                if (i == 0 || s[i - 1] == '(' || s[i - 1] == '+' || s[i - 1] == '-') {
                    tokens.push_back("0"); // Insert a zero for unary operator
                }
                tokens.push_back(string(1, s[i]));
            } else if (s[i] == '(' || s[i] == ')') {
                tokens.push_back(string(1, s[i]));
            }
        }

        Lint index = 0;
        return calculateHelper(tokens, index);

    }
// Recursive function to evaluate the expression
Lint calculateHelper(const vector<string>& tokens, Lint& index) {
        stack<Lint> stk;
        Lint num = 0;
        char sign = '+';

        while (index < tokens.size()) {
            string token = tokens[index];
            index++;

            if (isdigit(token[0])) {
                num = stoi(token);
            }

            if (token == "(") {
                num = calculateHelper(tokens, index);
            }

            if (!isdigit(token[0]) || index >= tokens.size()) {
                if (sign == '+') {
                    stk.push(num);
                } else if (sign == '-') {
                    stk.push(-num);
                }
                sign = token[0];
                num = 0;
            }

            if (token == ")") {
                break;
            }
        }

        Lint result = 0;
        while (!stk.empty()) {
            result += stk.top();
            stk.pop();
        }
        return result;
    }
```


那么再来看看怎么从 AST 的角度来实现这个 eval 函数.

对于ast而言, 我们需要定义节点类型, 解析器, 以及评估函数. 对于四则运算的表达式, 我们可以定义以下几种节点类型:
* 数字
* 二元运算符

```cpp
// ---------------- AST 节点 ----------------
struct ASTNode {
    virtual int eval() const = 0;
    virtual void print(std::ostream& os, int indent = 0) const = 0;
    virtual ~ASTNode() = default;

    friend std::ostream& operator<<(std::ostream& os, const ASTNode& node) {
        node.print(os);
        return os;
    }
};

struct IntNode : ASTNode {
    int value;
    explicit IntNode(int v) : value(v) {}
    int eval() const override { return value; }
    void print(std::ostream& os, int indent = 0) const override {
        os << std::string(indent, ' ') << "IntNode(" << value << ")";
    }
};

struct BinOpNode : ASTNode {
    char op;
    std::unique_ptr<ASTNode> left, right;
    BinOpNode(char o, std::unique_ptr<ASTNode> l, std::unique_ptr<ASTNode> r)
        : op(o), left(std::move(l)), right(std::move(r)) {}
    int eval() const override {
        int l = left->eval();
        int r = right->eval();
        switch (op) {
            case '+': return l + r;
            case '-': return l - r;
            case '*': return l * r;
            case '/':
                if (r == 0) throw std::runtime_error("Division by zero");
                return l / r;
        }
        throw std::runtime_error("Unknown operator in eval");
    }

    void print(std::ostream& os, int indent = 0) const override {
        os << std::string(indent, ' ') << "BinOpNode(" << op << ")\n";
        left->print(os, indent + 2);
        os << "\n";
        right->print(os, indent + 2);
    }
};
```

其中`print`函数用于打印 AST 结构, 方便调试. 而`eval`函数则用于计算节点的值.

接下来是解析器部分, 我们使用递归下降解析器来构建 AST. 这里的递归下降的核心思想就是将表达式按照运算优先级拆分为多个层次, 每个层次对应一个解析函数.
比如 `+`, `-` 优先级最低, 所以最外层是 `expr` 函数; `*`, `/` 优先级次之, 所以中间层是 `term` 函数; 最内层是 `factor`, 处理数字和括号.

```cpp
// ---------------- Parser ----------------
class Parser {
    std::string s;
    size_t pos = 0;

    // 跳过空白
    void skip_ws() {
        while (pos < s.size() && std::isspace(static_cast<unsigned char>(s[pos]))) ++pos;
    }

    // 返回当前可见字符（会先跳空白），不消耗
    char peek() {
        skip_ws();
        return pos < s.size() ? s[pos] : '\0';
    }

    // 返回当前可见字符并前移一位（会先跳空白）
    char get() {
        skip_ws();
        return pos < s.size() ? s[pos++] : '\0';
    }

    std::unique_ptr<ASTNode> number() {
        skip_ws();
        if (pos >= s.size() || !std::isdigit(static_cast<unsigned char>(s[pos]))) {
            throw std::runtime_error("Expected number at position " + std::to_string(pos));
        }
        int val = 0;
        while (pos < s.size() && std::isdigit(static_cast<unsigned char>(s[pos]))) {
            val = val * 10 + (s[pos++] - '0');
        }
        return std::make_unique<IntNode>(val);
    }

    // factor 处理: number | '(' expr ')' | unary +/-
    std::unique_ptr<ASTNode> factor() {
        char c = peek();
        if (c == '(') {
            get(); // consume '('
            auto node = expr();
            if (peek() != ')') throw std::runtime_error("Missing closing ')' at pos " + std::to_string(pos));
            get(); // consume ')'
            return node;
        }
        // 一元 +/-
        if (c == '+' || c == '-') {
            char sign = get();
            auto rhs = factor(); // 注意递归以支持 - ( -1 ) 等
            if (sign == '+') return rhs;
            // -x  -> (-1) * x
            return std::make_unique<BinOpNode>('*', std::make_unique<IntNode>(-1), std::move(rhs));
        }
        return number();
    }

    // term 处理乘除
    std::unique_ptr<ASTNode> term() {
        auto node = factor();
        while (true) {
            char c = peek();
            if (c == '*' || c == '/') {
                char op = get();
                auto rhs = factor();
                node = std::make_unique<BinOpNode>(op, std::move(node), std::move(rhs));
            } else break;
        }
        return node;
    }

    // expr 处理加减
    std::unique_ptr<ASTNode> expr() {
        auto node = term();
        while (true) {
            char c = peek();
            if (c == '+' || c == '-') {
                char op = get();
                auto rhs = term();
                node = std::make_unique<BinOpNode>(op, std::move(node), std::move(rhs));
            } else break;
        }
        return node;
    }

public:
    explicit Parser(const std::string& str) : s(str), pos(0) {}
    std::unique_ptr<ASTNode> parse() {
        auto root = expr();
        skip_ws();
        if (pos != s.size()) {
            throw std::runtime_error("Unexpected token after parse at pos " + std::to_string(pos));
        }
        return root;
    }
};
```

`parser`类负责将输入字符串解析为 AST. 它维护一个位置指针, 指向当前正在处理的字符.

* `skip_ws`函数跳过空白字符. 包括空格, 制表符等.
* `peek`函数返回当前可见字符但不前移位置指针.
* `get`函数返回当前可见字符并前移位置指针.
* `number`函数解析一个整数并返回一个`IntNode`.

```cpp
// main
// ---------------- 测试 ----------------
int main() {
    try {
        std::string input = "3 + 4 * (5 - 2)";
        Parser parser(input);
        auto ast = parser.parse();

        std::cout << "Eval result: " << ast->eval() << "\n";
        std::cout << "AST structure:\n" << *ast << "\n";

        // 额外测试：带空格、前缀负号、多位数
        std::vector<std::string> tests = {
            "3 + 4 + 5 + 6",
            "  12 + 34 ",
            "-3 + (2 * 5)",
            " (1 + 2) * (3 + 4) ",
            "10/2 + 6* -2"
        };
        for (auto &t : tests) {
            Parser p(t);
            auto a = p.parse();
            std::cout << t << " = " << a->eval() << "\n";
            std::cout << "AST:\n" << *a << "\n";
        }
    } catch (const std::exception &e) {
        std::cerr << "Parse/eval error: " << e.what() << "\n";
    }
    return 0;
}
```

```bash
3 + 4 + 5 + 6 = 18
AST:
BinOpNode(+)
  BinOpNode(+)
    BinOpNode(+)
      IntNode(3)
      IntNode(4)
    IntNode(5)
  IntNode(6)
  12 + 34  = 46
AST:
BinOpNode(+)
  IntNode(12)
  IntNode(34)
-3 + (2 * 5) = 7
AST:
BinOpNode(+)
  BinOpNode(*)
    IntNode(-1)
    IntNode(3)
  BinOpNode(*)
    IntNode(2)
    IntNode(5)
 (1 + 2) * (3 + 4)  = 21
AST:
BinOpNode(*)
  BinOpNode(+)
    IntNode(1)
    IntNode(2)
  BinOpNode(+)
    IntNode(3)
    IntNode(4)
10/2 + 6* -2 = -7
AST:
BinOpNode(+)
  BinOpNode(/)
    IntNode(10)
    IntNode(2)
  BinOpNode(*)
    IntNode(6)
    BinOpNode(*)
      IntNode(-1)
      IntNode(2)
```