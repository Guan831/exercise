from io import IncrementalNewlineDecoder
from io import StringIO
import re
from collections import Counter
from typing import Pattern
import chardet
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from janome.analyzer import Analyzer
from janome.tokenfilter import ExtractAttributeFilter, POSStopFilter
from janome.tokenfilter import POSKeepFilter
import matplotlib.font_manager as fm
from matplotlib import rcParams
from collections import Counter
import matplotlib.pyplot as plt

#%matplotlib inline


def check_query(filename, query):
    with open(filename, 'r', encoding='UTF-8')as f:
        s = f.read()
        return query in s

#1.9
def get_string_form_file(filename):
    with open(filename, 'rb') as f :
      d=f.read()
      e = chardet.detect(d)['encoding']
      if e == None:
        e='UTF-8'
      return d.decode(e)

#1.10
def chenck_encoding_and_query(filename,query):
  s= get_string_form_file(filename)
  return query in s

#1.11
def get_ngram(string , N=1):
  return [string[i:i+N] for i in range(len(string)-N+1) ]

#1.13
def get_most_common_ngram(filename,N=1,k=1):
  s=get_string_form_file(filename)
  return Counter(get_ngram(s,N=N)).most_common(k)

#1.22
def get_snippet_form_filr(filrname,query,width=2):
  s=get_string_form_file(filrname)
  p='.{0,%d}%s.{0,%d}'%(width,query,width)
  r=re.search(p,s)
  if r:
    return r.group(0)
  else:
    return None
#2.6
def get_m_snippet_from_filr(filename,query,width=3):
  t=Tokenizer(wakati=True)
  qlist=list(t.tokenize(query))
  qlen=len(qlist)
  s=get_string_form_file(filename)
  slist=list(t.tokenize(s))
  for i in [k for k,v in enumerate(slist)if v==qlist[0]]:
    if qlist ==slist[i:i +qlen]:
      return ''.join(slist[max(0,i - width):i+ width + qlen])
  return None
#2.8
def creat_wordcloud(frequencies,font,width=600,height=400):
  wordcloud= WordCloud(background_color='white' , font_path=font,width=width,height=height)
  plt.figure(figsize=(width/50,height/50))
  plt.imshow(wordcloud.generate_from_frequencies(frequencies))
  plt.axis('off')
  plt.show()
#2.9
def get_words(s):
  a= Analyzer(token_filters=[POSStopFilter(['記号']),ExtractAttributeFilter('surface')])
  return list(a.analyze(s))
def get_words_from_file(f):
  return get_words(get_string_form_file(f))
#2.10
japanese_font_candidates=['Hiragino Maru Gothic Pro','Yu Gothic','Arial Unicods MS','Meirio','Takao',
                          'IPAexGothic','IPAPGothic','VL PGothic', 'Noto Sans CJK JP']
def get_japanese_fonts(candidates=japanese_font_candidates):
  fonts=[]
  for f in fm.findSystemFonts():
    p=fm.FontProperties(fname=f)
    try:
      n=p.get_name()
      if n in candidates:
        fonts.append(f)
    except RuntimeError:
      pass
  fonts.append('font/ipaexg.ttf')
  return fonts
def configure_fonts_for_japanese(fonts=japanese_font_candidates):
  if hasattr(fm.FontManager,'addfont'):
    fm.FontManager.addfont('font/ipaexg.ttf')
  else:
    ipa_font_files= fm.findSystemFonts(fontpaths='font')
    ipa_font_list=fm.createFontList(ipa_font_files)
    fm.FontManager.ttflist.extend(ipa_font_list)
  rcParams['font.family']='sans-serif'
  rcParams['font.sans-serif']=fonts
#2.12
def plot_frequency(count,log_scale=False):
  y= list (sorted (count.values(),reverse=True))
  x=range(1,len(y)+1)
  if log_scale:
    plt.loglog(x,y)
  else:
    plt.plot(x,y)

if __name__ == '__main__':
  '''2.1
  string = get_string_form_file('data/ch02/alice.txt')
  tokens = re.split('[ \n\.]+',string)
   for t in tokens[:10]:
       print(t)
  '''
  '''2.2
  tokenizer = Tokenizer()
  string='すもももももももものうち'
  for t in tokenizer.tokenize(string):
   print('{}\t{}'.format(t.surface, t.part_of_speech))
  '''
  '''2.3
  string='すもももももももものうち'
  tokenizer=Tokenizer(wakati=True)
  print(list(tokenizer.tokenize(string)))# =tokenize(string,wakati=Ture)
  '''
  '''2.4
  string ='ふなっしーはかわいい'
  tokenizer = Tokenizer()
  for t in tokenizer.tokenize(string):
    print('{}\t{}'.format(t.surface,t.part_of_speech))
  '''
  '''2.5
  string ='ふなっしーはかわいい'
  tokenizer = Tokenizer('data/ch02/userdic.csv',udic_type='simpledic')
  for t in tokenizer.tokenize(string):
    print('{}\t{}'.format(t.surface,t.part_of_speech))
  '''
  '''2.7
  #query='京都'
  query='東京都'
  file_list=['data/ch01/%02d.txt'%x for x in (1,2,3,4)]
  for f in file_list:
    print(f,get_m_snippet_from_filr(f,query))
  ''' 
  '''2.11
  string =get_string_form_file('data/ch01/melos.txt')
  words=get_words(string)
  count=Counter(words)
  font=get_japanese_fonts()[0]
  creat_wordcloud(count,font)
  '''
  plot_frequency(Counter(get_words(get_string_form_file('data/ch01/melos.txt'))))