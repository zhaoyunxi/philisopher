#knn算法

#数据是海伦约会的数据,对此作出一个knn算法
import random
from pylab import mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

k = 6

## 这个可以使得在matplotlib中的中文乱码变成中文
mpl.rcParams['font.sans-serif'] = ['SimHei']
def import_data(filename):
    #取文件中的100个数据
    
    with open(filename) as file:
        data = file.readlines()

    random.shuffle(data)
    dataset = []
    index = 0
    for line in data:
        temp = line.strip()
        item = temp.split("\t")
        if(item != ['']):
            new_item = []
            for a in item:
                new_item.append(float(a))
            dataset.append(new_item)
            index+=1
            if(index == 1000):
                break

    #dataset = normal(dataset)
    
    test = dataset[:len(dataset)//3]
    train = dataset[len(dataset)//3:]
    
    return train,test

#数据归一化
def normal(data):
    dataset = []
    temp = [[],[],[]]
    maxnum = []
    mininum = []
    rangenum = []
    for a in data:
        temp[0].append(a[0])
        temp[1].append(a[1])
        temp[2].append(a[2])
    for b in range(0,3):
       maxnum.append(max(temp[b]))
       mininum.append(min(temp[b]))
    for c in range(0,3):
        rangenum.append(maxnum[c]-mininum[c])
    
    for d in data:
        item = []
        for e in range(0,3):
            item.append((d[e] - mininum[e]) / (maxnum[e] - mininum[e]))
        item.append(d[3])   
        dataset.append(item)
        
    return dataset
        
def distance(x,y):
    a = (x[0] - y[0])**2+(x[1] - y[1])**2+(x[2]-y[2])**2
    return a**0.5

def knn(obj,train):
    dists = []
    item = {"distance":0,"favorability":0}
    result = {1:0,2:0,3:0}
    for a in train :
        item["distance"] = distance(obj,a)
        item["favorability"] = a[3]
        dists.append(item)
    
    dists = sorted(dists,key = lambda item:item['distance'])

    
    for j in range(0,k) :
        if dists[j]["favorability"] == 1 :
           result[1] += dists[j]["distance"] 
        elif dists[j]["favorability"] == 2 :
           result[2] += dists[j]["distance"]
        elif dists[j]["favorability"] == 3 :
           result[3] += dists[j]["distance"]

    print("预计结果为%d---实际结果为%d"%(judge(result),int(obj[3])))
    return judge(result)


def judge(dic):
    a = dic[1]
    b = dic[2]
    c = dic[3]
    if a>b and a>c:
        return 1
    elif b>a and b>c:
        return 2
    elif c>a and c>b:
        return 3

##这个函数要使用在归一化之前 所以要在import_data函数返回train与test
def show_data(train,test):
    '''
    三个特征 飞行里程数 玩游戏时间 冰淇淋公升数
    该可视化函数主要是对训练集进行可视化
    记住每一次运行代码，都要讲figure窗口 放大这样才能看清
    设计了两个figure对象 其中一个是三个2D图 一个是一个3D图
    '''
    fig1 = plt.figure()
    fig1, axes = plt.subplots(nrows=2, ncols=2)
    axes[0,0].set(title = '飞行里程数与玩游戏时间对友好度的影响',xlabel='飞行里程数', ylabel='玩游戏时间')
    axes[0,0].set_xlim([0,100000])
    axes[0,0].set_ylim([0,20])
    
    axes[0,1].set(title = '飞行里程数与冰淇淋对友好度的影响',xlabel = '飞行里程数',ylabel='冰淇淋公升数')
    axes[0,1].set_xlim([0,100000])
    axes[0,1].set_ylim([0,2])
    
    axes[1,0].set(title = '玩游戏时间与冰淇淋对友好度的影响',xlabel = '玩游戏时间',ylabel='冰淇淋公升数')
    axes[1,0].set_xlim([0,20])
    axes[1,0].set_ylim([0,2])
    
    length_train = len(train)
    length_test = len(test)
    
    for a in range(length_train):
        axes[0,0].scatter(train[a][0],train[a][1],color=judge_color(train[a]))
    
    for a in range(length_train):
        axes[0,1].scatter(train[a][0],train[a][2],color=judge_color(train[a]))
    
    for a in range(length_train):
        axes[1,0].scatter(train[a][1],train[a][2],color=judge_color(train[a]))
    #对第一块画板的设计结束下面开始第二块
    fig2 = plt.figure()

    ax = fig2.add_subplot(111,projection='3d')
    ax.set(title='各项特征对于友好度的影响')
    ax.set_xlabel('飞行里程数')
    ax.set_ylabel('玩游戏时间')
    ax.set_zlabel('冰淇淋公升数')
    ax.set_xlim([0,100000])
    ax.set_ylim([0,20])
    ax.set_zlim([0,2])

    #由于我要生成legend所以要特殊处理一下
    for a in range(length_train):
        if train[a][3]==1:
            l1=ax.scatter(train[a][0],train[a][1],train[a][2],color=judge_color(train[a]))
        elif train[a][3]==2:
            l2=ax.scatter(train[a][0],train[a][1],train[a][2],color=judge_color(train[a]))
        else :
            l3=ax.scatter(train[a][0],train[a][1],train[a][2],color=judge_color(train[a]))


    ax.legend(handles=[l1,l2,l3,],labels=['Dislike','Just so so','charming'],loc='best')
    
    
    plt.show()
    
#判断该对象到底该是什么颜色
def judge_color(obj):
    ##红色代表不喜欢 黄色表示一般 绿色表示有魅力
    if obj[3] == 1:
        return 'red'
    elif obj[3] == 2:
        return 'yellow'
    else:
        return 'green'

def judge_label(obj):
    if obj[3]==1:
        return 'Dislike'
    elif obj[3] == 2:
        return 'Just so so'
    else:
        return 'charming'

def main():
    correct = 0
    train_and_test = import_data("data.txt")
    train = train_and_test[0]
    test = train_and_test[1]
    show_data(train,test)
    """
    for a in test :
        m = knn(a,train)
        if m == a[3] :
            correct+=1
    
    print("正确率为{}%".format(correct/len(test)*100))
    """



if __name__ == '__main__':
    main()

