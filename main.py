# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
def check_query(filename, query):
    with open(filename, 'r', encoding='UTF-8')as f:
        s = f.read()
        return query in s

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
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
