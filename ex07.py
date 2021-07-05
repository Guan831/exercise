from ex04 import get_list_from_file
from ex03 import get_bows, get_tfidmodel_and_weights, get_weights
from ex01 import get_string_form_file
import ex06
from gensim import matutils
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV

if __name__ == '__main__':
    '''
    # 7.1
    book_texts = [get_string_form_file(
        'data/ch07/%d.txt' % i)for i in range(15)]
    tfidf_model, dic, vectors = get_tfidmodel_and_weights(book_texts)

    vectors = matutils.corpus2dense(vectors, len(dic)).T
    titles = get_list_from_file('data/ch07/book-titles.txt')
    classes = get_list_from_file('data/ch07/class.txt')

    # 7.2
    mnb = MultinomialNB()
    mnb.fit(vectors, classes)
    # 7.3
    test_texts = ['Pythonで実装',
                  '微分方程式を解く',
                  '規格に準拠',
                  'アナログからデジタルへ',
                  '人工知能']

    test_bow = get_bows(test_texts, dic)
    test_vectors = get_weights(test_bow, dic, tfidf_model)
    test_vectors = matutils.corpus2dense(test_vectors, len(dic)).T

    predicted_classed = mnb.predict(test_vectors)

#    for i, j in zip(test_texts, predicted_classed):
#        print('{}:{}'.format(i, j))
    '''

    # 7.4
    cv_texts = [get_string_form_file(
        'data/ch07/cv/%d.txt' % i)for i in range(90)]
    tfidf_model, dic, vectors = get_tfidmodel_and_weights(cv_texts)
    vectors = matutils.corpus2dense(vectors, len(dic)).T

    classes = get_list_from_file('data/ch07/cv/class.txt')
    K = 3
    skf = StratifiedKFold(n_splits=K)

    '''
    #7.5
    K = 3
    skf = StratifiedKFold(n_splits=K)

    classifier = MultinomialNB()
    scores = cross_val_score(classifier, vectors, classes, cv=skf)

    for i in range(K):
        print(' Test %d/%d:/t%.4f' % (i+1, K, scores[i]))

        #print(f'Test {i+1}/{K}:\t{scores[i]:.4f}')
    print('Average:\t%.4f' % (sum(scores)/K))

    '''
    '''
    # 7.6
    K = 3
    skf = StratifiedKFold(n_splits=K)

    classifier = svm.SVC(kernel='rbf', C=1, gamma=1)

    scores = cross_val_score(classifier, vectors, classes, cv=skf)

    for i in range(K):
        print('Test %d/%d:\t%.4f' % (i+1, K, scores[1]))
    print('Average:\t%.4f' % (sum(scores)/K))
    '''
    '''
    # 7.7
    classifier = svm.SVC(kernel='rbf', C=1, gamma=1)

    prediction = cross_val_predict(classifier, vectors, classes, cv=skf)

    cm = confusion_matrix(classes, prediction)

    class_names = [j for i, j in enumerate(classes)if not j in classes[:i]]

    fmt = '%2d\t'*6

    for i, j in enumerate(cm):
        print(fmt % tuple(j), class_names[i])
    '''
    # 7.8
    params = {
        'kernel': ['rbf'],
        'C': [0.1, 1, 10, 100],
        'gamma': [0.1, 1, 10, 100]
    }
    classifier = svm.SVC()

    gs = GridSearchCV(classifier, params, cv=3)
    gs.fit(vectors, classes)

    print(gs.best_params_)
