from typing import Text

from gensim.similarities.docsim import MatrixSimilarity
import ex07
import ex06
import ex05
import ex04
import ex03
import ex02
import ex01
from pprint import pprint
# 8.2


def add_weights(dic, vec, weight=1.0):
    for (id, val) in vec:
        if not id in dic:
            dic[id] = 0
        dic[id] += weight*val


def Rocchio(query_vec, R_plus_vecs, R_minus_vecs,
            alpha=1.0, beta=0.75, gamma=0.15):
    q = {id: alpha*val for (id, val) in query_vec}
    n = len(R_plus_vecs)
    if n > 0:
        w = beta/n
        for v in R_plus_vecs:
            add_weights(q, v, weight=w)
        n = len(R_minus_vecs)
    if n > 0:
        w = -gamma/n
        for v in R_minus_vecs:
            add_weights(q, v, weight=w)
    return list(q.items())

# 8.3


def vsm_seach_with_feedback(texts, query, R_plus, R_minus):
    tfidf_model, dic, text_weights = ex03.get_tfidmodel_and_weights(texts)
    index = MatrixSimilarity(text_weights, num_features=len(dic))

    query_bows = ex03.get_bows([query], dic)

    query_weights = ex03.get_weights(query_bows, dic, tfidf_model)

    R_plus_vecs = [text_weights[i] for i in R_plus]
    R_minus_vecs = [text_weights[i] for i in R_minus]

    feedback_query = Rocchio(query_weights[0], R_plus_vecs, R_minus_vecs)

    sims = index[feedback_query]

    return sorted(enumerate(sims), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    # 8.1

    texts = [ex01.get_string_form_file(
        'data/ch08/%d.txt' % i)for i in range(12)]
    titles = ex04.get_list_from_file('data/ch08/book-titles.txt')
    '''
    r = ex04.vsm_search(texts, '環境')

    pprint([(i, titles[i])for i, _ in r])
    '''
    # 8.2

    r = vsm_seach_with_feedback(texts, '環境', [6], [11])
    pprint([(i, titles[i]) for i, _ in r])
