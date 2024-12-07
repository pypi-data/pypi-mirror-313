import random
def count(list):
    sum = 0
    for i in list:
        sum += i
    return sum



def delete(ls):
    ls.clear()
    return ls
list = [1,2,3,4,5,6]
def jumble(ls):
    for i in range(random.randint(0, ls.__len__()), random.randint(0, ls.__len__())):
        #rnd = random.randint(0, ls.__len__())
        ls[i] = ls[-1] 
    return ls

print(jumble(list))


