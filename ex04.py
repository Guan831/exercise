import warnings
from gensim.corpora import dictionary
from gensim.similarities.docsim import query_shard
warnings.filterwarnings('ignore')
from matplotlib.pyplot import title
from ex01 import *
from ex02 import *
from ex03 import *
from gensim import corpora,models
from gensim.similarities import MatrixSimilarity
#4.1
def jaccard(X,Y):
    x=set(X)
    y=set(Y)
    a=len(x.intersection(y))
    b=len(x.union(y))
    if b==0:
        return 0
    else:
        return a/b

#4.4
def vsm_search(texts,query):
    tfidf_model,dic,text_weights =get_tfidmodel_and_weights(texts)
    index =MatrixSimilarity(text_weights,num_features=len(dic))

    query_bows=get_bows([query],dic)
    query_weights=get_weights(query_bows,dic,tfidf_model)
    sims=index[query_weights[0]]

    return sorted(enumerate(sims),key=lambda x:x[1],reverse=True)
def vsm_text(texts,query):
    tfidf_model, dic, text_weights = get_tfidmodel_and_weights(texts)
    index = MatrixSimilarity(text_weights, num_features=len(dic))
    query_bows = get_bows([query], dic)
    query_weights = get_weights(query_bows, dic, tfidf_model)
    sims = index[query_weights[0]]
    return sorted(enumerate(sims), key=lambda x: x[1], reverse=True)


def get_list_from_file(file_name):
    with open(file_name,'r',encoding='UTF-8')as f:
        return f.read().split()


if __name__ == '__main__':
    '''4.2
    book_texts=[get_string_form_file('data/ch04/%d.txt' %i ) for i in range(10)]

    tfidf_model , dic , book_weights =get_tfidmodel_and_weights(book_texts)
    keyword_lists=[[x[0]for x in w[:10]] for w in book_weights]
    results=[(x,jaccard(keyword_lists[9],keyword_lists[x]))for x in range(9)]
    results.sort(key=lambda x:x[1],reverse=True)

    results.sort(key=lambda x:x[1],reverse=True)

    with open('data/ch04/book-titles.txt',encoding='UTF-8') as f:
        titles = f.read().strip().split('\n')
    
    for x in range(9):
        print('%s %.4f'%(titles[results[x][0]],results[x][1]))
    '''
    '''4.3
    texts=['花より団子。とにかく団子','みたらしよりあんこ']
    words=[get_words(text,keep_pos=['名詞'])for text in texts]
    dic = corpora.Dictionary(words)

    for i in range(len(dic)):
        print('dic[%d]=%s'%(i,dic[i]))
    
    bows=[dic.doc2bow(w) for w in words]
    tfidf=models.TfidfModel(bows)
    weights= tfidf[bows[0]]
    weights=[(i,round(j,4))for i,j in weights]
    print('weights=',weights)
    '''
    '''4.5
    book_texts=[get_string_form_file('data/ch04/%d.txt'%i ) for i in range(10)]
    titles=get_list_from_file('data/ch04/book-titles.txt')
    result=vsm_search(book_texts[:-1],book_texts[9])
    for x in range(9):
        print ('%s %.4f'%(titles[result[x][0]],result[x][1]))
    '''
    '''4.6
    texts= [get_string_form_file('data/ch04/%d.txt'%i) for i in range(10)]
    titles=get_list_from_file('data/ch04/book-titles.txt')
    query='数学'
    result=vsm_search(texts,query)
    for x in range(len(result)):
        print ('%s %.4f'%(titles[result[x][0]],result[x][1]))
    '''
    

