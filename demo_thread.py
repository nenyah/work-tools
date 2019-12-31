'''
@Description: 线程示例
@Author: Steven
@Date: 2019-11-15 10:28:24
@LastEditors  : Steven
@LastEditTime : 2019-12-31 09:21:42
'''
import time
import threading


def hello(name, t):
    """线程函数"""

    for i in range(10):
        print('Hello, 我是小%s' % name)
        time.sleep(t)


def demo():
    A = threading.Thread(target=hello, args=('A', 1), name='A')
    B = threading.Thread(target=hello, args=('B', 2), name='B')
    C = threading.Thread(target=hello, args=('C', 3), name='C')

    C.setDaemon(True)  # 设置子线程在主线程结束时是否无条件跟随主线程一起退出

    A.start()
    A.join(5)  # 等待A线程结束，若5秒钟后未结束,则代码继续
    B.start()
    C.start()

    time.sleep(20)

    print('进程A%s' % ('还在工作中' if A.is_alive() else '已经结束工作', ))
    print('进程B%s' % ('还在工作中' if B.is_alive() else '已经结束工作', ))
    print('进程C%s' % ('还在工作中' if C.is_alive() else '已经结束工作', ))

    print('下班了。。。')


if __name__ == '__main__':
    demo()
