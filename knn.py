#knn算法

#数据是海伦约会的数据,对此作出一个knn算法
import random
k = 6
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
            if(index == 100):
                break

    dataset = normal(dataset)
    
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

def main():
    correct = 0
    train_and_test = import_data("data.txt")
    train = train_and_test[0]
    test = train_and_test[1]
    for a in test :
        m = knn(a,train)
        if m == a[3] :
            correct+=1
    
    print("正确率为{}%".format(correct/len(test)*100))


if __name__ == '__main__':
    main()

