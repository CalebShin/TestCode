import operator

def nightshift(works):
    index, value = max(enumerate(works), key=operator.itemgetter(1))
    if value > 0 : works[index]-=1
        

def nightshift_fatigue(works, time):
    for i in range(time):
        nightshift(works)

    return sum([num * num for num in works])

if __name__ == "__main__":        
    print(nightshift_fatigue([4,3,3],4))
    print(nightshift_fatigue([2,1,2],1))
    print(nightshift_fatigue([1,1],3))

