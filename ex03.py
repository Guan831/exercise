from matplotlib.pyplot import text
from ex01 import get_string_form_file
from sys import pycache_prefix
from janome.analyzer import Analyzer
from janome.tokenfilter import ExtractAttributeFilter
from janome.tokenfilter import POSStopFilter
from janome.tokenfilter import POSKeepFilter
from ex02 import *
from ex01 import *
from pprint import pprint
from gensim import models, corpora
import copy
from collections import Counter

# 3.3


def get_words(string, keep_pos=None):
    filters = []
    if keep_pos is None:
        filters.append(POSStopFilter(['記号']))
    else:
        filters.append(POSKeepFilter(keep_pos))
    filters.append(ExtractAttributeFilter('surface'))
    a = Analyzer(token_filters=filters)
    return list(a.analyze(string))
# 3.9


def build_corpus(file_list, dic_file=None, courpus_file=None):
    docs = []
    for f in file_list:
        text = get_string_form_file(f)
        words = get_words(text, keep_pos=['名詞'])
        docs.append(words)

        print(f)
    dic = corpora.Dictionary(docs)
    if not (dic_file is None):
        dic.save(dic_file)
    bows = [dic.doc2bow(d) for d in docs]
    if not (courpus_file is None):
        corpora.MmCorpus.serialize(courpus_file, bows)
    return dic, bows
# 3.10


def bows_to_cfs(bows):
    cfs = dict()
    for b in bows:
        for id, f in b:
            if not id in cfs:
                cfs[id] = 0
            cfs[id] += int(f)
    return cfs


def load_dictionaty_any_corpus(dic_file, corpus_file):
    dic = corpora.Dictionary.load(dic_file)
    bows = list(corpora.MmCorpus(corpus_file))
    if not hasattr(dic, 'cfs'):
        dic.cfs = bows_to_cfs(bows)
    return dic, bows
# 3.12


def load_aozora_corpus():
    return load_dictionaty_any_corpus('data/aozora/aozora.dic', 'data/aozora/aozora.mm')


def get_bows(texts, dic, allow_update=False):
    bows = []
    for text in texts:
        words = get_words(text, keep_pos=['名詞'])
        bow = dic.doc2bow(words, allow_update=allow_update)
        bows.append(bow)
    return bows


def add_to_corpus(texts, dic, bows, replicate=False):
    if replicate:
        dic = copy.copy(dic)
        bows = copy.copy(bows)
    texts_bows = get_bows(texts, dic, allow_update=True)
    bows.extend(texts_bows)
    return dic, bows, texts_bows

# 3.13


def get_weights(bows, dic, tfidf_model, surface=False, N=1000):
    weights = tfidf_model[bows]
    weihgts = [sorted(w, key=lambda x:x[1], reverse=True)[:N] for w in weights]
    if surface:
        return [[(dic[x[0]], x[1]) for x in w]for w in weights]
    else:
        return weights
# 3.15


def translate_bows(bows, table):
    return [[tuple([table[j[0]], j[1]]) for j in i if j[0] in table]for i in bows]


def get_tfidmodel_and_weights(texts, use_aozora=True, pos=['名詞']):
    if use_aozora:
        dic, bows = load_aozora_corpus()
    else:
        dic = corpora.Dictionary()
        bows = []
    text_docs = [get_words(text, keep_pos=pos)for text in texts]
    text_bows = [dic.doc2bow(d, allow_update=True) for d in text_docs]
    bows.extend(text_bows)

    text_ids = list(set([text_bows[i][j][0] for i in range(len(text_bows))
                         for j in range(len(text_bows[i]))]))

    text_tokens = [dic[i] for i in text_ids]
    dic.filter_tokens(good_ids=text_ids)

    id2id = dict()
    for i in range(len(text_ids)):
        id2id[text_ids[i]] = dic.token2id[text_tokens[i]]

    bows = translate_bows(bows, id2id)
    text_bows = translate_bows(text_bows, id2id)

    tfidf_model = models.TfidfModel(bows, normalize=True)

    text_weights = get_weights(text_bows, dic, tfidf_model)
    return tfidf_model, dic, text_weights


if __name__ == '__main__':
    '''3.1
    string='京都とは違う奈良の魅力'
    stop_pos=['助詞','助動詞','記号']
    analyzer= Analyzer(token_filters=[POSStopFilter(stop_pos),ExtractAttributeFilter('surface')])
    print(list(analyzer.analyze(string)))
    '''
    '''3.2
    string='京都とは違う奈良の魅力'
    keep_pos=['名詞']
    analyzer=Analyzer(token_filters=[POSKeepFilter(keep_pos),ExtractAttributeFilter('surface')])
    print(list(analyzer.analyze(string)))
    '''
    '''3.3-2.11
    string =ex02.get_string_form_file('data/ch01/melos.txt')
    words=get_words(string,keep_pos=['名詞'])
    count=ex02.Counter(words)
    font=ex02.get_japanese_fonts()[0]
    ex02.creat_wordcloud(count,font)
    '''
    '''3.4 3.5 3.6 3.7 3.8 3.11
    #3.4
    D=['data/ch03/1.txt','data/ch03/2.txt']
    texts=[get_string_form_file(x) for x in D]
    #pprint(texts,width=40)
    #3.5
    doce= [get_words(x,keep_pos=['名詞'])for x in texts]
    #pprint(doce,width=40)
    #3.6
    dictionary = corpora.Dictionary(doce)
    for k ,v in dictionary.items():
        print(k,v)
    #3.7
    i=2
    s='花粉'
    print('ID={}の語は「{}」'.format(i,dictionary[i]))
    print('「{}」のIDは{}'.format(s,dictionary.token2id['花粉']))
    #3.8
    bows=[dictionary.doc2bow(d) for d in doce]
    #pprint(bows)
    #3.11
    tfidf_model= models.TfidfModel(bows,normalize= False)
    weights=tfidf_model[bows[1]]
    print(weights)
    '''
    '''3.14
    dic,bows=load_aozora_corpus()
    melos_text=get_string_form_file('data/ch01/melos.txt')
    dic,bows,melos_bows=add_to_corpus([melos_text],dic,bows)
    tfidf_model=models.TfidfModel(bows,normalize=True)
    weights=get_weights(melos_bows,dic,tfidf_model,surface=True)
    count=dict(weights[0])
    font=get_japanese_fonts()[0]
    creat_wordcloud(count,font)
    '''
