import sys
import random
import time
import numpy as np
from collections import deque
from threading import Timer

E = 50																# 所有的边缘服务器数目
Vn = 27					    										# 数据率
REQUIREMENT = 4													    # 时间约束
Es = list()					                						# 供选的边缘服务器集合
comm_Energy = 1                                                     # 通信能耗
comp_Energy = [1.181, 1.19, 0.842, 0.988, 1.029, 1.061, 1.022, 0.806, 1.087, 0.982, 1.057, 0.85,
               1.138, 0.898, 1.02, 0.898, 0.861, 0.998, 0.86, 0.947, 1.153, 0.915, 1.144, 0.838,
               1.172, 1.073, 1.057, 0.999, 0.814, 1.11, 1.154, 0.885, 1.143, 0.946, 1.098, 1.165,
               1.099, 0.906, 0.924, 0.894, 0.975, 1.059, 0.891, 0.852, 0.807, 1.119, 1.046, 0.887,
               0.944, 1.106]                                        # 边缘服务器计算能耗
performance = [1262, 1021, 1560, 1574, 1001, 1492, 1107, 1123, 1728, 1314, 1955, 1167, 1146, 1706,
               1026, 1817, 1266, 1306, 1846, 1726, 1693, 1633, 1126, 1744, 1231, 1303, 1564, 1701,
               1438, 1351, 1776, 1968, 1922, 1769, 1184, 1797, 1431, 1007, 1610, 1091, 1022, 1056,
               1235, 1772, 1384, 1002, 1265, 1907, 1314, 1824]
# performance = np.empty(E, dtype=int)				        		# 每个边缘服务器的性能
que = list()				                       					# 边缘服务器上的排队队列


class Task:
    def __init__(self, val1, val2, val3):
        self.task_size = val1										# 任务大小
        self.result = val2											# 结果大小
        self.target = val3											# 任务总指令数
        self.com_t = np.zeros(E, dtype=float)  						# 通讯时间
        self.process_t = np.zeros(E, dtype=float)  					# 处理时间
        self.que_t = np.zeros(E, dtype=float)  						# 排队时间
        self.energy = np.zeros(E, dtype=float)                      # 总能耗
        self.sum_t = 0  											# 选定边缘服务器后的总运行时间


def initial():
    for i in range(E):
        Es.append(i+1)
        # performance[i] = random.randint(1000, 2000)
        que.append(deque())


def sae(t):
    result = None
    for i in range(E):
        t.com_t[i] = (t.task_size + t.result) / Vn
        t.process_t[i] = t.target / performance[i]
        t.energy[i] = t.process_t[i] * comp_Energy[i]
        for j in range(len(que[i])):
            t.que_t[j] += que[j][i]
        if t.que_t[i] >= REQUIREMENT:
            delete_es(i+1)
        else:
            tmp1 = t.com_t[i] + t.que_t[i] + t.process_t[i]
            if tmp1 > REQUIREMENT:
                delete_es(i+1)
    if len(Es) == 0:
        return -1
    elif len(Es) == 1:
        return Es[0]
    else:
        # tmp2 = random.randint(1, len(Es))
        # result = Es[tmp2-1]
        # t.sum_t = t.com_t[result-1] + t.que_t[result-1] + t.process_t[result-1]
        # choose_es(result, t.sum_t)
        # delete_task_in_queue(result, t.sum_t)
        # a = normalization(t.com_t)
        norm_process_t = normalization(t.process_t)
        norm_energy = normalization(t.energy)
        flag = float("inf")
        for i in range(len(Es)):
            tmp = 0.5 * norm_energy[i] + 0.5 * norm_process_t[i]
            if tmp < flag:
                flag = tmp
                result = Es[i]
        choose_es(result, t.sum_t)
        delete_task_in_queue(result, t.sum_t)
        return result


def cec(t):
    IN = dict()
    temp_sum = 0
    weight = dict()
    result = list()
    for i in range(E):
        for j in range(len(que[i])):
            t.que_t[i] += que[i][j]
        instructions = (REQUIREMENT - t.que_t[i] - t.com_t[i]) * performance[i]
        IN[i] = instructions
    # desc = select_main_es(IN)
    # for i in range(E):
    #     temp_sum += desc[i][1]
    #     result.append(desc[i][0] + 1)
    #     if temp_sum > t.target:
    #         break
    # # divide
    # for i in range(len(result)):
    #     t_task = REQUIREMENT - t.que_t[result[i] - 1]
    #     choose_es(result[i], t_task)
    #     delete_task_in_queue(result[i], t_task)
    # # merge
    norm_instructions = normalization(list(IN.values()))
    norm_energy = normalization(1 / t.energy)
    for i in range(E):
        weight[i] = (0.5 * norm_instructions[i] + 0.5 * norm_energy[i])
    desc = select_main_es(weight)
    for i in range(E):
        temp_sum += IN[desc[i][0] + 1]
        result.append(desc[i][0] + 1)
        if temp_sum > t.target:
            break
    # divide
    for i in range(len(result)):
        t_task = REQUIREMENT - t.que_t[result[i] - 1]
        choose_es(result[i], t_task)
        delete_task_in_queue(result[i], t_task)
    # merge
    return result


def delete_es(val):
    if Es.count(val):
        Es.remove(val)


def select_main_es(val):
    tmp = sorted(val.items(), key=lambda x: x[1], reverse=True)
    return tmp


def choose_es(val1, val2):
    que[val1-1].append(val2)


def delete_task_in_queue(val1, val2):
    def tmp(x):
        que[x - 1].popleft()
        # print('时间'+str(val2)+'后结束')
    Timer(val2, tmp, [val1]).start()


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


if __name__ == '__main__':
    start = time.perf_counter()
    initial()
    task = Task(25, 1, 10000)
    result1 = sae(task)
    if result1 != -1:
        print("SAE选中的边缘服务器序号是" + str(result1))
        print("能耗：" + str(task.energy[result1-1]))
        end = time.perf_counter()
        print(end - start)
        sys.exit()
    else:
        result2 = cec(task)
        print("CEC选中的边缘服务器序号是：")
        for q in result2:
            print(q, end=' ')
        end = time.perf_counter()
        print('\n' + str(end - start))
        sys.exit()
