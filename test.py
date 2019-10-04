from markdown2 import markdown

text = '\n```python \n' \
       'print("hello world")\n' \
       '```'

print(text)

print(markdown(text, extras=['fenced-code-blocks'], ))