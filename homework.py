import threading
from philisopher import philisopher
import random
import time
"""
解决哲学家问题的思路,这个哲学家要么一次性
拿五双筷子,要么就别拿
"""

forks = [True,True,True,True,True]
##这个锁至关重要
mutex = threading.RLock()

ph0 = philisopher("Plato",0)
ph1 = philisopher("Socrates",1)
ph2 = philisopher("Virgil",2)
ph3 = philisopher("Hegel",3)
ph4 = philisopher("zhaoyunxi",4)

phs = [ph0,ph1,ph2,ph3,ph4]
for item in phs:
    print("%d号哲学家%s要吃%d碗面条"%(item.ID,item.name,item.noodles))

def takefork(ph):
    #上锁
    mutex.acquire()
    leftfork = forks[ph.ID]
    rightfork = forks[(ph.ID+1)%5]
    if leftfork and rightfork:
        forks[ph.ID] = False
        forks[(ph.ID+1)%5] = False
    mutex.release()
    return (leftfork and rightfork)


def ReadyForDinner(ph):
    while True:
        if takefork(ph):
            noodles = random.randrange(5,10)
            ph.eat(noodles)
            
            print(ph.name,ph.noodles)
            if ph.noodles <= 0:
                forks[ph.ID] = True
                forks[(ph.ID+1)%5] = True
                break
            forks[ph.ID] = True
            forks[(ph.ID+1)%5] = True
        #吃完了开始思考
            ph.think()
            time.sleep(random.randrange(2,5))
        else:
            print("没抢到筷子,只能思考")

def main():
    threads = []
    for i in range(5):
        item = threading.Thread(target=ReadyForDinner,args = (phs[i],))
        item.start()
        threads.append(item)

    for item in threads:
        item.join()


if __name__ == '__main__':
    main()
