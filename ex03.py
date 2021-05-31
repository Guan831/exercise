from sys import pycache_prefix
from janome.analyzer import Analyzer
from janome.tokenfilter import ExtractAttributeFilter
from janome.tokenfilter import POSStopFilter
from janome.tokenfilter import POSKeepFilter
import ex02

#3.3
def get_words(string,keep_pos=None):
    filters=[]
    if keep_pos is None:
        filters.append(POSStopFilter(['記号']))
    else :
        filters.append(POSKeepFilter(keep_pos))
    filters.append(ExtractAttributeFilter('surface'))
    a =Analyzer(token_filters=filters)
    return list(a.analyze(string))




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