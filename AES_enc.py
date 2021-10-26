import numpy as np

row = 4
col = 4
l = 8

output_1 = np.zeros((row, col)).tolist()
output_2 = np.zeros((row, col)).tolist()
output_3 = np.zeros((row, col)).tolist()
output_4 = np.zeros((row, col)).tolist()

# 字节代换层
def map_layer(input, S_box):
    for i in range(row):
        for j in range(col):
            text = input[i][j]  # 十六进制表示的整数
            if not isinstance(text, str):
                text = str(hex(text))  # 转化成字符串表示然后拆分开
            start = text.find('x')
            text = text[start + 1:]
            text = list(text)
            while len(text) < 4:
                text.insert(0, '0')
            index_0 = '0x' + text[-2]  # 高四位
            index_1 = '0x' + text[-1]  # 低四位
            output_2[i][j] = S_box[eval(index_0)][eval(index_1)]  # 映射
            output_2[i][j] = hex(output_2[i][j])
    return output_2
# g函数中的映射函数
def map2(text, S_box):
    if not isinstance(text, str):
        text = str(hex(text))  # 转化成字符串表示然后拆分开
    start = text.find('x')
    text = text[start + 1:]
    text = list(text)
    while len(text) < 4:
        text.insert(0, '0')
    index_0 = '0x' + text[-2]  # 高四位
    index_1 = '0x' + text[-1]  # 低四位
    output_2 = S_box[eval(index_0)][eval(index_1)]  # 映射
    output_2 = hex(output_2)
    return output_2
# 异或
def xor(w1, w2):
    """
    :param w1: 格式是'0x1d'
    :param w2:
    :return:格式是['0','x','2','a']
    """
    w1 = eval(w1)
    w2 = eval(w2)
    re = w1 ^ w2
    re = list(hex(re))  # 格式是['0','x','2','a']
    if len(re) < 4:
        re.insert(2, '0')
    return re
# 函数g
def g(w1, RC_000,S_box):
    """
    :param w1: 格式是'0x1e234d5f'
    :return:
    """
    w1 = list(w1)
    w1 = w1[2:]  # 去掉'0x'后的列表
    w1 = ''.join(w1)
    b0 = '0x' + w1[0:2]
    b1 = '0x' + w1[2:4]
    b2 = '0x' + w1[4:6]
    b3 = '0x' + w1[6:8]
    # ------S盒映射--------
    b_0 = map2(b1, S_box)
    b_1 = map2(b2, S_box)
    b_2 = map2(b3, S_box)
    b_3 = map2(b0, S_box)
    # ------xor------------
    r1 = xor(b_0, RC_000)
    r1 = ''.join(r1[2:])  # 格式是'2a'
    r2 = xor(b_1, '0x00')  # 格式是['0','x','2','a']
    r2 = ''.join(r2[2:])
    r3 = xor(b_2, '0x00')
    r3 = ''.join(r3[2:])
    r4 = xor(b_3, '0x00')
    r4 = ''.join(r4[2:])

    res = '0x' + r1 + r2 + r3 + r4
    return res
# 密钥扩展
def extend_key(key,S_box):
    RC = ['0x00', '0x01', '0x02', '0x04', '0x08', '0x10', '0x20', '0x40', '0x80', '0x1b', '0x36']
    W = np.zeros(44).tolist()
    W[0] = '0x' + key[0] + key[1] + key[2] + key[3]
    W[1] = '0x' + key[4] + key[5] + key[6] + key[7]
    W[2] = '0x' + key[8] + key[9] + key[10] + key[11]
    W[3] = '0x' + key[12] + key[13] + key[14] + key[15]

    for i in range(4, 44):
        if i / 4 == i // 4:
            RC_000 = RC[int(i / 4)]
            W[i] = xor(W[i - 4], g(W[i - 1], RC_000,S_box))
        else:
            W[i] = xor(W[i - 4], W[i - 1])
        W[i] = ''.join(W[i])
    return W
# 轮密钥加
def add_layer(input, KeyArray):
    for i in range(row):
        for j in range(col):
            if isinstance(input[i][j], str):
                input[i][j] = eval(input[i][j])
            output_1[i][j] = input[i][j] ^ KeyArray[i][j]  # 异或运算
            output_1[i][j] = hex(output_1[i][j])
    return output_1
# 行混淆
def shift_rows(input):
    for i in range(row):
        for j in range(col):
            tmp = np.mod(j + i, col)
            output_3[i][j] = input[i][tmp]
    return output_3
# 列混淆
### 列混淆子层是AES算法中最为复杂的部分，属于扩散层，
### 列混淆操作是AES算法中主要的扩散元素，它混淆了输入矩阵的每一列，
### 使输入的每个字节都会影响到4个输出字节。
### 行位移子层和列混淆子层的组合使得经过三轮处理以后，矩阵的每个字节都依赖于16个明文字节成可能。
### 其中包含了矩阵乘法、伽罗瓦域内加法和乘法的相关知识。
def list2hex(list):
    """
    :param list: list的元素都是字符
    :return: 对应的十六进制
    """
    res = ''.join(list)
    res = '0b' + res
    res = hex(eval(res))
    return res

# 伽罗瓦域乘法
def multiply_by_1(x):
    x = eval(x)
    return hex(x), x

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

def GF2_multi(x1, x2):
    # x1='0001'
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
        return r[0] ^ r[1] ^ r[2] ^ r[3]
# 列混淆
def mix_columns(input,m):
    for i in range(row):
        for j in range(col):
            if isinstance(input[i][j], str):
                input[i][j] = eval(input[i][j])
            if isinstance(m[i][j], int):
                m[i][j] = bin(m[i][j])[2:]

    for i in range(row):
        for j in range(col):
            r1 = GF2_multi(m[i][0], input[0][j])

            r2 = GF2_multi(m[i][1], input[1][j])

            r3 = GF2_multi(m[i][2], input[2][j])

            r4 = GF2_multi(m[i][3], input[3][j])

            output_4[i][j] = r1 ^ r2 ^ r3 ^ r4

            output_4[i][j] = hex(output_4[i][j])
    return output_4




if __name__ == "__main__":
    pass
