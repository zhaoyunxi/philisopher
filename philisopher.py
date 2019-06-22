import random

class philisopher:
    def __init__(self,name,ID):
        self.ID = ID
        self.name = name
        #这个哲学家要吃的面条数量
        self.noodles = random.randrange(10,50)

    def think(self):
        print("%d号哲学家%s正在思考"%(self.ID,self.name))

    def eat(self,noodles):
        print("%d号哲学家%s开始吃东西,并且吃了%d碗面条"%(self.ID,self.name,noodles))
        self.noodles-=noodles
