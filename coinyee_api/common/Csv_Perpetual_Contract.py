# encoding='utf-8'
import csv
import codecs
from itertools import islice

#读取本地csv文件
data = csv.reader(codecs.open('./test_data/perpetual_contract.csv', 'r', 'utf-8'))

#存放用户数据
perpetual_contract_apis = []

#循环输出每行信息
for line in islice(data, 1, None):
    perpetual_contract_apis.append(line)

