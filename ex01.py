from io import StringIO
import re
from collections import Counter
from typing import Pattern
import chardet

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

if __name__ == '__main__':
  ''' 1.1'''
  query = '京都'
  s1 = '清水寺在京都'
  s2 = '浅草寺在东京'
  print(query in s1)
  print(query in s2)
  ''' '''
  '''1.2
  print(check_query('清水寺在京都','京都'))
  print(check_query('浅草寺在东京', '京都'))
  '''
  '''1.3
  print(check_query('venv/data/ch01/01.txt', '京都'))
  '''
  '''1.4
  query = '京都'
  file_list = ['data/ch01/%02d.txt' % x for x in (1, 2, 3, 4)]
  for f in file_list:
    r = check_query(f, query)
    print('{} in {}...{}'.format(query, f, r))
  '''
  '''1.5
  print(list('a'.encode()))
  print(list('abc'.encode()))
  '''
  '''1.6
  print(list('京'.encode("EUC-JP")))
  print(list('京'.encode("Shift-JIS")))
  print(list('京'.encode("UTF-8")))
  '''
  '''1.7
  print(chardet.detect('明日，京都に行きます'.encode('EUC-JP')))
  '''
  '''1.8
  print(chardet.detect('京'.encode('EUC-JP')))
  '''
  '''1.11
  file_list = ['data/ch01/%02d.txt' % x for x in (1, 2, 3, 4)]
  query = '京都'
  for f in file_list:
    r =chenck_encoding_and_query(f,query)
    print('{} in {}...{}'.format(query, f, r))
  '''
  '''1.12
  string = '情报检索'
  print(get_ngram(string,N=1))
  print(get_ngram(string,N=2))
  '''
  '''1.14
  print(get_most_common_ngram('data/ch01/melos.txt',N=3,k=5))
  print(get_most_common_ngram('data/ch01/album.txt',N=3,k=5))
  '''
  '''1.15
  string = 'やっぱり『つぶ餡』が好き'
  pattern = '『.*』'
  result=re.search(pattern,string)
  print(result.group(0))
  '''
  '''1.16
  string = 'やっぱり『つぶ餡』が好き'
  pattern = '『(.*)』'
  result=re.search(pattern,string)
  print(result.group(1))
  '''
  '''1.17
  string = 'やっぱり『つぶ餡』が好き'
  pattern = '『((..).*)』'
  result=re.search(pattern,string)
  print(result.group(1))
  print(result.group(2))
  '''
  '''1.18
  string='このばたもちはとてももちもちしている'
  pattern=r'(..)\1'
  result=re.search(pattern,string)
  print(result.group(0))
  '''
  '''1.19
  string='『つぶ餡』にするか『こし餡』にするか'
  pattern='『(.*)』'
  result=re.search(pattern,string)
  print(result.group(1))
  '''
  '''1.20
  string='『つぶ餡』にするか『こし餡』にするか'
  pattern='『(.*?)』'
  result=re.search(pattern,string)
  print(result.group(1))
  '''
  '''1.21
  string='『つぶ餡』にするか『こし餡』にするか'
  pattern='『(.*?)』'
  result=re.findall(pattern,string)
  print(result)
  '''
  '''1.23
  query='京都'
  filr_list=['data/ch01/%02d.txt'%x for x in (1,2,3,4)]
  for f in filr_list:
    print(f,get_snippet_form_filr(f,query,width=6))
  '''
