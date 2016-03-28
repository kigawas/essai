# encoding: utf-8
import enchant
import language_check
from nltk import sent_tokenize, word_tokenize
import json, string, os
import cPickle as pickle
import numpy as np

class LexicalFeature:
    def __init__(self, essay):
        self.essay = essay
        self.sents = sent_tokenize(self.essay)
        self.words = []
        for sent in self.sents:
            self.words.extend(word_tokenize(sent))
        self.pos = []
        self.type_token_ratio = len(set(self.words))/len(self.words)
        self.sent_counts = len(self.sents)
        self.char_counts = sum(map(lambda x:len(x), self.sents))
        self.word_counts = len(self.words)
        self.long_word_counts = len(filter(lambda x:len(x)>=5, self.words))
        self.awl = sum(map(lambda x:len(x), self.words))/float(self.word_counts)
        self.punctuation_counts = self.__punc_count()
        self.err_count = self.__spell_errors()/float(self.sent_counts)

    def get_all_features(self):
        return self.type_token_ratio, self.sent_counts, \
                self.char_counts, self.word_counts, \
                self.long_word_counts, self.awl, \
                self.punctuation_counts, self.err_count

    def __punc_count(self):
        return len(filter(lambda x:x in string.punctuation, self.words))

    def __spell_errors(self):
        try:
            import enchant
        except ImportError:
            return 0
        d = enchant.Dict('en-US')
        err_count = 0
        for word in filter(lambda x:x.isalnum() and x.islower(), self.words):
            if d.check(word) is False:
                #print word
                err_count += 1
        return err_count


class EssayScorer(object):
    d = enchant.Dict('en-US')
    t = language_check.LanguageTool('en-US')
    t.disable_spellchecking()

    basedir = os.path.abspath(os.path.dirname(__file__))
    tfidf = pickle.load(open(basedir+'/pickles/tfidf'))
    scaler = pickle.load(open(basedir+'/pickles/scaler'))
    clf = pickle.load(open(basedir+'/pickles/clf'))

    def __init__(self, essay):
        self.essay = essay
        self.sents = [word_tokenize(sent) for sent in sent_tokenize(essay)]
        self.words = filter(lambda x:x.isalnum(), sum(self.sents, []))
        self.score = self.__score()
        self.spell_errors = self.__spell_check()
        self.grammar_errors = self.__grammar_check()
        self.coherence = self.__coherence()

    def __score(self):
        lf = [LexicalFeature(self.essay).get_all_features()]
        X = np.concatenate((EssayScorer.tfidf.transform([self.essay]),
                            EssayScorer.scaler.transform(lf)),
                            axis = 1)
        return EssayScorer.clf.predict(X)[0]

    def __spell_check(self):
        res = {}
        for w in self.words:
            if EssayScorer.d.check(w) is False:
                res[w] = EssayScorer.d.suggest(w)[:2]
        return json.dumps(res)

    def __grammar_check(self):
        res = []
        errors = EssayScorer.t.check(self.essay)
        for e in errors:
            res.append(unicode(e))
        return json.dumps(res)

    def __coherence(self):
        return ""


if __name__ == "__main__":
    text = 'A sentence witj a error in the Hitchhiker\'s Guide tot he Galaxy'
    e = EssayScorer(text)
    print e.sents
    print e.words
    print e.spell_errors
    print e.grammar_errors
    print e.score