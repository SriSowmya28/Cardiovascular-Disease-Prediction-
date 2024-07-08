from flask import Flask, render_template

app = Flask(__name__)


@app.route('/page1')
def home():
    return "<h1>hello</h1>"

if __name__ == "__main__":
    app.run(debug=True)

