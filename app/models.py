from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class Essay(db.Model):
    __tablename__ = 'essays'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime(True))
    score = db.Column(db.Float)
    spell_errors = db.Column(db.Text)
    grammar_errors = db.Column(db.Text)
    
    def __repr__(self):
        return '<Essay {0}>: {1}. Created at:{2}'.format(self.text, self.score, self.time)
    
    