from operator import index
from gensim.models import LsiModel
from pprint import pprint
from gensim.models.ldamulticore import worker_e_step
from gensim.models.nmf import Nmf
from gensim.similarities.docsim import MatrixSimilarity
from gensim.models import LdaModel
from gensim.models import Word2Vec
from gensim.utils import tokenize
from numpy import negative, positive
from numpy.core.fromnumeric import size
import ex07
import ex06
import ex05
import ex04
import ex03
import ex02
import ex01
import ex08
import ex09
import gensim
from gensim.models import KeyedVectors
from pprint import pprint
from gensim.models.doc2vec import TaggedDocument
from gensim.models.doc2vec import Doc2Vec
import pickle

# 10.11


def d2v_search(model, texts, query):
    docs = [ex02.get_words(text) if type(
        text) is str else text for text in texts]

    query_doc = ex02.get_words(query) if type(query) is str else query

    r = [(i, model.docvecs.similarity_unseen_doce(model, doc, query_doc, steps=50))
         for i, doc, in enumerate(docs)]

    return sorted(r, key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    # 10.1

    training_documents = ['年越しには天ぷら蕎麦をいただきます',
                          '関東では雑煮に鶏肉と小松菜に入れます']

    training_data = [ex02.get_words(d) for d in training_documents]
    '''
    print('training_data=', training_data)
    w2v_model = Word2Vec(training_data, vector_size=3,
                         window=2, sg=1, min_count=1)

    word = '蕎麦'
    print(word, '=', w2v_model.wv[word])
    '''
# 10.2 10.3
    word_vectors = KeyedVectors.load('data/ch10/w2v.kv')
    #pprint(word_vectors.most_similar(['酸素'], topn=5))
# 10.4
    '''
    print(word_vectors.most_similar(
        positive=['饂飩', 'イタリア'], negative=['日本'], topn=1))
    '''
# 10.5
    '''
    data = [[['饂飩', 'イタリア'], ['日本']],
            [['信長', '美濃'], ['尾張']],
            [['丸の内', '大阪'], ['東京']]]

    for p_words, n_words in data:
        top = word_vectors.most_similar(
            positive=p_words, negative=n_words, topn=1)

        answer = top[0][0]

        print('{}-{}+{}={}'.format(p_words[0], n_words[0], p_words[1], answer))
    '''
    # 10.6

    tagged_data = [TaggedDocument(words=d, tags=[i])
                   for i, d in enumerate(training_data)]
    '''
    pprint(tagged_data)
    '''
    # 10.7
    d2v_model = Doc2Vec(tagged_data, dm=1, vector_size=3,
                        window=2, min_count=1)
    # 10.8
    # print(d2v_model.docvecs[0])
    # 10.9

    model_file = 'data/jawiki.doc2vec.dmpv300d.model'
    d2v_wikipedia_model = Doc2Vec.load(model_file, mmap='r')

    # 10.10
    '''
    doc1 = ex02.get_words('Pythonを使うと自然言語処理が簡単にできる')
    doc2 = ex02.get_words('実データを用いた情報検索プログラミングは楽しい')
    print(f'doc1 = {doc1}')
    print(f'doc2 = {doc2}')

    sim = d2v_wikipedia_model.docvecs.similarity_unseen_docs(d2v_wikipedia_model,
                                                             doc1, doc2, steps=50)
    print('類似度：％４'％sim)
    '''
    # 10.12
    book_texts = [ex02.get_string_form_file(
        'data/ch05/%d.txt' % i) for i in range(10)]

    query = '人工知能'
    right_answer = [0, 1, 0, 1, 0, 1, 0, 0, 1, 1]

    result = d2v_search(d2v_wikipedia_model, book_texts, query)

    ranking = tuple([x[0]for x in result])
    print(ranking)
    print('%.4f' % ex05.get_average_precision(ranking, right_answer))

    # 10.13
    with open('data/ch10/tokenized.dat', 'rb')as f:
        tokenize_texts, tokenize_query = pickle.load

    result = d2v_search(d2v_wikipedia_model, tokenize_texts, tokenize_query)

    ranking = tuple(x[0] for x in result)
    print(ranking)
    print('%.4f' % ex05.get_average_precision(ranking, right_answer))
