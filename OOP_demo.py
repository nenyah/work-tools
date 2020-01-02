'''
@Description: OOP demo
@Author: Steven
@Date: 2019-12-24 16:13:21
@LastEditors  : Steven
@LastEditTime : 2020-01-02 13:15:08
'''


class OOPDemo:
    name = "OOPDemo"  # 类属性

    def __new__(cls, *args):
        # print("__new__方法被执行")
        return super().__new__(cls)

    def __init__(self, msg):
        self.msg = msg  # 实例属性
        # print("start init ...")
        # OOPDemo.speak(self.msg)

    # 实例方法
    def getmsg(self):
        return self.msg

    # 类方法
    @classmethod
    def getname(cls):
        return cls.name

    # 静态方法
    @staticmethod
    def speak(msg):
        print(msg)


if __name__ == "__main__":
    d1 = OOPDemo("Hello Wolrd!")
    d2 = OOPDemo("Hello Python!")
    d2.name = "Change Demo"
    print(type(d2.name))
    print(hasattr(d2, "name"))
    # print(d1.name)  # 实例调用
    # print(d1.msg)
    # print(d1.getmsg())
    # print(d1.getname())
    # # print(OOPDemo.getmsg()) 类不能调用实例方法
    # print(d2.name)  # 实例调用
    # print(d2.msg)
    # print(d2.getmsg())
    # print(d2.getname())
    # print(OOPDemo.name)  # 类调用属性
    # # print(OOPDemo.msg)
    # print(OOPDemo.getname())  # 类调用类方法
    # OOPDemo.name="类修改"
    # print(d1.name)
    # print(d2.name)
    # print(OOPDemo.name)
