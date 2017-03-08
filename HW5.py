import json
import re

class Word:
    def __init__(self, **kwargs):
        vars(self).update(kwargs)

    def __repr__(self):
        return str(vars(self))
    
    
def make_list(words_dicts):
    words = []
    for i in words_dicts:
        word = {}
        word['wordform'] = i['text']
        word['analyses'] = len(i['analysis'])
        if i['analysis']:
            word['lemma'] = i['analysis'][0]['lex']
            word['word_class'] = re.findall('^([A-Z]+)[=,]', i['analysis'][0]['gr'])[0]
        words.append(Word(**word))
        print(Word(**word))


words_dicts = []
words_json = open('python_mystem.json','r',encoding='utf-8')
for line in words_json:
    line = json.loads(line)
    if line not in words_dicts and line['text'] != '\\s' and \
       re.search('\\w+',line['text']) is not None:
        words_dicts.append(line)
make_list(words_dicts)
