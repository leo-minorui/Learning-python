"""
与前一个test文件相比，mutex对象变成了共享对象而非全局的对象，有助于提升健壮性

"""

import _thread,time

stdoutmutex = _thread.allocate_lock()
numthreads = 5
exitmutexes = [_thread.allocate_lock() for i in range(numthreads)]


def counter(myId, count, mutex):
    for i in range(count):
        time.sleep(1 / (myId+1))
        with mutex:                          #上下文管理器
            print('[%s] => %s' % (myId, i))
    exitmutexes[myId].acquire()

for i in range(numthreads):
    _thread.start_new_thread(counter,(i, 5, stdoutmutex))

while not all(mutex.locked() for mutex in exitmutexes): time.sleep(0.25)  #all()判断所有的可迭代参数是否为True
print("Main thread exitting.")