import random
import numpy as np
from openpyxl import Workbook

V_max = 5
V_min = -5
X_max = 10
X_min = -10
particle_nums = 30  # 种群数量
D = 8  # 计算维度

temp_res = []


def rand_r():
    return random.randint(0, 100) / 100


def get_fitness_evaluation(arr):
    y = float(1.00 / (abs(arr[0] + 1) + abs(arr[1]) + abs(arr[2] - 1) + abs(arr[3] - 2) +
                      abs(arr[4] + 2) + abs(arr[5] - 3) + abs(arr[6] + 3) + abs(arr[7]) + 1))
    return y


class PSOAlgorithm:
    def __init__(self):
        self.x = np.zeros((particle_nums, D), dtype=float)  # 粒子当前位置
        self.v = np.zeros((particle_nums, 8), dtype=float)  # 例子的方向和速度
        self.c1 = 2.0
        self.c2 = 2.0
        self.w = 0.7  # 惯性因子
        self.pbest = np.zeros((particle_nums, D), dtype=float)  # 粒子的历史最优位置
        self.gbest = np.zeros(D, dtype=float)  # 所有粒子历史最优位置，（最大化问题对应）
        self.p_best_fitness = np.zeros(particle_nums, dtype=float)
        self.g_best_fitness = 0.0

    def initial_function(self):
        """初始化函数"""
        # 初始化每一个粒子
        for i in range(0, particle_nums):
            for j in range(0, D):
                self.x[i][j] = float(random.randint(X_min, X_max))
                self.v[i][j] = float(random.randint(V_min, V_max))
            # 初始化g_best和p_best
            self.p_best_fitness[i] = get_fitness_evaluation(self.x[i])
            # 初始化当前个体最优位置，并找到群体最优位置

            if self.p_best_fitness[i] > self.g_best_fitness:
                self.g_best_fitness = self.p_best_fitness[i]
                self.gbest = self.x[i]
        print("算法开始，初始最优解：", self.gbest, self.g_best_fitness)
        print("")

    def pso_main(self, max_iteration):
        """粒子群算法主函数"""
        for i in range(0, max_iteration):  # 迭代次数
            for j in range(0, particle_nums):  # 更新粒子速度和位置
                # 更新粒子速度
                for k in range(0, D):
                    # 计算每一维度
                    self.v[j][k] = self.w * self.v[j][k] + self.c1 * rand_r() * (
                            self.pbest[j][k] - self.x[j][k]) + self.c2 * rand_r() * (
                                           self.gbest[k] - self.x[j][k])
                # 控制速度不超过最大值
                for a in range(0, D):
                    if self.v[j][a] > V_max:
                        self.v[j][a] = V_max
                    if self.v[j][a] < V_min:
                        self.v[j][a] = V_min
                # 更新粒子位置
                self.x[j] += self.v[j]
                # 控制速度不超过最大值
                for a in range(0, D):
                    if self.x[j][a] > X_max:
                        self.x[j][a] = X_max
                    if self.x[j][a] < X_min:
                        self.x[j][a] = X_min
                # 评价每个粒子的适应度
                new_p_fitness = get_fitness_evaluation(self.x[j])
                # 更新个体最优
                if self.p_best_fitness[j] < new_p_fitness:
                    self.p_best_fitness[j] = new_p_fitness
                    self.pbest[j] = self.x[j]
                # 更新全局最优
                if new_p_fitness > self.g_best_fitness:
                    self.g_best_fitness = new_p_fitness
                    self.gbest = self.x[j]
            # 输出算法迭代信息到控制台
            print("第%s次迭代，全局最优解%s" % (i + 1, self.gbest))
            print(self.g_best_fitness)
            temp_res.append(self.g_best_fitness)
            print("")


if __name__ == '__main__':
    book = Workbook()
    sheet = book.active
    for i in range(0, 11):
        pso = PSOAlgorithm()
        pso.initial_function()
        pso.pso_main(1000)
        for j in range(0, len(temp_res)):
            sheet.cell(row=j + 1, column=i + 1).value = temp_res[j]
        del pso
        temp_res = []
    book.save("sample.xlsx")
