# 这是一个示例 Python 脚本。
from io import StringIO
import re
from collections import Counter
import chardet

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
#1.2 1.3 
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
  
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
  '''1.1
    query = '京都'
    s1 = '清水寺在京都'
    s2 = '浅草寺在东京'
    print(query in s1)
    print(query in s2)
  '''
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


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
