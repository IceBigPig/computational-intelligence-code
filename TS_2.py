import copy

# 城市数量
city_num = 4
# 城市坐标位置和距离
city = [
    [0, 1, 0.5, 1],
    [1, 0, 1, 1],
    [1.5, 5, 0, 1],
    [1, 1, 1, 0]
]

# 禁忌表
tabu_list = []
tabu_time = []
# 禁忌长度，即禁忌期限
tabu_limit = 2
# 初始化解
city_i = [0, 1, 2, 3]
# 最优解
best_s = copy.deepcopy(city_i)
# 最优距离
best_distance = 4.0


# 计算解的距离(传入的是真实的顺序)
def get_distance(i_arr):
    local_distance = 0.0
    for i in range(0, city_num - 1):
        local_distance += city[i_arr[i]][i_arr[i + 1]]
    local_distance += city[i_arr[city_num - 1]][i_arr[0]]
    return local_distance


# 给定两城市的名称，交换两个城市的位置
def swap_city(i, j):
    city_arr = copy.deepcopy(city_i)
    index_i = city_arr.index(i)
    index_j = city_arr.index(j)
    temp_ = city_arr[index_i]
    city_arr[index_i] = city_arr[index_j]
    city_arr[index_j] = temp_
    return city_arr


local_tabu_time = []
local_tabu_list = []


# 降低周期
def decrease_period():
    length = len(tabu_time)
    if length != 0:
        for i in range(0, length):
            tabu_time[i] = tabu_time[i] - 1
            if tabu_time[i] == -1:
                local_tabu_list.append(tabu_list[i])
                local_tabu_time.append(tabu_time[i])


for i in range(0, 1000):
    # 临时变量
    local_i = -1
    local_j = -1
    local_best_fit = 9999999
    # 开始从第二个进行交换
    for i in range(1, city_num - 1):
        # 待交换的第一层
        for j in range(i + 1, city_num):
            # 待交换的二层
            if [i, j] in tabu_list:
                # 当遍历交换时出现的交换位在交换表中，则不进行交换
                print("不进行交换", i, j)
                continue
            else:
                # 当交换位不存在交换表中，进行交换并计算距离
                temp_distance = get_distance(swap_city(i, j))
                print("交换位：", i, j, "距离是：", temp_distance)
                # 局部最优
                if temp_distance < local_best_fit:
                    local_best_fit = temp_distance
                    local_i = i
                    local_j = j
    decrease_period()
    tabu_time = copy.deepcopy(local_tabu_time)
    tabu_list = copy.deepcopy(local_tabu_list)
    local_tabu_time = []
    local_tabu_list = []
    print("局部最优写入禁忌表：", local_best_fit, " ", local_i, ",", local_j)
    tabu_list.append([local_i, local_j])
    tabu_time.append(tabu_limit)
    city_i = swap_city(local_i, local_j)
    # 若局部最优优于全局，则进行更新
    if local_best_fit < best_distance:
        best_distance = local_best_fit
        best_s = city_i
    print(best_distance)
