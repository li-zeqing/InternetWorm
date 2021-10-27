import flask
from flask import render_template, Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('html_doc.html')

if __name__ == "__main__":
    app.run()