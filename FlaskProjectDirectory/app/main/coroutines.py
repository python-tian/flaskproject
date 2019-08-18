#协程
#生成器
# def hello():
#     for i in (1,10,3):
#         key=yield i
#         print(key)
#         print("helloworld")
# h=hello()
# # print("--------------------")
# # print(next(h))
# # print("--------------------")
# # print(next(h))
# # print("--------------------")
# #send方法
# print("-------------------")
# print(next(h))
# print("-------------------")
# print(h.send(10))
# print("-------------------")
# print(h.send(20))
# print("-------------------")
#在实际工作中，协程需要2个函数,send传参问题，当send被作为第一个执行的时候，参数必须是none，当
#处于send（变量）时，yield执行完i时，也会执行变量。
# def getContent():
#     #获取内容方法
#     while True:
#         url=yield "I have content"
#         print("get content from url:%s"%url)
# def getUrl(g):
#     url_list=["url1","url2","url3","url4","url5"]
#     for i in url_list:
#         print("--------------------")
#         g.send(i)
#         print("--------------------")
#
#
# if __name__=="__main__":
#     g=getContent()
#     print(next(g))
#     getUrl(g)
import gevent
from gevent.lock import Semaphore

# def fun1():
#     for i in range(5):
#         print("I am fun 1 this is %s"%i)
#         gevent.sleep(0)
#
# def fun2():
#     for i in range(5):
#         print("I am fun 2 this is %s"%i)
#         gevent.sleep(0)
# fun1()
# fun2()
#
# # t1=gevent.spawn(fun1)
# # t2=gevent.spawn(fun2)
# #
# # gevent.joinall([t1,t2])
sem=Semaphore(1)
def fun1():
    for i in range(5):
        sem.acquire()
        print("I am fun 1 this is %s"%i)
        sem.release()

def fun2():
    for i in range(5):
        sem.acquire()
        print("I am fun 2 this is %s"%i)
        sem.release()
t1=gevent.spawn(fun1)
t2=gevent.spawn(fun2)

gevent.joinall([t1,t2])

