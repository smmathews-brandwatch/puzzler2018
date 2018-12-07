import flask
import webbrowser

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def health():
    return 'Your server is running'

if __name__ == "__main__":
    webbrowser.open_new_tab('http://0.0.0.0:5000/')
    app.run()
