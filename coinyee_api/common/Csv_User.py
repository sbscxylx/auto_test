# encoding='utf-8'
import csv
import codecs
from itertools import islice

#读取本地csv文件
data = csv.reader(codecs.open('./test_data/user_info.csv', 'r', 'utf-8'))

#存放用户数据
user_data = []

#循环输出每行信息
for line in islice(data, 1, None):
    user_data.append(line)

