# coding:gbk
import random
import math

# n����Ʒ ,��������C
# time ��������, balance  ƽ�����
# best ��¼ȫ������  T �¶�  af�˻���
global best, m, C, w_sum, v_sum
n = 5
T = 10.0
af = 0.95
time = 10
balance = 3
best_way = [0] * n
now_way = [0] * n  # best_way ��¼ȫ�����Žⷽ��   now_way ��¼��ǰ�ⷽ��
weight = [2, 3, 5, 1, 4]
value = [2, 5, 8, 3, 6]


def cop(a, b, le):  # ���ƺ��� ��b�����ֵ��ֵa����
    for i in range(le):
        a[i] = b[i]


def calc(x):  # ���㱳����ֵ
    global C, w_sum
    v_sum = 0
    w_sum = 0
    for i in range(n):
        v_sum += x[i] * value[i]
        w_sum += x[i] * weight[i]
    return v_sum


def produce():  # ��ʼ���������
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


def init():  # ��ʼ������
    global C, best, T
    C = 8
    best = -1
    produce()  # ������ʼ��


def get(x):  # ������������Ѿ����ڵ���Ʒȡ��
    while 1 > 0:
        ob = random.randint(0, n - 1)
        if x[ob] == 1:
            x[ob] = 0
            break


def put(x):  # ������뱳���в����ڵ���Ʒ
    while 1 > 0:
        ob = random.randint(0, n - 1)
        if x[ob] == 0:
            x[ob] = 1
            break


def solve():  # ��������
    global best, T, balance
    test = [0] * n
    for i in range(balance):
        now = calc(now_way)
        cop(test, now_way, n)
        ob = random.randint(0, n - 1)  # ���ѡȡĳ����Ʒ
        if test[ob] == 1:
            put(test)
            test[ob] = 0  # �ڱ����������ó���������������Ʒ
        else:  # ���ڱ�������ֱ�Ӽ�����滻�����ڱ����е���Ʒ
            if random.random() < 0.5:
                test[ob] = 1
            else:
                get(test)
                test[ob] = 1
        temp = calc(test)
        if w_sum > C:
            continue  # �Ƿ���������
        if temp > best:
            best = temp
            cop(best_way, test, n)  # ����ȫ������

        if temp > now:
            cop(now_way, test, n)  # ֱ�ӽ����½�
        else:
            g = 1.0 * (temp - now) / T
            if random.random() < math.exp(g):  # ���ʽ����ӽ�
                cop(now_way, test, n)


init()
isGood = 0
for i in range(time):
    solve()
    T = T * af  # �¶��½�
    if best == 11:
        print('�ҵ����Ž�:295,��������', i + 1)
        isGood = 1
        break  # �ﵽ���Ž���ǰ�˳�

if isGood == 0:
    print('ֻ�ҵ����Ž�:', best, '��������', time)
print('����Ϊ��', best_way)  # ��ӡ����
