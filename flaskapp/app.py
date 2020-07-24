from flask import Flask, render_template, redirect, url_for, request
import test

app = Flask(__name__)

@app.route("/")
def home_function():
    return render_template("home.html")

@app.route("/redirect")
def redirect():
    return render_template("redirect.html")

    
