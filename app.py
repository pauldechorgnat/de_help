from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socket_io = SocketIO(app=app)


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





if __name__ == '__main__':
    socket_io.run(app, debug=True)