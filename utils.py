from bs4 import BeautifulSoup
import re

def create_new_text(raw_text):
    line_break = re.compile('\r|\n|<br>')
    new_text = line_break.split(raw_text)
    new_lines = []
    for i, line in enumerate(new_text):
        # print(i, line)
        new_line = line.replace('<', r'&lt;').replace('>', u'&gt;')
        if len(new_line) > 0:
            new_lines.append(new_line)
    new_text = '<br>\n'.join(new_lines)

    return new_text


def format_text2(text):
    soup = BeautifulSoup(text, features='html.parser')
    for block_quote in soup.find_all('blockquote'):
        code = block_quote.find_next('code')

        # changing the <br> and \n\r
        raw_text = ''.join([str(c) for c in code.contents]).replace('<br/>', '<br>')

        new_text = create_new_text(raw_text)
        # print(code.string)
        code.string = new_text

    return str(soup).replace('&amp;', '&').replace('&lt;br&gt;', '<br>')


html = '''
<blockquote>
<code class="lol">
ls -l | grep hadoop
</code>
</blockquote>'''


if __name__ == '__main__':
    new_html = format_text2(html)
    # print(new_html)
    print(format_text2(new_html))
