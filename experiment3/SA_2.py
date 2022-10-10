# coding:gbk
import random
import math
import openpyxl

# C 背包容量,best全局最优解
global best, m, C, w_sum, v_sum, T, n, iteration_times, balance_times, weight, value, best_way, now_way


# 初始化函数
def init():
    global best, m, C, w_sum, v_sum, T, n, iteration_times, balance_times, weight, value, best_way, now_way
    C = 8
    # 物品数量
    n = 5
    # 初始温度
    T = 10.0
    # 迭代次数
    iteration_times = 10
    # 平衡次数
    balance_times = 3
    # 重量
    weight = [2, 3, 5, 1, 4]
    # 价值
    value = [2, 5, 8, 3, 6]
    # best_way 记录全局最优解方案
    best_way = [0] * n
    # now_way 记录当前解方案
    now_way = [0] * n
    best = -1
    # 产生初始解
    while True:
        for k in range(n):
            if random.random() < 0.5:
                now_way[k] = 1
            else:
                now_way[k] = 0
        calculate_value(now_way)
        if w_sum < C:
            break
    best = calculate_value(now_way)
    copy_arr(best_way, now_way, n)


# 随机将背包中已经存在的物品取出
def get(x):
    while 1 > 0:
        ob = random.randint(0, n - 1)
        if x[ob] == 1:
            x[ob] = 0
            break


# 随机放入背包中不存在的物品
def put(x):
    while 1 > 0:
        ob = random.randint(0, n - 1)
        if x[ob] == 0:
            x[ob] = 1
            break


# 迭代函数
def start_iteration():
    global best, T, balance_times
    test = [0] * n
    for i in range(balance_times):
        now = calculate_value(now_way)
        copy_arr(test, now_way, n)
        ob = random.randint(0, n - 1)  # 随机选取某个物品
        if test[ob] == 1:
            put(test)
            test[ob] = 0  # 在背包中则将其拿出，并加入其它物品
        else:  # 不在背包中则直接加入或替换掉已在背包中的物品
            if random.random() < 0.5:
                test[ob] = 1
            else:
                get(test)
                test[ob] = 1
        temp = calculate_value(test)
        if w_sum > C:
            continue  # 非法解则跳过
        if temp > best:
            best = temp
            copy_arr(best_way, test, n)  # 更新全局最优
        if temp > now:
            copy_arr(now_way, test, n)  # 直接接受新解
        else:
            g = 1.0 * (temp - now) / T
            if random.random() < math.exp(g):  # 概率接受劣解
                copy_arr(now_way, test, n)


# 复制函数 把b数组的值赋值a数组
def copy_arr(a, b, le):
    for i in range(le):
        a[i] = b[i]


# 计算背包价值
def calculate_value(x):
    global C, w_sum, v_sum
    v_sum = 0
    w_sum = 0
    for i in range(n):
        v_sum += x[i] * value[i]
        w_sum += x[i] * weight[i]
    return v_sum


if __name__ == "__main__":
    a = ""
    # 创建一个工作簿
    f = openpyxl.Workbook()
    table = f.active
    table.title = 'SA_Res'
    for i in range(0, 8):
        init()
        is_best_flag = False
        for i in range(iteration_times):
            start_iteration()
            T = T - 1  # 温度下降
            if best == 14:
                print('找到最优解:14,迭代次数', i + 1)
                a = '找到最优解:14,迭代次数' + str(i + 1)

                is_best_flag = True
                # 达到最优解提前退出
                break
        if not is_best_flag:
            print('只找到次优解:', best, '迭代次数', iteration_times)
            a = '只找到次优解:' + str(best) + '迭代次数' + str(iteration_times)
        table.cell(row=i + 1, column=1).value = a
        print('方案为：', best_way)
    f.save('SA_2_res.xlsx')
