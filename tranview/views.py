from flask import render_template, flash, redirect, session, url_for, request, g
from tranview import app, db
from .forms import TextInputForm
from .models import ContentText, Line
from nltk.tokenize import sent_tokenize


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    texts = ContentText.query.filter_by(original_id=None).all()
    return render_template("index.html", texts=texts)


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = TextInputForm()
    if form.validate_on_submit():
        flash('New content added!')
        t = form.content.data
        text = ContentText(title=form.title.data, content=t)
        db.session.add(text)
        db.session.commit()
        session['textid'] = text.id
        return render_template("textview.html", text=text)
    return render_template("form.html", form=form)


@app.route('/textview/<int:id>')
def textview(id):
    text = ContentText.query.filter_by(id=id).first()
    return render_template("textview.html", text=text)


@app.route('/merge/<int:id>')
def merge(id):  # merges line with previous one
    text = ContentText.query.filter_by(id=session["textid"]).first()
    line = Line.query.filter_by(id=id).first()
    prev_line = Line.query.filter_by(lineno=line.lineno - 1, text_id=text.id).first()
    prev_line.body = prev_line.body + line.body
    db.session.delete(line)
    db.session.add(prev_line)
    follow_lines = Line.query.filter(Line.lineno > line.lineno, Line.text_id == text.id).all()
    for l in follow_lines:
        l.lineno = l.lineno - 1
        db.session.add(l)
    db.session.commit()
    return render_template("textview.html", text=text)


@app.route('/add_translation/<int:id>', methods=['GET', 'POST'])
def add_translation(id):  # add translation to selected original
    session['textid'] = id
    text = ContentText.query.filter_by(id=id).first()
    form = TextInputForm()
    if form.validate_on_submit():
        flash('New content added!')
        t = form.content.data
        trans = ContentText(title=form.title.data, content=t, original=text)
        db.session.add(trans)
        db.session.commit()
        return render_template("textview.html", text=text)
    if form.title.data is None:
        form.title.data = "Translation: " + text.title
    return render_template("form.html", form=form)


@app.route('/sidebyside/<int:id>')
def sidebyside(id):  # shows translation alongside its original text
    text = ContentText.query.filter_by(id=id).first()
    orig_text = text.original
    return render_template("sidebyside.html", title="Side by side compare", orig_lines=orig_text.lines,
                           trans_lines=text.lines)


@app.route('/all_translations/<int:id>')
def all_translations(id):  # shows translation alongside its original text
    text = ContentText.query.filter_by(id=id).first()
    return render_template("all_translations.html", title="See all translations", text=text)
