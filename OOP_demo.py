'''
@Description: OOP demo
@Author: Steven
@Date: 2019-12-24 16:13:21
@LastEditors  : Steven
@LastEditTime : 2019-12-31 09:36:27
'''


class OOPDemo:
    def __init__(self, msg):
        print("start init ...")
        self.msg(msg)

    @staticmethod
    def msg(msg):
        print(msg)


if __name__ == "__main__":
    demo = OOPDemo("Hello World!")
