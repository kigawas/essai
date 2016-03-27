from flask import render_template, session, redirect, url_for, current_app, flash
from .. import db
from ..models import Essay
from . import main
from .forms import EssayForm
from ..scoring import EssayScorer

import json
from datetime import datetime

@main.route('/', methods=['GET', 'POST'])
def index():
    form = EssayForm()
    if form.validate_on_submit():
        text = form.essay.data
        time = datetime.now()
        es = EssayScorer(text)
        score, spell_e, gram_e, coh = es.score, es.spell_errors, es.grammar_errors, es.coherence
        essay_tuple = Essay(text=text, time=time, score=score, spell_errors=spell_e, grammar_errors=gram_e, coherence=coh)
        db.session.add(essay_tuple)
        flash(spell_e)
        flash(json.loads(gram_e))
        #return redirect(url_for('.index'))
    return render_template('essay.html',form=form)