import sys
import random
import numpy as np
from collections import deque

E = 5																# 所有的边缘服务器数目
Vn = 27					    										# 数据率
REQUIREMENT = 4														# 时间约束
Es = list()					                						# 供选的边缘服务器集合
performance = np.empty(E, dtype=int)				        		# 每个边缘服务器的性能
que = list()				                       					# 边缘服务器上的排队队列


class Task:
	# int num;								                        任务序号
	task_size = 0					                                # 任务大小
	result = 0						                                # 结果大小
	target = 0						                                # 任务总指令数
	com_t = np.zeros(E, dtype=float)						    	# 通讯时间
	process_t = np.zeros(E, dtype=float)				        	# 处理时间
	que_t = np.zeros(E, dtype=float)				            	# 排队时间
	sum_t = 0							                        	# 选定边缘服务器后的总运行时间

	def __init__(self, val1, val2, val3):
		self.task_size = val1
		self.result = val2
		self.target = val3

	def choose_es(self, val):
		que[val-1].append(self.sum_t)

	def delete_task_in_queue(self, val):
		pass


def initial():
	for i in range(E):
		Es.append(i+1)
		performance[i] = random.randint(1000, 2000)
		que.append(deque())


def sae(t):
	for i in range(E):
		t.com_t[i] = (t.task_size + t.result)/Vn
		t.process_t[i] = t.target / performance[i]
		for j in range(que[i].__len__()):
			t.que_t[j] += que[j][i]
		if t.que_t[i] >= REQUIREMENT:
			delete_es(i)
		else:
			tmp1 = t.com_t[i]+t.que_t[i]+t.process_t[i]
			if tmp1 > REQUIREMENT:
				delete_es(i)
	if Es.__len__() == 0:
		return -1
	elif Es.__len__() == 1:
		return 0
	else:
		tmp2 = random.randint(1, Es.__len__())
		result = Es[tmp2-1]
		t.sum_t = t.com_t[result-1]+t.que_t[result-1]+t.process_t[result-1]
		t.choose_es(result)
		t.delete_task_in_queue(result)
		return result


def cec():
	pass


def delete_es(val):
	pass


if __name__ == '__main__':
	initial()
	task = Task(25, 1, 10000)
	result1 = sae(task)
	if result1 != -1:
		print("选中的边缘服务器序号是" + str(result1))
	sys.exit()





