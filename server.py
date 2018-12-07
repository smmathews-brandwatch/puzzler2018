import flask
import webbrowser

app = flask.Flask(__name__)
app.debug = True
app.env = 'development'

@app.route('/', methods=['GET'])
def health():
    return 'Your server is running'

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/')
    app.run()
