import sys
import random
import numpy as np
from collections import deque

E = 5																# 所有的边缘服务器数目
Vn = 27					    										# 数据率
REQUIREMENT = 4													    # 时间约束
Es = list()					                						# 供选的边缘服务器集合
performance = np.empty(E, dtype=int)				        		# 每个边缘服务器的性能
que = list()				                       					# 边缘服务器上的排队队列


class Task:
    def __init__(self, val1, val2, val3):
        self.task_size = val1										# 任务大小
        self.result = val2											# 结果大小
        self.target = val3											# 任务总指令数
        self.com_t = np.zeros(E, dtype=float)  						# 通讯时间
        self.process_t = np.zeros(E, dtype=float)  					# 处理时间
        self.que_t = np.zeros(E, dtype=float)  						# 排队时间
        self.sum_t = 0  											# 选定边缘服务器后的总运行时间


def initial():
    for i in range(E):
        Es.append(i+1)
        performance[i] = random.randint(1000, 2000)
        que.append(deque())


def sae(t):
    for i in range(E):
        t.com_t[i] = (t.task_size + t.result) / Vn
        t.process_t[i] = t.target / performance[i]
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
        tmp2 = random.randint(1, len(Es))
        result = Es[tmp2-1]
        t.sum_t = t.com_t[result-1] + t.que_t[result-1] + t.process_t[result-1]
        choose_es(result, t.sum_t)
        delete_task_in_queue(result, t.sum_t)
        return result


def cec(t):
    IN = dict()
    temp_sum = 0
    result = list()
    for i in range(E):
        for j in range(len(que[i])):
            t.que_t[i] += que[i][j]
        instructions = (REQUIREMENT - t.que_t[i] - t.com_t[i]) * performance[i]
        IN[i] = instructions
    desc = select_main_es(IN)
    # main_Es = desc[0][0]
    for i in range(1, E):
        temp_sum += desc[i][1]
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
    pass


if __name__ == '__main__':
    initial()
    task = Task(25, 1, 10000)
    result1 = sae(task)
    if result1 != -1:
        print("1.选中的边缘服务器序号是" + str(result1))
        sys.exit()
    else:
        result2 = cec(task)
        print("2.选中的边缘服务器序号是：")
        for q in result2:
            print(q, end=' ')
        sys.exit()
