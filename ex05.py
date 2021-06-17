import matplotlib
from numpy import may_share_memory
from numpy.lib.function_base import percentile
from ex04 import *
from pprint import pprint
from sklearn.metrics import precision_score,recall_score,f1_score
import matplotlib.pyplot as plt
#5.3
def select_by_threshold(r,threchold):
    answer=[0]*len(r)
    for i in r :
        if  i[1]>threchold: answer[i[0]]=1
    return answer

#5.5
def print_scores(right_answer,my_answer):
    print('precision %.4f'%precision_score(right_answer,my_answer))
    print('recall    %.4f'%recall_score(right_answer,my_answer))
    print('f-measure %.4f'%f1_score(right_answer,my_answer))

#5.12
def top_n(r,n):
    answer=[0]*len(r)
    for i in range(n):
        answer[r[i]]=1
    return answer

#5.14
def get_pr_curve(ranking,answer):
    precision =[1]
    recall=[0]
    for i in range (1,len(ranking)+1):
        x=top_n(ranking,i)
        precision.append(precision_score(answer,x))
        recall.append(recall_score(answer,x))
    return precision,recall

#5.15
def draw_pr_curve(ranking,answer):
    precision,recall = get_pr_curve(ranking,answer)
    plt.xlim(-0.05,1.05)
    plt.ylim(0.0,1.1)

    plt.xlabel('recall')
    plt.ylabel('precision')

    plt.fill_between(recall,precision,0,facecolor='#FFFFCC')
    plt.plot(recall,precision,'o-')
    plt.show()

#5.18
def get_average_precision(ranking,answer):
    precision,recall=get_pr_curve(ranking,answer)
    ap=0.0

    for i in range(1,len(precision)):
        ap+= (recall[i]-recall[i-1])*(precision[i-1]+precision[i])/2.0
    return ap

if __name__ == '__main__':
    #5.1
    right_answer=[0,1,0,1,0,1,0,0,1,1]
    
    #5.2
    book_texts=[get_string_form_file('data/ch05/%d.txt'%i) for i in range(10)]
    query='人工知能'
    
    result=vsm_search(book_texts,query)
    #pprint(result)
    '''
    #5.4
    my_answer=select_by_threshold(result,threchold=0)
    print('right_awswer={}'.format(right_answer))
    print('My_answer={}'.format(my_answer))
    
    #5.6
    print_scores(right_answer,my_answer)
    
    #5.7
    my_answer=select_by_threshold(result,threchold=0.3)
    print('my_answer={}'.format(my_answer))
    print_scores(right_answer,my_answer)
    '''
    #5.8
    #print(get_words(query))
    #5.9
    my_ranking=tuple(x[0] for x in result)
    #print(my_ranking)
    #5.10
    #print(''.join([str(right_answer[i])for i in my_ranking]))

    #5.11
    
    matching=[i for i,x in enumerate (right_answer) if x==1]
    non_matching=[i for i, x in enumerate(right_answer) if x== 0]
    good_ranking=tuple(matching+non_matching)
    #print(good_ranking)
    #print(''.join([str(right_answer[i])for i in good_ranking]))
    
    #5.13
    '''
    n=2
    my_answer_n=top_n(my_ranking,n)
    print(my_answer_n)
    print(recall_score(right_answer,my_answer_n))
    print(precision_score(right_answer,my_answer_n))
    '''
    #5.16
    #draw_pr_curve(my_ranking,right_answer)
    #5.17
    #draw_pr_curve(good_ranking,right_answer)

    #5.19
    print('my_ranking    %.4f'%get_average_precision(my_ranking,right_answer))
    print('good_ranking  %.4f'%get_average_precision(good_ranking,right_answer))



    




    
