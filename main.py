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

re_md = re.compile('\\@slider .*\r')

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
        #saving markdown content
        with open('temp.md', 'w') as file:
            file.write(text)
        # turning it into html
        html_from_md = markdown(text, extras=['fenced-code-blocks'])
        sliders = re_md.findall(text)
        if len(sliders) > 0:
            for s in sliders:
                folder = s.split(' ')[1].replace('\r', '')
                # print(app.static_folder)
                folder = os.path.join('static', folder)
                slider_temp = template_slider
                slider_temp = slider_temp.replace('folder_placeholder', folder)
                slider_temp = slider_temp.replace('number_of_images_placeholder', str(len(os.listdir(folder))))

                html_from_md = html_from_md.replace(markdown(s), slider_temp)

        with open('temp.html', 'w') as file:
            file.write(html_from_md)
    with open('temp.md', 'r') as file:
        text = file.read()
    form.pagedown.data = text
    print(form.pagedown.data)
    return render_template('index.html', form=form, text=text)

@app.route('/preview', methods=['GET'])
def preview():
    return render_template('preview.html')


if __name__ == '__main__':
    app.run(debug=True)
