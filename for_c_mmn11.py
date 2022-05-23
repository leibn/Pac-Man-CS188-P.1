import random
import numpy
for i in range(1,10,1):
    f = open("test"+str(i), 'w')
    print(str(i))
    f1=[]
    f2=[]
    for j in range(1,i+1,1):
        f1[i]=random.randint(-10,10)
        print(str(f1[i]))
    for r in range(1,i+1,1):
        f1[r] = random.randint(-10, 10)
        print(str(f1[r]))
    
    print("\n\n\n")


