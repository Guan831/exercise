from operator import index
from gensim.models import LsiModel
from pprint import pprint
from gensim.models.nmf import Nmf
from gensim.similarities.docsim import MatrixSimilarity
from gensim.models import LdaModel
import ex07
import ex06
import ex05
import ex04
import ex03
import ex02
import ex01
import ex08
import gensim

# 9.4


def lsi_search(texts, query, num_topics):
    tfidf_model, dic, text_tfidf_weights = ex03.get_tfidmodel_and_weights(
        texts)

    lsi_model = LsiModel(corpus=text_tfidf_weights,
                         id2word=dic, num_topics=num_topics)
    lsi_weights = lsi_model[text_tfidf_weights]
    index = MatrixSimilarity(lsi_weights, num_features=len(dic))

    query_bows = ex03.get_bows([query], dic)

    query_tfidf_weights = ex03.get_weights(query_bows, dic, tfidf_model)
    query_lsi_weights = lsi_model[query_tfidf_weights]

    sims = index[query_lsi_weights[0]]
    return sorted(enumerate(sims), key=lambda x: x[1], reverse=True)

# 9.8


def nmf_search(texts, query, num_topics, passes=20, random_state=None):
    tfidf_model, dic, text_tfidf_weights = ex03.get_tfidmodel_and_weights(
        texts)

    nmf_model = Nmf(corpus=text_tfidf_weights, id2word=dic,
                    num_topics=num_topics, passes=passes, random_state=random_state)

    nmf_weights = nmf_model[text_tfidf_weights]

    index = MatrixSimilarity(nmf_weights, num_features=len(dic))

    query_bows = ex03.get_bows([query], dic)
    query_tfidf_weights = ex03.get_weights(query_bows, dic, tfidf_model)

    query_nmf_weights = nmf_model[query_tfidf_weights]

    sims = index[query_nmf_weights[0]]

    return sorted(enumerate(sims), key=lambda x: x[1], reverse=True)


# 9.14
def lda_search(texts, query, num_topics, passes=20, random_state=None):
    tfidf_model, dic, text_tfidf_weights = ex03.get_tfidmodel_and_weights(
        texts)

    lda_model = LdaModel(corpus=text_tfidf_weights, id2word=dic,
                         num_topics=num_topics, passes=passes, random_state=random_state)

    lda_weights = lda_model[text_tfidf_weights]
    index = MatrixSimilarity(lda_weights, num_features=len(dic))

    query_bows = ex03.get_bows([query], dic)
    query_tfidf_weights = ex03.get_weights(query_bows, dic, tfidf_model)
    query_lda_weights = lda_model[query_tfidf_weights]

    sims = index[query_lda_weights[0]]

    return sorted(enumerate(sims), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':

    # 9.1
    book_texts = [ex02.get_string_form_file(
        'data/ch05/%d.txt' % i)for i in range(10)]
    tfidf_model, dic, tfidf_weights = ex03.get_tfidmodel_and_weights(
        book_texts)
    '''
    #9.2
    num_topics = 5
    lsi_model = LsiModel(corpus=tfidf_weights,
                         id2word=dic, num_topics=num_topics)
    #9.3
    print(lsi_model.print_topic(0, 3))
    
    #tfidf_weights=tfidf_model[bows]
    #lsi_weights=lsi_model[tfidf_weights]
    '''
    # 9.5
    query = '人工知能'

    tfidf_result = ex04.vsm_search(book_texts, query)
    # pprint(tfidf_result)
    # 9.6
    num_topics = 5
    lsi_result = lsi_search(book_texts, query, num_topics)
    # pprint(lsi_result)
    ''''''
    # 9.7
    right_answer = [0, 1, 0, 1, 0, 1, 0, 0, 1, 1]
    tfidf_ranking = [x[0] for x in tfidf_result]
    '''
    lsi_ranking = [x[0] for x in lsi_result]
    print('TFIDF:%.4f' % ex05.get_average_precision(tfidf_ranking, right_answer))
    print('LSI  :%.4f' % ex05.get_average_precision(lsi_ranking, right_answer))
    '''
    # 9.9
    '''
    num_topics = 5
    nmf_result = nmf_search(book_texts, query, num_topics, random_state=7)

    # pprint(nmf_result)
    # 9.10
    nmf_ranking = [x[0] for x in nmf_result]
    #print('%.4f' % ex05.get_average_precision(nmf_ranking, right_answer))
    # 9.11
    lda_model = LdaModel(corpus=tfidf_weights, id2word=dic,
                         num_topics=5, passes=20, random_state=6)

    # 9.12
    lda_weights = lda_model[tfidf_weights]
    # print(book_texts[1])
    # pprint(lda_weights[1])

    # 9.13
    #print(lda_model.print_topic(0, 4))

    # 9.15
    num_topics = 5

    lda_result = lda_search(book_texts, query, num_topics, random_state=6)
    lda_ranking = tuple(x[0] for x in lda_result)

    #print('%.4f' % ex05.get_average_precision(lda_ranking, right_answer))
    '''
    # 9.16
    num_topics = 5
    num_trials = 5
    sum_of_ap = 0.0
    for i in range(num_topics):
        lda_result = lda_search(book_texts, query, num_topics)
        lda_ranking = tuple(x[0]for x in lda_result)
        ap = ex05.get_average_precision(lda_ranking, right_answer)
        print('%d:%.4f' % (i, ap))
        sum_of_ap += ap

    print('AVG:%.4f' % (sum_of_ap/num_trials))
