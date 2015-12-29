from flask import render_template, flash, redirect, session, url_for, request, g
from tranview import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("base.html")
