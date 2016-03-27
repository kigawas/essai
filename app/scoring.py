# encoding: utf-8
import enchant
import language_check
from nltk import sent_tokenize, word_tokenize
import json
import cPickle as pickle

class EssayScorer(object):
    d = enchant.Dict('en-US')
    t = language_check.LanguageTool('en-US')
    t.disable_spellchecking()
    
    def __init__(self, essay):
        self.essay = essay
        self.sents = [word_tokenize(sent) for sent in sent_tokenize(essay)]
        self.words = filter(lambda x:x.isalnum(), sum(self.sents, []))
        self.score = self.__score()
        self.spell_errors = self.__spell_check()
        self.grammar_errors = self.__grammar_check()
        self.coherence = self.__coherence()
    
    def __score(self):
        return 0
    
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
    e = EssayScorer('A sentence witj a error in the Hitchhiker\'s Guide tot he Galaxy')
    print e.sents
    print e.words
    print e.spell_errors
    print e.grammar_errors