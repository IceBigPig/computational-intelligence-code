import random
import time

w = 0.7
N = 30
V_max = 5
V_min = -5
G_max = 10000


def pso_algorithm(v, c_1, r_1, p_Best, x, c_2, r_2, g_Best):
    return w * v + c_1 * r_1 * (p_Best - x) + c_2 * r_2 * (g_Best - x)


def compute_f(arr):
    return 1 / (abs(arr[0] + 1) + abs(arr[1]) + abs(arr[2] - 1) + abs(arr[3] - 2) + abs(arr[4] + 2) + abs(arr[5] - 3) +
                abs(arr[6] + 3) + abs(arr[7]) + 1)


def init_point_X():
    x_arr = []
    for j in range(0, 8):
        x_arr.append(random.randint(-10, 10))
    return x_arr


def init_point_V():
    v_arr = []
    for j in range(0, 8):
        v_arr.append(random.randint(V_min, V_max))
    return v_arr


max_index = 0
max_value = 0

pBest_arr = []
res_arr = []

var_x = []
var_v = []
# 初始化粒子群
for i in range(0, N):
    var_x.append(init_point_X())
    var_v.append(init_point_V())

for i in range(0, N):
    print("初始化点", i, ":", var_x[i][0], var_x[i][1], var_x[i][2], var_x[i][3], var_x[i][4], var_x[i][5], var_x[i][6],
          var_x[i][7])
    res = compute_f(var_x[i])
    # 记录计算结果
    res_arr.append(res)
    # 记录pBest
    pBest_arr.append(var_x[i])
    # 记录最大值
    if res > max_value:
        max_value = res
        max_index = i

# 生成gBest
gBest = var_x[max_index]

print("初始化结果：\n")
print("max_index:", max_index, "value:", max_value)
print("compute result:" + str(res_arr))
print("gBest=" + str(gBest))
print("Value:gBest=" + str(compute_f(gBest)))
print("V init =" + str(var_v))
print("\n\n")

time.sleep(3)


# 随机生成 0-1 之间的小数
def get_r():
    return random.randint(0, 100) / 100


times = 0
IS_EOF = True
while IS_EOF:
    times = times + 1
    # 更新每一个粒子
    for i in range(0, N):
        # 更新第i个粒子的速度
        for x in range(0, 8):
            # 计算第x维度
            var_v[i][x] = pso_algorithm(var_v[i][x], 2.0, 0.7, pBest_arr[i][x], var_x[i][x], 2.0, 0.5, gBest[x])
        # 更新第i个粒子位置
        for x in range(0, 8):
            # 计算第x维度
            var_x[i][x] = var_x[i][x] + var_v[i][x]

        # 比较更新后的粒子
        res = compute_f(var_x[i])
        if res > compute_f(pBest_arr[i]):
            print("更新pBest:" + str(i))
            time.sleep(3)
            pBest_arr[i] = var_x[i]

        if compute_f(pBest_arr[i]) > compute_f(gBest):
            gBest = pBest_arr[i]

    print("第", times, "次计算:\t", var_x[i][0], var_x[i][1], var_x[i][2], var_x[i][3], var_x[i][4], var_x[i][5],
          var_x[i][6], var_x[i][7])

    if times == 10000:
        IS_EOF = False
print(gBest)
print("计算结果：" + str(compute_f(gBest)))
