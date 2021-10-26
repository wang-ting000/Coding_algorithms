import numpy as np

import copy


'''

# 去掉二进制表示中的'0b'
start = x2.find('b')
x2 = x2[start + 1:]
x2 = list(x2)
while len(x2) < 8:
    x2.insert(0, '0')

res = np.zeros((4, 8)).tolist()  # 8*4，每行储存的是一个位数的GF乘法结果
r = [0] * len(x1)

ll = len(x2)
for k in range(len(x1)):  # K是1110的第k位
    if x1[k] == '1':  # '1110' 一次移位
        for n in range(8):  # n是跟x2乘法的第n位
            if n <= ll - 4 + k:
                res[k][n] = x2[n + ll - 5 - k]  # 完成移位运算
            else:
                res[k][n] = '0'
        r[k] = list2hex(res[k])
    if isinstance(r[k], str):
        r[k] = eval(r[k])

temp = r[0] ^ r[1] ^ r[2] ^ r[3]
if x2[0] == '1' and x1 != '0001':  # 如果最高位为1就会发生数据溢出，此时需要异或11011
    temp = temp ^ 0b11011

return temp'''
def list2hex(list):
    """
    :param list: list的元素都是字符
    :return: 对应的十六进制
    """
    res = ''.join(list)
    res = '0b' + res
    res = hex(eval(res))
    return res
l=8
def multiply_by_2(x):
    """
    :param x: 待处理的16进制数字
    :return: 在伽罗瓦域乘2的结果
    """
    # 先转化成二进制
    x = str(bin(eval(x)))
    # 去掉二进制表示中的'0b'
    start = x.find('b')
    x = x[start + 1:]
    x = list(x)
    # 如果不够八位就补零
    while len(x) < l:
        x.insert(0, '0')

    res = ['*'] * l
    # 如果左移位前高位为1就异或'1b'
    b = ['0', '0', '0', '1', '1', '0', '1', '1']
    for i in range(l):
        if i != l - 1:
            res[i] = x[i + 1]
        else:
            res[i] = '0'

    if x[0] == '1':
        for i in range(l):
            res[i] = eval(res[i]) ^ eval(b[i])
            res[i] = str(res[i])

    return res, x

def multiply_by_1(x):
    x = eval(x)
    return hex(x), x

def multiply_by_3(x):
    """
    :param x: 待处理的数字
    :return: 在伽罗瓦域乘3的结果，相当于乘二再异或上本身
    """
    out = ['0'] * l
    temp, x = multiply_by_2(x)
    for i in range(l):
        out[i] = eval(temp[i]) ^ eval(x[i])
        out[i] = str(out[i])
    return out, x


def GF2_multi(x1, x2):
    # x1=mi
    if isinstance(x2, str):
        x2 = str(bin(eval(x2)))
    else:
        x2 = bin(x2)

    if eval(list2hex(list(x1))) == 1:
        return eval(x2)
    else:
        r = [0] * len(x1)
        for k in range(len(x1)): # k=0是高位
            if x1[k] == '1' and k != len(x1)-1:
                temp = x2
                loop = len(x1)-1-k  # loop次移位
                for j in range(loop):
                    [temp,_] = multiply_by_2(temp) # temp='0b10110001'
                    temp = list2hex(temp)
                r[k] = eval(temp)
            elif x1[k] == '1' and k == len(x1)-1: # 不用移位
                temp = x2
                [temp,_] = multiply_by_1(temp)
                r[k] = eval(temp)
        return r[0] ^ r[1] ^ r[2] ^ r[3] ^ r[4] ^ r[5] ^ r[6] ^ r[7]

A = [['00001110','00001011','00001101','00001001'],
     ['00001001','00001110','00001011','00001101'],
     ['00001101','00001001','00001110','00001011'],
     ['00001011','00001101','00001001','00001110']]

B = [[22, 11, 149, 48], [162, 220, 12, 136], [242, 202, 66, 6], [53, 18, 239, 174]]

res = np.zeros((4,4)).tolist()

for i in range(4):
    for j in range(4):
        ans1 = GF2_multi(A[i][0], B[0][j])
        ans2 = GF2_multi(A[i][1], B[1][j])
        ans3 = GF2_multi(A[i][2], B[2][j])
        ans4 = GF2_multi(A[i][3], B[3][j])

        res[i][j] = hex(ans1 ^ ans2^ans3^ans4)

    print(res[i])

