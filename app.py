from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/post_info", method=["POST"])
def post_info():
    return render_template("index.html")
