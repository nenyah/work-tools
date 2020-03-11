# from multiprocessing import Process
# import os
# import time

# # 子进程要执行的代码
# def run_proc(name):
#     time.sleep(2)
#     print('Run child process %s (%s)...' % (name, os.getpid()))

# if __name__ == '__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Process(target=run_proc, args=('test', ))
#     print('Child process will start.')
#     p.start()
#     p.join()
#     print('Child process end.')

# from multiprocessing import Pool
# import os, time, random

# def long_time_task(name):
#     print('Run task %s (%s)...' % (name, os.getpid()))
#     start = time.time()
#     time.sleep(random.random() * 3)
#     end = time.time()
#     print('Task %s runs %0.2f seconds.' % (name, (end - start)))

# if __name__ == '__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Pool(9)
#     for i in range(10):
#         p.apply_async(long_time_task, args=(i, ))
#     print('Waiting for all subprocesses done...')
#     p.close()
#     p.join()
#     print('All subprocesses done.')

# import subprocess

# print('$ nslookup www.python.org')
# r = subprocess.call(['nslookup', 'www.python.org'])
# print('Exit code:', r)

# import subprocess

# print('$ nslookup')
# p = subprocess.Popen(['nslookup'],
#                      stdin=subprocess.PIPE,
#                      stdout=subprocess.PIPE,
#                      stderr=subprocess.PIPE)
# output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
# print(output)
# print('Exit code:', p.returncode)

# from multiprocessing import Process, Queue
# import os, time, random

# # 写数据进程执行的代码:
# def write(q):
#     print('Process to write: %s' % os.getpid())
#     for value in ['A', 'B', 'C']:
#         print('Put %s to queue...' % value)
#         q.put(value)
#         time.sleep(random.random())

# # 读数据进程执行的代码:
# def read(q):
#     print('Process to read: %s' % os.getpid())
#     while True:
#         value = q.get(True)
#         print('Get %s from queue.' % value)

# if __name__ == '__main__':
#     # 父进程创建Queue，并传给各个子进程：
#     q = Queue()
#     pw = Process(target=write, args=(q, ))
#     pr = Process(target=read, args=(q, ))
#     # 启动子进程pw，写入:
#     pw.start()
#     # 启动子进程pr，读取:
#     pr.start()
#     # 等待pw结束:
#     pw.join()
#     # pr进程里是死循环，无法等待其结束，只能强行终止:
#     pr.terminate()

# from multiprocessing import Process, Value
# import time

# alive = Value('b', False)

# def worker(alive):
#     while alive.value:
#         time.sleep(0.1)
#         print("running")

# if __name__ == '__main__':
#     p = Process(target=worker, args=(alive, ))
#     alive.value = True
#     p.start()
#     time.sleep(1)
#     alive.value = False

from multiprocessing import Pool


def f(x):
    return x * x


if __name__ == '__main__':
    with Pool(processes=4) as pool:
        multiple_results = [pool.apply_async(f, (i, )) for i in range(4)]
        print([res.get() for res in multiple_results])
        pool.close()
        pool.join()
