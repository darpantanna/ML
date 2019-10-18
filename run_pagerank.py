import sys
import json
from scipy.sparse.linalg import eigs
import numpy as np

with open("adj_list.json") as adj_list:
    adj = json.load(adj_list)

with open("url_dict.json") as url_dict:
    url = json.load(url_dict)

with open("url_dict_reverse.json") as url_reverse:
    urlR = json.load(url_reverse)


num=0
for i in url:
    num += 1

matrix = [[0 for x in range(num)] for y in range(num)]
for i in adj:
    for j in adj[i]:
        if(int(i) != int(j)):
            matrix[int(i)][int(j)] = 1


flag=0
for i in range(len(matrix)):
    flag = 0
    for j in range(len(matrix[i])):
        if(matrix[i][j] != 0):
            flag = 1

    if flag == 0:
        for k in range(len(matrix[i])):
            if i != k:
                matrix[i][k] = 1

for j in range(len(matrix[0])):
    flag=0
    for i in range(len(matrix)):
        if(matrix[i][j] != 0):
            flag=1

    if flag==0:
        for k in range(len(matrix)):
            if i != k:
                matrix[k][j] = 1

count = 0
for i in range(len(matrix)):
    count = 0
    for j in range(len(matrix[i])):
        if matrix[i][j] == 1:
            count = count + 1

    for k in range(len(matrix[i])):
        if matrix[i][k] == 1:
            matrix[i][k] = matrix[i][k]/(count*1.0)


def calc(matrix):
    val, vec = eigs(np.array(matrix).T, k=1)
    v = np.matrix(vec) / sum(vec)
    p = np.real(v)

    return p

ans = calc(matrix)
'''
class Website(object):
    url=''
    rank=0.0

    def _init_ (self, urlR):
        for k,v in urlR.items():
            setattr(self, k,v)
    
    web = []
    for url in range(len(urlR)):
        web = [url, urlR[string(url)]

'''
sorted(urlR.items())
sorted(url.keys())

result = zip(urlR, url, ans)
result.sort(key=lambda t:t[2])


for i in range(len(result)):
    res1 = result[i][1]
    res2 = result[i][2]
    print res1
    print res2
