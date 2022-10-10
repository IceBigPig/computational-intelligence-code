# coding:gbk
import random
import math
import openpyxl

# C ��������,bestȫ�����Ž�
global best, m, C, w_sum, v_sum, T, n, iteration_times, balance_times, weight, value, best_way, now_way


# ��ʼ������
def init():
    global best, m, C, w_sum, v_sum, T, n, iteration_times, balance_times, weight, value, best_way, now_way
    C = 8
    # ��Ʒ����
    n = 5
    # ��ʼ�¶�
    T = 10.0
    # ��������
    iteration_times = 10
    # ƽ�����
    balance_times = 3
    # ����
    weight = [2, 3, 5, 1, 4]
    # ��ֵ
    value = [2, 5, 8, 3, 6]
    # best_way ��¼ȫ�����Žⷽ��
    best_way = [0] * n
    # now_way ��¼��ǰ�ⷽ��
    now_way = [0] * n
    best = -1
    # ������ʼ��
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


# ������������Ѿ����ڵ���Ʒȡ��
def get(x):
    while 1 > 0:
        ob = random.randint(0, n - 1)
        if x[ob] == 1:
            x[ob] = 0
            break


# ������뱳���в����ڵ���Ʒ
def put(x):
    while 1 > 0:
        ob = random.randint(0, n - 1)
        if x[ob] == 0:
            x[ob] = 1
            break


# ��������
def start_iteration():
    global best, T, balance_times
    test = [0] * n
    for i in range(balance_times):
        now = calculate_value(now_way)
        copy_arr(test, now_way, n)
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
        temp = calculate_value(test)
        if w_sum > C:
            continue  # �Ƿ���������
        if temp > best:
            best = temp
            copy_arr(best_way, test, n)  # ����ȫ������
        if temp > now:
            copy_arr(now_way, test, n)  # ֱ�ӽ����½�
        else:
            g = 1.0 * (temp - now) / T
            if random.random() < math.exp(g):  # ���ʽ����ӽ�
                copy_arr(now_way, test, n)


# ���ƺ��� ��b�����ֵ��ֵa����
def copy_arr(a, b, le):
    for i in range(le):
        a[i] = b[i]


# ���㱳����ֵ
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
    # ����һ��������
    f = openpyxl.Workbook()
    table = f.active
    table.title = 'SA_Res'
    for i in range(0, 8):
        init()
        is_best_flag = False
        for i in range(iteration_times):
            start_iteration()
            T = T - 1  # �¶��½�
            if best == 14:
                print('�ҵ����Ž�:14,��������', i + 1)
                a = '�ҵ����Ž�:14,��������' + str(i + 1)

                is_best_flag = True
                # �ﵽ���Ž���ǰ�˳�
                break
        if not is_best_flag:
            print('ֻ�ҵ����Ž�:', best, '��������', iteration_times)
            a = 'ֻ�ҵ����Ž�:' + str(best) + '��������' + str(iteration_times)
        table.cell(row=i + 1, column=1).value = a
        print('����Ϊ��', best_way)
    f.save('SA_2_res.xlsx')
