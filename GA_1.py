import random
import numpy as np
import openpyxl

# 群体规模
N = 20
# 计算维度
D = 4
# 取值范围
C_MAX = 5.0
C_MIN = -5.0
# 交配概率
Mating_Probability = 0.9
# 变异概率
Variation_Probability = 0.05


def getEval(arr):
    return 1.0 / (arr[0] * arr[0] + arr[1] * arr[1] + arr[2] * arr[2] + arr[3] * arr[3] + 1)


class genetic_model:

    def __init__(self):
        self.C = np.zeros((N, D), dtype=float)
        self.Best = np.zeros(D, dtype=float)
        self.Eval_Best = 0.0
        self.Eval = np.zeros(N, dtype=float)
        self.Proportion = np.zeros(N, dtype=float)

    # 初始化
    def init_model(self):
        # 初始化群体
        for i in range(0, N):
            for j in range(0, D):
                self.C[i][j] = random.uniform(C_MIN, C_MAX)
            # 计算Best和Eval_Best
            res = getEval(self.C[i])
            self.Eval[i] = res
            if res > self.Eval_Best:
                self.Eval_Best = res
                self.Best = self.C[i]
        print("粒子群:\n", self.C)
        print("适应值:\n", self.Eval)

    # 轮盘选择
    def select(self):
        # 计算群体适应值总和
        Eval_all = 0.0
        for i in range(0, N):
            Eval_all += self.Eval[i]
        for i in range(0, N):
            self.Proportion[i] = self.Eval[i] / Eval_all
        temp_arr = []
        for i in range(0, N):
            rand_num = random.uniform(0, 1)
            aim = 0.0
            for j in range(0, N):
                if aim <= rand_num <= aim + self.Proportion[j]:
                    temp_arr.append(j)
                    break
                aim += self.Proportion[j]
        # 更新粒子群体
        temp_C = self.C
        for i in range(0, N):
            self.C[i] = temp_C[temp_arr[i]]

    def mating(self):
        temp_probability = np.zeros(N, dtype=bool)
        for i in range(0, N):
            # 达到交配概率的进行交配标记
            if random.uniform(0, 1) < Mating_Probability:
                temp_probability[i] = True
            # 没有达到交配概率的直接进行保留
            else:
                temp_probability[i] = False

        mating_pop = []
        for j in range(0, N):
            if temp_probability[j]:
                mating_pop.append(j)
                if len(mating_pop) == 2:
                    bit = random.randint(0, D - 1)
                    self.mating_action(bit, mating_pop[0], mating_pop[1])
                    # 清空临时交配粒子记录
                    mating_pop = []
            else:
                continue

    def mating_action(self, bit, index_one, index_two):
        index = D - bit - 1
        for i in range(0, D):
            if i >= index:
                temp = self.C[index_one][i]
                self.C[index_one][i] = self.C[index_two][i]
                self.C[index_two][i] = temp

    # 变异处理
    def variation(self):
        for i in range(0, N):
            probability = random.uniform(0, 1)
            bit = random.randint(0, D - 1)
            # 当达到变异条件时，进行变异
            if probability <= Variation_Probability:
                print("变异染色体:", i, "染色体位:", bit)
                self.C[i][bit] = random.uniform(C_MIN, C_MAX)

    # 重新评估适应值
    def reevaluation(self):
        for i in range(0, N):
            # 计算Best和Eval_Best
            res = getEval(self.C[i])
            self.Eval[i] = res
            if res > self.Eval_Best:
                self.Eval_Best = res
                self.Best = self.C[i]


if __name__ == '__main__':
    # 创建一个工作簿
    f = openpyxl.Workbook()
    table = f.active
    table.title = 'GA_1'

    for j in range(0, 6):
        Variation_Probability += 0.1
        genetic = genetic_model()
        genetic.init_model()
        for i in range(0, 10000):
            genetic.select()
            genetic.mating()
            genetic.variation()
            genetic.reevaluation()
            print("\nBest=", genetic.Eval_Best)
            table.cell(row=i+1, column=j+1).value = genetic.Eval_Best
        del genetic
    # 保存文件
    f.save('GA_1_res.xlsx')
