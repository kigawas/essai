import json
from datetime import datetime

from flask import (render_template, session, redirect, url_for, current_app,
                   flash)
from .. import db
from ..models import Essay
from . import main
from .forms import EssayForm
from ..scoring import EssayScorer


@main.route('/', methods=['GET', 'POST'])
def index():
    form = EssayForm()
    if form.validate_on_submit():
        text = form.essay.data
        time = datetime.now()
        es = EssayScorer(text)
        score, spell_e, gram_e, coh = (es.score, es.spell_errors,
                                       es.grammar_errors, es.coherence)
        essay_tuple = Essay(text=text,
                            time=time,
                            score=score,
                            spell_errors=json.dumps(spell_e),
                            grammar_errors=json.dumps(gram_e),
                            coherence=json.dumps(coh))
        db.session.add(essay_tuple)

        flash("Your essay is scored. You got point {} of 6.".format(score))
        return render_template('result.html', text=text, es=es, zip=zip)
    return render_template('index.html', form=form)


@main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
