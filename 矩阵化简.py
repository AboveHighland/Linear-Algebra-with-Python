import numpy as np
from fractions import Fraction

# 此函数可以逐行获得矩阵的非零首元的列位置信息，
# 并把信息存储在列表中，返回该列表
def get_fn(matrix):
    lt = []
    for item in matrix:
        t = 0
        while t < len(item) and item[t] == 0:
            t += 1
        lt.append(t)
    return lt

# 此函数根据首元信息，调整原矩阵的各行位置，
# 返回的矩阵，每行首元列位置总体增大，如[0,0,2,3]

def zero_down(matx):
    matx_old=matx
    llt=get_fn(matx_old)
    cl=len(matx_old[0])  #列数
    #lt是包含首元位置信息的列表

    matrix_new=[]
    for k in range(cl+1):
        if k in llt:
            args = [index for index, value in enumerate(llt) if value == k]
            for a in args:
                matrix_new.append(matx_old[a])
    return matrix_new


def row_operation1part(matrix):
    lt = get_fn(matrix)
    cl=len(matrix[0])
    for k in range(cl):
        if lt.count(k) > 1:
            # k出现的第一个位置的索引
            x = lt.index(k)

            # k的个数
            c = lt.count(k)

            # 定位到首元列位置重复的那一行的第一个非零元素
            a = matrix[x][k]
            for s in range(k,len(matrix[x])):
                matrix[x][s]=Fraction(matrix[x][s],a)
            for i in range(1, c):
                aa = matrix[x + i][k]
                for w in range(k,len(matrix[x])):
                    matrix[x+i][w] = matrix[x+i][w]-aa*matrix[x][w]

    return matrix


def format_fraction_matrix(matrix):
    rows = []
    for row in matrix:
        ls_row = []
        for frac in row:
            if frac.denominator == 1:
                ls_row.append(frac.numerator)  # 分母为1时简化为整数
            else:
                ls_row.append(frac.numerator/frac.denominator)  # 否则显示为分数
        rows.append(ls_row)

    return np.array(rows)


#判断是否为阶梯形矩阵，如果是阶梯形，返回True
def isprime(lss,cl):
    element_to_remove=cl    #矩阵的列数
    while element_to_remove in lss:
        #lt.remove()用于移除列表中某个元素的第一个匹配项
        lss.remove(element_to_remove)
    isp=True
    if len(lss)>1:
        for i in range(len(lss) - 1):
            if lss[i] >= lss[i + 1]:
                isp = False
                break
    return isp


#将原矩阵化为阶梯形矩阵
def row_operation(matrix):
    matx = zero_down(matrix)
    lts = get_fn(matx)
    cl=len(matx[0])
    while not isprime(lts,cl):
        matx=row_operation1part(matx)
        matx=zero_down(matx)
        lts = get_fn(matx)

    lts2 = get_fn(matx)
    while cl in lts2:
        lts2.remove(cl)

    for l in lts2:
        x=lts2.index(l)
        axl=matx[x][l]
        if axl != 0 and axl != 1:
            for i in range(l,cl):
                matx[x][i]=Fraction(matx[x][i],axl)
    return matx

#将阶梯形矩阵化为行最简形矩阵
def rref(matx):
    ltm=get_fn(matx)    #首元行列信息
    cl = len(matx[0])  # 矩阵的列数
    ltm2=list(ltm)
    while cl in ltm2:
        ltm2.remove(cl)
    ltm2.reverse()
    for j in ltm2:
        #xr是列序号为j的首元的行序号
        xr=ltm.index(j)
        if xr>0:
            for mn in range(xr):
                rc=matx[mn][j]
                if rc != 0:
                    for pr in range(j,cl):
                        matx[mn][pr]=matx[mn][pr]-rc*(matx[xr][pr])

    return matx

#  ***关键思路***
# 先将矩阵化为行阶梯形，
# 首元信息不是[0,0,2,3]，
# 而要化为首元[0,1,2,3]对应的矩阵



#因为Fraction的两个参数必须是整数
#所以必须矩阵确保每个元素是整数
#把带分数的矩阵每个元素都乘10的某个次方
def format_int(ipt_mx):
    lt_n10 = []
    format_mx=[]
    for row3 in ipt_mx:
        for item in row3:
            if type(item) == float:
                s = str(item)
                d_part = s.split(".")[1]
                l = len(d_part)
                lt_n10.append(l)
    if len(lt_n10) != 0:
        n10 = max(lt_n10)
        for row4 in ipt_mx:
            format_mx_row=[]
            for item in row4:
                new_item = int(item * pow(10, n10))
                format_mx_row.append(new_item)
            format_mx.append(format_mx_row)
        return format_mx
    else:
        return ipt_mx

print("[[0,1,2,3],[0,2,2,3],[0,1,0,0]]")
print("按上述格式（英文输入法），在下一行输入要化为最简式的*非零*原矩阵：")

ipt_mx=eval(input())
print(np.array(ipt_mx))
print("*"*60)


format_mx=format_int(ipt_mx)
mx=row_operation(format_mx)
mx_rref=rref(mx)
print(format_fraction_matrix(mx_rref))













