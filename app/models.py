from . import db


class Essay(db.Model):
    __tablename__ = 'essays'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime(True))
    score = db.Column(db.Float)
    spell_errors = db.Column(db.Text)
    grammar_errors = db.Column(db.Text)
    coherence = db.Column(db.Text)

    def __repr__(self):
        return '<Essay {0}>: {1}. Created at:{2}'.format(self.text, self.score, self.time)

