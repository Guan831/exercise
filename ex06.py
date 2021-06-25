from ex05 import *
from gensim import matutils
from sklearn.cluster import KMeans
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import average, linkage, dendrogram
from scipy.cluster.hierarchy import fcluster
import matplotlib.font_manager as fm
from scipy.cluster.hierarchy import cophenet


if __name__ == '__main__':
    # 6.1
    book_texts = [get_string_form_file(
        'data/ch06/%d.txt' % i)for i in range(12)]
    tfidf_model, dic, vectors = get_tfidmodel_and_weights(book_texts)
    titles = get_list_from_file('data/ch06/book-titles.txt')

    # 6.2

    dense_vectors = matutils.corpus2dense(vectors, len(dic)).T
    K = 4
    result = KMeans(n_clusters=K).fit(dense_vectors)
    '''
    for label in range(K):
        print([titles[i] for i in np.where(result.labels_ == label)[0]])
    '''

    # 6.3
    data = [[1, 3], [2, 2], [2.5, 5], [5.5, 8.5], [6, 8]]

    xlist = [x[0]for x in data]
    ylist = [x[1]for x in data]

    plt.xlim(0.5, 6.5)
    plt.ylim(1.5, 9.5)
    plt.scatter(xlist, ylist)

    delta = 0.1
    for i, (x, y) in enumerate(zip(xlist, ylist)):
        plt.annotate(str(i), (x+delta, y+delta))
    # plt.show()
    # 6.4
    d = pdist(data)
    L = linkage(d, method='average')
    threshold = 4
    #dendrogram(L, orientation='left', color_threshold=threshold)
    # 6.5
    '''
    f = fcluster(L, threshold, criterion='distance')
    for i, j in enumerate(f):
        print('data[%d]:cluster %d' % (i, j))
    '''
    # 6.6

    configure_fonts_for_japanese()
    d = pdist(dense_vectors)
    #L = linkage(d, method='ward')
    #dendrogram(L, labels=titles, color_threshold=1.4, orientation='left')
    # plt.show()

    # 6.7
    '''
    L = linkage(d, method='average')
    dendrogram(L, labels=titles, color_threshold=1.38, orientation='left')
    plt.show()
    '''

    # 6.8
    d = pdist(dense_vectors)
    methods = ['average', 'centroid', 'complete',
               'median', 'single', 'ward', 'weighted']

    for m in methods:
        L = linkage(d, method=m)
        c = cophenet(L, d)
        print('%s\t%7.4f' % (m, c[0]))
