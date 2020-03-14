import sys
import random
import numpy as np
from collections import deque
from threading import Timer

a = list()


def task(x):
    print('任务' + str(x) + '结束')


for i in range(1, 6):
    tmp = random.randint(1, 20)
    a.append(tmp)
    print('任务' + str(i) + '开始:')
    Timer(tmp, task, (i, )).start()
    # print('任务' + str(i) + '开始计时:')
print(a)
