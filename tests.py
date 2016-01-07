#!flask/bin/python
import os
import unittest

from config import basedir
from tranview import app, db
from nltk import sent_tokenize

from tranview.models import ContentText, Line


class MyTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_contenttext(self):
        text1 = "Ala ma kota. Ola ma psa. Pies Oli to Azor."
        ct = ContentText(title="test", content=text1)
        db.session.add(ct)
        db.session.commit()
        ct_test = ContentText.query.filter_by(title="test").first()
        assert ct_test.content == text1

    def test_tokenize(self):
        text1 = "Ala ma kota. Ola ma psa. Pies Oli to Azor."
        ct = ContentText(title="test", content=text1)
        db.session.add(ct)
        db.session.commit()
        ct_test = ContentText.query.filter_by(title="test").first()
        l0 = ct_test.lines[1]
        assert l0.body == "Ola ma psa."

    def test_append_translations(self):
        # check relationship between original and translations(s)
        orig = "Ala ma kota. Ola ma psa. Pies Oli to Azor."
        t1 = "Ala has a cat. Ola has a dog. Ola's dog is Azor."
        t2 = "Ala owns a cat. Ola owns a dog. Ola's dog's name is Azor."
        ct = ContentText(title="original", content=orig)
        t1ct = ContentText(title="trans1", content=t1, original=ct)
        t2ct = ContentText(title="trans2", content=t2, original=ct)
        assert (len(ct.translations) == 2)
        lo = [i.body for i in ct.lines]
        lt1 = [i.body for i in ct.translations[1].lines]
        nl = list(zip(lo, lt1))
        self.assertEqual(len(nl), 3)
        db.session.add(ct)
        db.session.commit()
        res = ContentText.query.filter_by(title="original").first()
        self.assertEqual(len(res.translations), 2)

    def test_compreh(self):
        orig = "Ala ma kota. Ola ma psa. Pies Oli to Azor."
        t1 = "Ala has a cat. Ola has a dog. Ola's dog is Azor."
        t2 = "Ala owns a cat. Ola owns a dog. Ola's dog's name is Azor."
        ct = ContentText(title="original", content=orig)
        t1ct = ContentText(title="trans1", content=t1, original=ct)
        t2ct = ContentText(title="trans2", content=t2, original=ct)
        l = [tran.lines[1].body for tran in ct.translations]
        self.assertEqual(len(l), 2)

    def test_delete(self):
        # check relationship between original and translations(s)
        orig = "Ala ma kota. Ola ma psa. Pies Oli to Azor."
        t1 = "Ala has a cat. Ola has a dog. Ola's dog is Azor."
        t2 = "Ala owns a cat. Ola owns a dog. Ola's dog's name is Azor."
        ct = ContentText(title="original", content=orig)
        t1ct = ContentText(title="trans1", content=t1, original=ct)
        t2ct = ContentText(title="trans2", content=t2, original=ct)
        db.session.add(ct)
        db.session.commit()
        res = ContentText.query.filter_by(title="original").first()
        lines = Line.query.all()
        assert (len(lines), 9)
        assert (len(res.translations) == 2)
        t1 = res.translations[0]
        db.session.delete(t1)
        db.session.commit()
        assert (len(res.translations) == 1)
        lines = Line.query.all()
        assert (len(lines), 6)



if __name__ == '__main__':
    unittest.main()
