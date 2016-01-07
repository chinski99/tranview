from tranview import db
from nltk import sent_tokenize


class ContentText(db.Model):
    __tablename__ = "content_text"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), index=True, unique=True)
    content = db.Column(db.Text(), index=True)
    lines = db.relationship('Line', cascade="all,delete", backref='content_text', lazy='dynamic')
    trans_id = db.Column(db.Integer)
    original_id = db.Column(db.Integer, db.ForeignKey('content_text.id'))
    translations = db.relationship('ContentText', cascade="all,delete",
                                   backref=db.backref('original', remote_side=[id]))

    def __repr__(self):
        return '<Text %r>' % (self.title)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sto = sent_tokenize(self.content)
        for i, l in enumerate(sto):
            self.lines.append(Line(lineno=i, body=l))


class Line(db.Model):
    __tablename = "line"
    id = db.Column(db.Integer, primary_key=True)
    lineno = db.Column(db.Integer)
    body = db.Column(db.String())
    text_id = db.Column(db.Integer, db.ForeignKey('content_text.id'))

    def __repr__(self):
        return '<Line %r>' % (self.body)
