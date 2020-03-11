#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import time, threading

# # 新线程执行的代码:
# def loop():
#     print('thread %s is running...' % threading.current_thread().name)
#     n = 0
#     while n < 5:
#         n = n + 1
#         print('thread %s >>> %s' % (threading.current_thread().name, n))
#         time.sleep(1)
#     print('thread %s ended.' % threading.current_thread().name)

# print('thread %s is running...' % threading.current_thread().name)
# t = threading.Thread(target=loop, name='LoopThread')
# t.start()
# t.join()
# print('thread %s ended.' % threading.current_thread().name)

# import time, threading

# # 假定这是你的银行存款:
# balance = 0


# def change_it(n):
#     # 先存后取，结果应该为0:
#     global balance
#     balance = balance + n
#     balance = balance - n


# def run_thread(n):
#     for i in range(1000000):
#         change_it(n)


# t1 = threading.Thread(target=run_thread, args=(5, ))
# t2 = threading.Thread(target=run_thread, args=(8, ))
# t1.start()  # 子线程等待调度
# t2.start()
# t1.join()  # 主线程等待子线程执行完毕
# t2.join()
# print(balance)

# import threading
# import time


# def run(n):
#     print("task", n, threading.current_thread())  #输出当前的线程
#     time.sleep(1)
#     print('3s')
#     time.sleep(1)
#     print('2s')
#     time.sleep(1)
#     print('1s')


# strat_time = time.time()

# t_obj = []  #定义列表用于存放子线程实例

# for i in range(3):
#     t = threading.Thread(target=run, args=("t-%s" % i, ))
#     t.start()
#     # t.join()
#     t_obj.append(t)
# """
# 由主线程生成的三个子线程
# task t-0 <Thread(Thread-1, started 44828)>
# task t-1 <Thread(Thread-2, started 42804)>
# task t-2 <Thread(Thread-3, started 41384)>
# """

# for tmp in t_obj:
#     t.join()  #为每个子线程添加join之后，主线程就会等这些子线程执行完之后再执行。

# print("cost:", time.time() - strat_time)  #主线程

# print(threading.current_thread())  #输出当前线程
# """
# <_MainThread(MainThread, started 43740)>
# """


# import threading
# import time


# def run(n):
#     print("task", n)
#     time.sleep(1)  #此时子线程停1s


# for i in range(3):
#     t = threading.Thread(target=run, args=("t-%s" % i, ))
#     t.start()

# time.sleep(0.5)  #主线程停0.5秒
# print(threading.active_count())  #输出当前活跃的线程数
# """
# task t-0
# task t-1
# task t-2
# 4
# """

# import threading
# import time


# def run(n):
#     print("task", n)
#     time.sleep(0.5)  #此时子线程停0.5s


# for i in range(3):
#     t = threading.Thread(target=run, args=("t-%s" % i, ))
#     t.start()

# time.sleep(1)  #主线程停1秒
# print(threading.active_count())  #输出活跃的线程数
# """
# task t-0
# task t-1
# task t-2
# 1
# """


import threading
import time


def run(n):
    print("task", n)
    time.sleep(1)  # 此时子线程停1s
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')


for i in range(3):
    t = threading.Thread(target=run, args=("t-%s" % i, ))
    t.setDaemon(True)  # 把子进程设置为守护线程，必须在start()之前设置
    t.start()

time.sleep(0.5)  # 主线程停0.5秒
print(threading.active_count())  # 输出活跃的线程数
"""
task t-0
task t-1
task t-2
4

Process finished with exit code 0
"""
