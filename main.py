from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField
from markdown2 import markdown
import re
import os
from bs4 import BeautifulSoup
from utils import format_text2

chevrons = {
    'right': '&gt;',
    'left': '&lt;'
}



re_md = re.compile('\\@slider .*\r')

code_block_begin_re = re.compile('<blockquote>\r\n<code>\r\n')
code_block_end_re = re.compile('</code>\r\n</blockquote>')
breaking_line_html = re.compile('\<br\>')
breaking_line = re.compile('\r\n')


template_slider = open('slider.html', 'r').read()

app = Flask(__name__, template_folder='.' )
app.config['SECRET_KEY'] = 'lol'
pagedown = PageDown(app)
socket = SocketIO(app=app)
bs = Bootstrap(app)


class PageDownFormExample(FlaskForm):
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PageDownFormExample()
    if form.validate_on_submit():
        # getting the text
        text = form.pagedown.data

        text = format_text2(text)
        text = text.replace('&lt;br&gt;', '')
        #saving markdown content
        with open('temp.md', 'w') as file:
            file.write(text)
        # turning it into html
        html_from_md = markdown(text, extras=['fenced-code-blocks'])
        sliders = re_md.findall(text)


        if len(sliders) > 0:
            for s in sliders:
                print(s)
                folder = s.split(' ')[1].replace('\r', '')
                # print(app.static_folder)
                url = os.path.join('https://raw.githubusercontent.com/pauldechorgnat/de_help/master/static/', folder)
                folder = os.path.join('static', folder)
                slider_temp = template_slider
                slider_temp = slider_temp.replace('folder_placeholder', url)
                slider_temp = slider_temp.replace('number_of_images_placeholder', str(len(os.listdir(folder))))
                print(slider_temp)
                text = text.replace(s, slider_temp)


        with open('temp.html', 'w') as file:
            file.write(text)
    with open('temp.md', 'r') as file:

        text = file.read()
    form.pagedown.data = text
    return render_template('index.html', form=form, text=text)

@app.route('/preview', methods=['GET'])
def preview():
    with open('final.html', 'w') as file:
        file.write(render_template('preview.html'))
    return render_template('preview.html')


if __name__ == '__main__':
    app.run(debug=True)
