import random
import sys
import copy

# 初始三十个城市坐标
city_x = [41, 37, 54, 25, 7, 2, 68, 71, 54, 83, 64, 18, 22, 83, 91, 25, 24, 58, 71, 74, 87, 18, 13, 82, 62, 58, 45, 41,
          44, 4]
city_y = [94, 84, 67, 62, 64, 99, 58, 44, 62, 69, 60, 54, 60, 46, 38, 38, 42, 69, 71, 78, 76, 40, 40, 7, 32, 35, 21, 26,
          35, 50]
# 城市数量
n = 30
distance = [[0 for col in range(n)] for raw in range(n)]

# 禁忌表
tabu_list = []
tabu_time = []
# 当前禁忌对象数量
current_tabu_num = 0
# 禁忌长度，即禁忌期限
tabu_limit = 50
# 候选集
candidate = [[0 for col in range(n)] for raw in range(200)]
candidate_distance = [0 for col in range(200)]
# 最佳路径以及最佳距离
best_route = []
best_distance = sys.maxsize
current_route = []
current_distance = 0.0


def greedy():
    # 通过贪婪算法确定初始r值，也就是初始信息素浓度
    sum = 0.0
    # 必须实例化一个一个赋值，不然只是把地址赋值，牵一发而动全身
    dis = [[0 for col in range(n)] for raw in range(n)]
    for i in range(n):
        for j in range(n):
            dis[i][j] = distance[i][j]

    visited = []
    # 进行贪婪选择——每次都选择距离最近的
    id = 0
    for i in range(n):
        for j in range(n):
            dis[j][id] = sys.maxsize
        minvalue = min(dis[id])
        if i != 29:
            sum += minvalue
        visited.append(id)
        id = dis[id].index(minvalue)
    sum += distance[0][visited[n - 1]]
    return visited


# 构建初始参考距离矩阵
def getdistance():
    for i in range(n):
        for j in range(n):
            x = pow(city_x[i] - city_x[j], 2)
            y = pow(city_y[i] - city_y[j], 2)
            distance[i][j] = pow(x + y, 0.5)
    for i in range(n):
        for j in range(n):
            if distance[i][j] == 0:
                distance[i][j] = sys.maxsize


# 计算总距离
def cacl_best(rou):
    sumdis = 0.0
    for i in range(n - 1):
        sumdis += distance[rou[i]][rou[i + 1]]
    sumdis += distance[rou[n - 1]][rou[0]]
    return sumdis


# 初始设置
def setup():
    global best_route
    global best_distance
    global tabu_time
    global current_tabu_num
    global current_distance
    global current_route
    global tabu_list
    # 得到初始解以及初始距离
    # current_route = random.sample(range(0, n), n)
    current_route = greedy()
    best_route = copy.copy(current_route)
    # 函数内部修改全局变量的值
    current_distance = cacl_best(current_route)
    best_distance = current_distance

    # 置禁忌表为空
    tabu_list.clear()
    tabu_time.clear()
    current_tabu_num = 0


# 交换数组两个元素
def exchange(index1, index2, arr):
    current_list = copy.copy(arr)
    current = current_list[index1]
    current_list[index1] = current_list[index2]
    current_list[index2] = current
    return current_list


# 得到邻域 候选解
def get_candidate():
    global best_route
    global best_distance
    global current_tabu_num
    global current_distance
    global current_route
    global tabu_list
    # 存储两个交换的位置
    exchange_position = []
    temp = 0
    # 随机选取邻域
    while True:
        current = random.sample(range(0, n), 2)
        # print(current)
        if current not in exchange_position:
            exchange_position.append(current)
            candidate[temp] = exchange(current[0], current[1], current_route)
            if candidate[temp] not in tabu_list:
                candidate_distance[temp] = cacl_best(candidate[temp])
                temp += 1
            if temp >= 200:
                break

    # 得到候选解中的最优解
    candidate_best = min(candidate_distance)
    best_index = candidate_distance.index(candidate_best)

    current_distance = candidate_best
    current_route = copy.copy(candidate[best_index])
    # 与当前最优解进行比较

    if current_distance < best_distance:
        best_distance = current_distance
        best_route = copy.copy(current_route)

    # 加入禁忌表
    tabu_list.append(candidate[best_index])
    tabu_time.append(tabu_limit)
    current_tabu_num += 1


# 更新禁忌表以及禁忌期限
def update_tabu():
    global current_tabu_num
    global tabu_time
    global tabu_list

    del_num = 0
    temp = [0 for col in range(n)]
    # 更新步长
    tabu_time = [x - 1 for x in tabu_time]
    # 如果达到期限，释放
    for i in range(current_tabu_num):
        if tabu_time[i] == 0:
            del_num += 1
            tabu_list[i] = temp

    current_tabu_num -= del_num
    while 0 in tabu_time:
        tabu_time.remove(0)

    while temp in tabu_list:
        tabu_list.remove(temp)


def solve():
    getdistance()
    runtime = int(input("迭代次数："))
    setup()
    for rt in range(runtime):
        get_candidate()
        update_tabu()

    print("当前距离：")
    print(current_distance)
    print(current_route)
    print("最优距离：")
    print(best_route)
    print(best_distance)


if __name__ == "__main__":
    solve()
