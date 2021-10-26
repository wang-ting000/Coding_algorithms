import numpy as np
row = 4
col = 4
output_o1 = np.zeros((row, col)).tolist()
output_o2 = np.zeros((row, col)).tolist()
output_o3 = np.zeros((row, col)).tolist()
output_o4 = np.zeros((row, col)).tolist()

# 解字节代换层
def de_map_layer(input, S_box_reverse):
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
            output_o2[i][j] = S_box_reverse[eval(index_0)][eval(index_1)]  # 映射
            output_o2[i][j] = hex(output_o2[i][j])
    return output_o2
# 解行位移
def de_shift_rows(input):
    for i in range(row):
        for j in range(col):
            tmp = np.mod(j - i, col)
            output_o3[i][j] = input[i][tmp]
    return output_o3


if __name__ == "__main__":
    pass
