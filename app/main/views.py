from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import User
from . import main
from .forms import NameForm, EssayForm
from datetime import datetime
from ..scoring import get_score

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

@main.route('/essay', methods=['GET', 'POST'])
def essay():
    form = EssayForm()
    if form.validate_on_submit():
        text = form.essay.data
        add_time = datetime.now()
        score = get_score(text)
        flash(score)
        #return redirect(url_for('.index'))
    return render_template('essay.html',form=form)