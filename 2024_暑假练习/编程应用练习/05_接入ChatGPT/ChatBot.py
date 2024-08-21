import openai
import re
import streamlit as st
import markdown2
from pygments import lex
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

ai_response_markdown = '''### 递推的概念

**递推**是一种通过已知的初始条件和递推关系，逐步推导出后续结果的方法。递推通常用于解决那些可以通过前一步的结果来推导出当前步结果的问题。

例如，斐波那契数列就是一个典型的递推问题。斐波那契数列的定义如下：
- \( F(0) = 0 \)
- \( F(1) = 1 \)
- \( F(n) = F(n-1) + F(n-2) \) （对于 \( n \geq 2 \)）

这里的递推关系是 \( F(n) = F(n-1) + F(n-2) \)，通过已知的初始条件 \( F(0) \) 和 \( F(1) \)，我们可以逐步计算出后续的斐波那契数。

### 递推与递归的关系

**递归**是一种函数调用自身的方法。递归通常用于解决那些可以分解为相同问题但规模更小的子问题的情况。

递推和递归在某些情况下可以相互转换。例如，斐波那契数列既可以用递推方法实现，也可以用递归方法实现。

**递归实现斐波那契数列：**
```python
def fibonacci_recursive(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)
```

**递推实现斐波那契数列：**
```python
def fibonacci_iterative(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b
```

### 递推与迭代的关系

**迭代**是一种通过循环来重复执行某个过程的方法。迭代通常用于解决那些可以通过重复某个步骤来逐步逼近结果的问题。

递推和迭代在很多情况下是相似的，因为它们都涉及到逐步计算。递推通常更侧重于通过已知的递推关系来计算结果，而迭代则更侧重于通过循环来重复执行某个过程。 

**迭代实现斐波那契数列：**
```python
def fibonacci_iterative(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b
```

### 总结

- **递推**：通过已知的初始条件和递推关系，逐步推导出后续结果。
- **递归**：函数调用自身，解决可以分解为相同问题但规模更小的子问题。
- **迭代**：通过循环重复执行某个过程，逐步逼近结果。

递推、递归和迭代不是同一个层面的概念，但它们之间有密切的关系。递推和递归可以相互转换，而递推和迭代在很多情况下是相似的。

### 编程题目

**题目：** 使用递推方法计算斐波那契数列的第 \( n \) 项。

**要求：**
1. 编写一个函数 `fibonacci(n)`，使用递推方法计算斐波那契数列的第 \( n \) 项。
2. 函数应返回第 \( n \) 项的值。

**示例：**
```python
print(fibonacci(0))  # 输出 0
print(fibonacci(1))  # 输出 1
print(fibonacci(5))  # 输出 5
print(fibonacci(10)) # 输出 55
```

**解答：**
```python
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b
```

希望这个讲解和题目能帮助你理解递推的概念以及它与递归、迭代之间的关系。如果有任何问题，欢迎随时提问！'''

def highlight_code(code, language):
    lexer = get_lexer_by_name(language)
    formatter = HtmlFormatter(style="colorful")
    highlighted_code = highlight(code, lexer, formatter)
    return f'<div class="highlighted-code">{highlighted_code}</div>'

def markdown_to_html(markdown_text):
    # 将Markdown转换为HTML
    html_text = markdown2.markdown(markdown_text)

    # 匹配所有的<code>标签
    code_blocks = re.findall(r'<code class="(.*?)">(.*?)</code>', html_text, re.DOTALL)

    # 对所有的代码块进行高亮
    for language, code in code_blocks:
        highlighted_code = highlight_code(code, language)
        #highlighted_code = lex(code, language)
        html_text = html_text.replace(f'<code class="{language}">{code}</code>', highlighted_code)

    return html_text


def get_answer(question):
    api_key = "sk-b4276afe3b344c29be0d95ea86d8085d"
    client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一位编程老师，需要给小朋友出一道编程方面的题目，并讲解。"},
            {"role": "user", "content": question},
        ],
        stream=False
    )
    return response.choices[0].message.content

def main():
    st.title("AI 聊天机器人")
    st.markdown("与 AI 聊天，输入你的问题：")

    user_input = st.text_input("你：", "")
    if user_input:
        #ai_response_markdown = get_answer(user_input)
        ai_response_html = markdown_to_html(ai_response_markdown)
        st.markdown(ai_response_html, unsafe_allow_html=True)
        #st.text_area("AI：", ai_response_markdown, height=500)

    return

if __name__ == "__main__":
    main()
    #ai_response_html = markdown_to_html(ai_response_markdown)
    #print(ai_response_html)