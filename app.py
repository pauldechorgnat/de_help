from flask import Flask, render_template
from flask_socketio import SocketIO
import datetime
import re
import os
from bs4 import BeautifulSoup

app = Flask(__name__)
socket_io = SocketIO(app=app)

header = '''
<head>
	<style>
		table {
			margin: 20px;
		}

		body {
			font-family: Source Sans Pro,sans-serif;
		}
		.slider {
			width:80%;
			margin-left: auto;
			margin-right: auto;
			height:auto;
        }

		.code {
			margin: 20px;
			border-radius: 5px;
			border-color: #000000;
		}
		.alert-info {
		    margin: 20px;
			border-radius: 5px;
			padding: 5px;
		}
		.alert-danger {
		    margin: 20px;
			border-radius: 5px;
			padding: 5px;
		}



	</style>
</head>
<body>
	<div class="container">
'''

footer = r'''			<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
			integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
			<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
			integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
			crossorigin="anonymous"></script>
			<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
			integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
			crossorigin="anonymous"></script>
			<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.3.3/ace.js" type="text/javascript"
			charset="utf-8"></script>
    <script>
	change_code = function(language='python'){
		var regular_expression = new RegExp(/^(\t)+/);
		var divs = document.getElementsByClassName(language);
		for (var i=0; i<divs.length; i++){
			var element = divs[i];
			element.style['margin'] = '20px';
            // element.style['border-radius'] = '5px';
            var lines = element.innerHTML.split('\n');
            var nb_lines = lines.length;
            text = element.innerHTML;
            element.style.height = ((nb_lines) * 16) + 'px';
            var editor = ace.edit(divs[i].id);
            text = text.split('&amp;').join('&');
            text = text.split('&gt;').join('>');
            text = text.split('&lt;').join('<');
            editor.setValue(text.substring(1), -1);
            editor.setTheme("ace/theme/monokai");
            editor.session.setMode("ace/mode/" + language);
            // editor.session.highlight()
            editor.setFontSize('16px');
            // editor.session.indentRows(startRow=0, endRow=nb_lines, indentString='\t');

         	// beautify.beautify(editor.session);
         	editor.setReadOnly(true);
         }
     }
     var languages = ['python', 'sh', 'yaml', 'xml', 'pig', 'sql', 'hbase', 'json', 'dockerfile'];
     for (var l=0; l<languages.length; l++){
     	change_code(languages[l]);
     }




 </script>
 <script>
 	next_slide = function(element, number_of_images){
 		var image_name = element.src.match('image[0-9]+\\.png')[0];
 		var new_image_number = (Number.parseInt(image_name.match('[0-9]+')) + 1) % number_of_images;
 		var new_image_path = 'image' + new_image_number + '.png';
 		element.src = element.src.replace(RegExp('image[0-9]+\\.png'), new_image_path);
 		return false;
 	}



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

</div>
</body>
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


# def create_new_html_code(raw_text):
#     line_break = re.compile('\r|\n|<br>')
#     new_text = line_break.split(raw_text)
#     new_lines = []
#     for i, line in enumerate(new_text):
#         # print(i, line)
#         new_line = line.replace('<', r'&lt;').replace('>', u'&gt;')
#         if len(new_line) > 0:
#             new_lines.append(new_line)
#     new_text = '<br>\n'.join(new_lines)
#
#     return new_text
#
#
# def format_html(text):
#     soup = BeautifulSoup(text, features='html.parser')
#     for block_quote in soup.find_all('blockquote'):
#         code = block_quote.find_next('code')
#
#         # changing the <br> and \n\r
#         raw_text = ''.join([str(c) for c in code.contents]).replace('<br/>', '<br>')
#
#         new_text = create_new_html_code(raw_text)
#         # print(code.string)
#         code.string = new_text
#         # adding the reactions:
#
#         code.attrs['onclick'] = 'copyText(this);'
#         code.attrs['style'] = 'cursor:pointer;'
#
#     return str(soup).replace('&amp;', '&').replace('&lt;br&gt;', '<br>')


def generate_html(text):
    re_md = re.compile('\\@slider .*\n')

    # code_block_begin_re = re.compile('<blockquote>\r\n<code>\r\n')
    # code_block_end_re = re.compile('</code>\r\n</blockquote>')
    # breaking_line_html = re.compile('\<br\>')
    # breaking_line = re.compile('\r\n')

    # text = format_html(text)
    # text = text.replace('&lt;br&gt;', '')
    sliders = re_md.findall(text)
    for s in sliders:
        print(s)
        folder = s.split(' ')[1].replace('\n', '')

        text = text.replace(s, generate_slider(folder_name=folder))

    return header + text + footer


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
        with open('templates/final.html', 'w') as file:
            file.write(new_text)
        socket_io.emit('saved')
    except:
        socket_io.emit('error')

@app.route('/final')
def final():
    return render_template('final.html')


if __name__ == '__main__':
    socket_io.run(app, debug=True, port=5005)
