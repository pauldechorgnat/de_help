from flask import Flask, render_template
from flask_socketio import SocketIO
import datetime
import re
import os
from bs4 import BeautifulSoup

app = Flask(__name__)
socket_io = SocketIO(app=app)

footer = '''
<script>
    next_slide = function(element, number_of_images){
        var image_name = element.src.match('image[0-9]+\\.png')[0];
        var new_image_number = (Number.parseInt(image_name.match('[0-9]+')) + 1) % number_of_images;
        var new_image_path = 'image' + new_image_number + '.png';
        element.src = element.src.replace(RegExp('image[0-9]+\\.png'), new_image_path);
        return false;
    }
</script>
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/styles/default.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.10/highlight.min.js"></script>

<script>
hljs.configure({useBR: true});
document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('blockquote code').forEach((block) => {
    hljs.highlightBlock(block);
  });
});
</script>
<script>
    evt = document.createEvent("HTMLEvents");
    evt.initEvent('DOMContentLoaded');
    document.dispatchEvent(evt);
</script>
<script>
    function copyText(element) {
      var range, selection, worked;

      if (document.body.createTextRange) {
        range = document.body.createTextRange();
        range.moveToElementText(element);
        range.select();
      } else if (window.getSelection) {
        selection = window.getSelection();
        range = document.createRange();
        range.selectNodeContents(element);
        selection.removeAllRanges();
        selection.addRange(range);
      }

      try {
        document.execCommand('copy');
        alert('text copied');
      }
      catch (err) {
        alert('unable to copy text');
      }
    }
</script>
<style>
    body {
        font-family: Source Sans Pro,sans-serif;
        }
    .slider {
        width:80%;
        margin-left: auto;
        margin-right: auto;
        height:auto;
    }
</style>
'''


def parse_summary(text):
    h1s = text.split('<h1>')[1:]
    # h1s=[]
    summary = '<ol>'
    for h1_index, h1 in enumerate(h1s):
        title = h1.split('</h1>')[0]
        summary += '<li>' + title + '</li>'
        h2s = ''.join(h1.split('</h1>')[1:]).split('<h2>')[1:]
        if len(h2s) > 0:
            summary += '<ol>'
            for h2 in h2s:
                title = h2.split('</h2>')[0]
                print(title)
                summary += '<li>' + title + '</li>'
                h3s = ''.join(h2.split('</h2>')[1:]).split('<h3>')[1:]
                if len(h3s) > 0:
                    summary += '<ol>'
                    for h3 in h3s:
                        title = h3.split('</h3>')[0]
                        print(title)
                        summary += '<li>' + title + '</li>'
                        h4s = ''.join(h3.split('</h3>')[1:]).split('<h4>')[1:]
                        if len(h4s) > 0:
                            summary += '<ol>'
                            for h4 in h4s:
                                title = h4.split('</h4>')[0]
                                print(title)
                                summary += '<li>' + title + '</li>'
                            summary += '</ol>'
                    summary += '</ol>'
            summary += '</ol>'

    return summary + '</ol>'


def backup(text):
    d = datetime.datetime.now()
    with open('backups/backup_' + str(d) + '.txt', 'w') as file:
        file.write(text)


def generate_slider(folder_name):
    n = len(os.listdir('./static/' + folder_name))
    url = os.path.join('https://raw.githubusercontent.com/pauldechorgnat/de_help/master/static/', folder_name)

    template = '''<div class="slider">
    <center>
        <img src="folder_placeholder/image0.png" style="cursor:pointer; margin-left: auto; margin-right: auto; width:80%; height:auto;"
             onclick="next_slide(this, number_of_images_placeholder);return false;"/>
    </center>
    </div>'''
    return template.replace('folder_placeholder', url).replace('number_of_images_placeholder', str(n))


def create_new_html_code(raw_text):
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


def format_html(text):
    soup = BeautifulSoup(text, features='html.parser')
    for block_quote in soup.find_all('blockquote'):
        code = block_quote.find_next('code')

        # changing the <br> and \n\r
        raw_text = ''.join([str(c) for c in code.contents]).replace('<br/>', '<br>')

        new_text = create_new_html_code(raw_text)
        # print(code.string)
        code.string = new_text
        # adding the reactions:

        code.attrs['onclick'] = 'copyText(this);'
        code.attrs['style'] = 'cursor:pointer;'

    return str(soup).replace('&amp;', '&').replace('&lt;br&gt;', '<br>')


def generate_html(text):
    re_md = re.compile('\\@slider .*\n')

    # code_block_begin_re = re.compile('<blockquote>\r\n<code>\r\n')
    # code_block_end_re = re.compile('</code>\r\n</blockquote>')
    # breaking_line_html = re.compile('\<br\>')
    # breaking_line = re.compile('\r\n')

    text = format_html(text)
    text = text.replace('&lt;br&gt;', '')
    sliders = re_md.findall(text)

    if len(sliders) > 0:

        for s in sliders:
            print(s)
            folder = s.split(' ')[1].replace('\n', '')

            text = text.replace(s, generate_slider(folder_name=folder))

    return text + footer


@app.route('/')
def index():
    return render_template('index.html')


@socket_io.on('generate_summary')
def generate_summary(data):
    summary = parse_summary(data['text'])
    socket_io.emit('summary_generated',
                   {
                       'summary': summary
                   })


@socket_io.on('backup')
def backup_code(data):
    backup(data['text'])


@socket_io.on('generate_preview')
def generate_preview(data):
    new_text = generate_html(data['text'])
    socket_io.emit('preview_generated', {'preview': new_text})


@socket_io.on('save')
def save(data):
    try:
        new_text = generate_html(data['text'])
        with open('final.html', 'w') as file:
            file.write(new_text)
        socket_io.emit('saved')
    except:
        socket_io.emit('error')


if __name__ == '__main__':
    socket_io.run(app, debug=True, port=5005)
