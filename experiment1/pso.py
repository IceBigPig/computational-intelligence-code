import numpy as np
import random
import openpyxl

# 临时变量
res = []

# 速度全局声明
V_MAX = 5
V_MIN = -5
X_MAX = 10
X_MIN = -10


# 目标函数，也是适应度函数（求最小化问题）
def function(arr):
    return float(1.00 / (abs(arr[0] + 1) + abs(arr[1]) + abs(arr[2] - 1) + abs(arr[3] - 2) + abs(arr[4] + 2) + abs(
        arr[5] - 3) + abs(arr[6] + 3) + abs(arr[7]) + 1))


# 生成随机[0, 1]的小数
def rand_float():
    return random.randint(0, 100) / 100


class PSO_model:
    def __init__(self, w, c_1, c_2, N, D, M):
        self.w = w  # 惯性权值
        self.c_1 = c_1
        self.c_2 = c_2
        self.N = N  # 初始化种群数量个数
        self.D = D  # 搜索空间维度
        self.M = M  # 迭代的最大次数
        self.x = np.zeros((self.N, self.D), dtype=float)  # 粒子的初始位置
        self.v = np.zeros((self.N, self.D), dtype=float)  # 粒子的初始速度
        self.pBest = np.zeros((self.N, self.D), dtype=float)  # 个体最优值初始化
        self.gBest = np.zeros(self.D, dtype=float)  # 种群最优值
        self.p_fit = np.zeros(self.N, dtype=float)
        self.g_fit = 0.0  # 初始化全局最优适应度

    # 初始化种群
    def init_pop(self):
        for i in range(self.N):
            # 为每一个粒子初始化速度和位置
            for j in range(self.D):
                self.x[i][j] = float(random.randint(X_MIN, X_MAX))
                self.v[i][j] = float(random.randint(V_MIN, V_MAX))

            self.p_fit[i] = function(self.x[i])
            # self.pBest[i] = self.x[i]  # 初始化个体的最优值

            if self.p_fit[i] > self.g_fit:  # 对个体适应度进行比较，计算出最优的种群适应度
                self.g_fit = self.p_fit[i]
                self.gBest = self.x[i]
        print("初始化最优：", self.gBest)
        print(self.g_fit)

    # 更新粒子的位置与速度
    def update(self):
        for t in range(0, self.M):  # 在迭代次数M内进行循环
            for i in range(self.N):  # 更新粒子的速度和位置
                for k in range(0, D):
                    r_1 = rand_float()
                    r_2 = rand_float()
                    self.v[i][k] = self.w * self.v[i][k] + self.c_1 * r_1 * (
                            self.pBest[i][k] - self.x[i][k]) + self.c_2 * r_2 * (self.gBest[k] - self.x[i][k])

                # 修正速度
                self.fix_v(i)

                self.x[i] += self.v[i]
                # 修正位移
                self.fix_x(i)

                aim = function(self.x[i])  # 计算一次目标函数的适应度
                if aim > self.p_fit[i]:  # 比较适应度大小，将大的赋值给个体最优
                    self.p_fit[i] = aim
                    self.pBest[i] = self.x[i]
                if aim > self.g_fit:  # 如果是个体最优再将和全体最优进行对比（与书本相同）
                    self.gBest = self.x[i]
                    self.g_fit = aim
            res.append(self.g_fit)

        print("最优值：", self.g_fit)
        print("位置为：")
        for a in range(0, D):
            print(a + 1, "维:", self.gBest[a])

    def fix_x(self, i):
        for k in range(0, D):
            if self.x[i][k] > X_MAX:
                self.x[i][k] = X_MAX
            if self.x[i][k] < X_MIN:
                self.x[i][k] = X_MIN

    def fix_v(self, i):
        for k in range(0, D):
            if self.v[i][k] > V_MAX:
                self.v[i][k] = V_MAX
            if self.v[i][k] < V_MIN:
                self.v[i][k] = V_MIN


if __name__ == '__main__':
    # w,c1,c2,r1,r2,N,D,M参数初始化
    w = 0.7  # 权重系数
    c1 = c2 = 2.0  # 一般设置为2
    N = 30  # 种群大小
    D = 8  # 搜索空间维度
    M = 10000  # 迭代最大次数

    # 创建一个工作簿
    f = openpyxl.Workbook()
    table = f.active
    table.title = '结果'

    for i in range(0, 11):
        print("第" + str(i + 1) + "次执行")
        pso_object = PSO_model(w, c1, c2, N, D, M)  # 设置初始权值
        pso_object.init_pop()
        pso_object.update()
        for x in range(0, len(res)):
            table.cell(row=x+1, column=i + 1).value = res[x]
        del pso_object
        res = []

    # 保存文件
    f.save('res.xlsx')
