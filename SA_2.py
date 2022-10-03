# coding:gbk
import random
import math

# n个物品 ,背包容量C
# time 迭代次数, balance  平衡次数
# best 记录全局最优  T 温度  af退火率
global best, m, C, w_sum, v_sum
n = 5
T = 10.0
af = 0.95
time = 10
balance = 3
best_way = [0] * n
now_way = [0] * n  # best_way 记录全局最优解方案   now_way 记录当前解方案
weight = [2, 3, 5, 1, 4]
value = [2, 5, 8, 3, 6]


def cop(a, b, le):  # 复制函数 把b数组的值赋值a数组
    for i in range(le):
        a[i] = b[i]


def calc(x):  # 计算背包价值
    global C, w_sum
    v_sum = 0
    w_sum = 0
    for i in range(n):
        v_sum += x[i] * value[i]
        w_sum += x[i] * weight[i]
    return v_sum


def produce():  # 初始产生随机解
    while 1 > 0:
        for k in range(n):
            if random.random() < 0.5:
                now_way[k] = 1
            else:
                now_way[k] = 0
        calc(now_way)
        if w_sum < C:
            break
    global best
    best = calc(now_way)
    cop(best_way, now_way, n)


def init():  # 初始化函数
    global C, best, T
    C = 8
    best = -1
    produce()  # 产生初始解


def get(x):  # 随机将背包中已经存在的物品取出
    while 1 > 0:
        ob = random.randint(0, n - 1)
        if x[ob] == 1:
            x[ob] = 0
            break


def put(x):  # 随机放入背包中不存在的物品
    while 1 > 0:
        ob = random.randint(0, n - 1)
        if x[ob] == 0:
            x[ob] = 1
            break


def solve():  # 迭代函数
    global best, T, balance
    test = [0] * n
    for i in range(balance):
        now = calc(now_way)
        cop(test, now_way, n)
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
        temp = calc(test)
        if w_sum > C:
            continue  # 非法解则跳过
        if temp > best:
            best = temp
            cop(best_way, test, n)  # 更新全局最优

        if temp > now:
            cop(now_way, test, n)  # 直接接受新解
        else:
            g = 1.0 * (temp - now) / T
            if random.random() < math.exp(g):  # 概率接受劣解
                cop(now_way, test, n)


init()
isGood = 0
for i in range(time):
    solve()
    T = T * af  # 温度下降
    if best == 11:
        print('找到最优解:295,迭代次数', i + 1)
        isGood = 1
        break  # 达到最优解提前退出

if isGood == 0:
    print('只找到次优解:', best, '迭代次数', time)
print('方案为：', best_way)  # 打印方案
