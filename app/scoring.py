# encoding: utf-8
import json
import string
import sys
import os
sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'coheoka'))

import numpy as np
import enchant
import language_check
from nltk import sent_tokenize, word_tokenize

from coheoka.evaluator import Evaluator
from coheoka.coherence_probability import ProbabilityVector
from coheoka.utils import pk_load


class LexicalFeature(object):
    def __init__(self, essay):
        self.essay = essay
        self.sents = sent_tokenize(self.essay)
        self.words = []
        for sent in self.sents:
            self.words.extend(word_tokenize(sent))
        self.pos = []
        self.type_token_ratio = len(set(self.words)) / len(self.words)
        self.sent_counts = len(self.sents)
        self.char_counts = sum(map(lambda x: len(x), self.sents))
        self.word_counts = len(self.words)
        self.long_word_counts = len(filter(lambda x: len(x) >= 5, self.words))
        self.awl = sum(map(lambda x: len(x), self.words)) / float(
            self.word_counts)
        self.punctuation_counts = self.__punc_count()
        self.err_count = self.__spell_errors() / float(self.sent_counts)

    def get_all_features(self):
        return self.type_token_ratio, self.sent_counts, \
            self.char_counts, self.word_counts, \
            self.long_word_counts, self.awl, \
            self.punctuation_counts, self.err_count

    def __punc_count(self):
        return len(filter(lambda x: x in string.punctuation, self.words))

    def __spell_errors(self):
        d = enchant.Dict('en-US')
        err_count = 0
        for word in filter(lambda x: x.isalnum() and x.islower(), self.words):
            if d.check(word) is False:
                err_count += 1
        return err_count


class EssayScorer(object):
    d = enchant.Dict('en-US')
    t = language_check.LanguageTool('en-US')
    t.disable_spellchecking()

    basedir = os.path.abspath(os.path.dirname(__file__))
    tfidf = pk_load(os.path.join(basedir, 'pickles', 'tfidf.pkl'))
    scaler = pk_load(os.path.join(basedir, 'pickles', 'scaler.pkl'))
    clf = pk_load(os.path.join(basedir, 'pickles', 'clf.pkl'))
    ev = pk_load(os.path.join(basedir, 'pickles', 'ev.pkl'))
    pv = pk_load(os.path.join(basedir, 'pickles', 'pv.pkl'))
    no_checking_id = ['WHITESPACE_RULE', 'EN_QUOTES']

    def __init__(self, essay, ret_json=False):
        self.ret_json = ret_json
        self.essay = '. '.join(essay.split('.'))
        self.sents = [s.strip() for s in sent_tokenize(self.essay)]
        self.sent_words = [word_tokenize(s) for s in self.sents]
        self.words = [w for w in sum(self.sent_words, []) if w.isalnum()]
        self.score = self.__score()
        self.spell_errors = self.__spell_check()
        self.grammar_errors = self.__grammar_check()
        self.coherence = self.__coherence()

    def __score(self):
        lf = [LexicalFeature(self.essay).get_all_features()]
        X = np.concatenate(
            (EssayScorer.tfidf.transform([self.essay]),
             EssayScorer.scaler.transform(lf)),
            axis=1)
        return str(EssayScorer.clf.predict(X)[0])

    def __spell_check(self):
        res = {}
        for i, s in enumerate(self.sent_words):
            res[i] = []
            for w in s:
                if w.isalnum() and EssayScorer.d.check(w) is False:
                    res[i].append({w: EssayScorer.d.suggest(w)[:2]})
        return json.dumps(res) if self.ret_json else res

    def __grammar_check(self):
        res = {}
        for i, s in enumerate(self.sents):
            errors = EssayScorer.t.check(s)
            res[i] = [e.__dict__
                      for e in errors
                      if e.ruleId not in EssayScorer.no_checking_id]

        return json.dumps(res) if self.ret_json else res

    def __coherence(self):
        if len(sent_tokenize(self.essay)) == 1:
            return 'Only one sentence. No coherence.'
        prob_coh = EssayScorer.pv.evaluate_coherence(self.essay)
        rank_coh = EssayScorer.ev.evaluate_coherence(self.essay)
        if rank_coh < 0:
            return 'Poor'
        elif 0 <= rank_coh < 0.2:
            return 'Fair'
        else:
            return 'Good'



def test_coherence_work():
    corpus = ['I love you. A computer is a machine.',
              'English is an international language. Lots of people learn it.']
    #corpus = ['I love you. A computer is a machine.', 'English is an international language. Lots of people learn it.']
    ev = Evaluator(corpus).make_data_and_clf().fit()
    pv = ProbabilityVector(corpus).make_probs()
    print ev.evaluate_coherence('I love you.')
    print pv.evaluate_coherence(
        'Time flies by. This is what we face. I love you.')


if __name__ == "__main__":
    text1 = 'A sentence witj a error in the Hitchhiker\'s Guide tot he Galaxy.'

    text2 = ('English is a internationaly language'
             ' which becomes importantly for modern world.')

    text3 = ('However, perhaps the discussion of man triumphing'
             'over nature makes little sense, as an economist once wrote,'
             ' "man talks of a battle with Nature, '
             'forgetting that if he won the battle, '
             'he would find himself on the losing side ".')
    T = text1
    e = EssayScorer(T)
    print e.sents
    print e.words
    print e.spell_errors
    print e.grammar_errors
    print e.score

    print EssayScorer.pv.evaluate_coherence(text1 + ' I love you.')
    print EssayScorer.ev.evaluate_coherence(text1)
    print EssayScorer.ev.evaluate_coherence(text2)
