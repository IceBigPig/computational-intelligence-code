import random
import numpy as np
import math
import copy


class SA:
    def __init__(self):
        # 初始温度
        self.T = 200
        # 平衡条件参数
        self.times = 30
        # 物体个数
        self.n = 5
        # 背包容量
        self.c = 8
        # 重量
        self.w = [2, 3, 5, 1, 4]
        # 价值
        self.v = [2, 5, 8, 3, 6]
        # 最优解
        self.s = -1
        # 构造的邻域解
        self.i = np.zeros(self.n)

    # 计算价值
    def get_F_i(self, arr):
        sum = 0
        for i in range(0, self.n):
            sum += arr[i] * self.v[i]
        return sum

    # 计算重量
    def get_wight(self, arr):
        sum = 0
        for i in range(0, self.n):
            sum += arr[i] * self.w[i]
        return sum

    # 随机生成一串二进制数字（数组）
    def get_Rand_Bool_Num(self):
        for i in range(0, self.n):
            self.i[i] = random.randint(0, 1)
        return self.i

    # 计算新解的接受概率
    def calculateP_k(self, j):
        a = (self.get_F_i(j) - self.get_F_i(self.i)) / self.T
        print(a)
        return math.exp(a)

    # 初始化计算最优解
    def init_SA(self):
        local_fit = self.get_F_i(self.get_Rand_Bool_Num())
        while self.get_wight(self.i) > self.c:
            local_fit = self.get_F_i(self.get_Rand_Bool_Num())
        self.s = local_fit

    # 在T温度下局部搜索
    def local_search(self):
        for local_T in range(self.T, 1, -1):
            times = self.times
            for i in range(0, times):
                # 构造邻域解,并判断是否合法
                local_j = copy.deepcopy(self.i)
                while True:
                    # 随机反转一位数字
                    bit = random.randint(0, self.n - 1)
                    if local_j[bit] == 0:
                        local_j[bit] = 1
                    else:
                        local_j[bit] = 0
                    # 计算反转后的解值
                    local_weight = self.get_wight(local_j)
                    if local_weight < self.c and local_weight != 0:
                        local_fit = self.get_F_i(local_j)
                        break
                    else:
                        local_j = copy.deepcopy(self.i)
                # 当局部搜索到的值由于全局时,接受新的解,更新全局值
                if local_fit > self.s:
                    self.i = local_j
                    self.s = local_fit
                    print("更新全局最优解：", local_j, local_fit)
                elif local_fit <= self.s:
                    # 当搜索到的值小于全局最优时，计算接受概率P(t)
                    P_t = self.calculateP_k(local_j)
                    # 达到接受概率接受新的解
                    p_temp = random.uniform(0, 1)
                    if p_temp < P_t:
                        print("接受劣解:", P_t, ">", p_temp, "接受劣解：", local_fit, "更新前全局最优解：", self.s)
                        self.i = local_j
                        self.s = local_fit
                print("温度为：", local_T, " 局部适应值：", local_fit)
            self.T -= 1


if __name__ == '__main__':
    sa_test = SA()
    sa_test.init_SA()
    sa_test.local_search()
    print(sa_test.s)
    print(sa_test.i)
    print(sa_test.get_wight(sa_test.i))
