from random import randint

for _ in range(10):
    for __ in range(10):
        format = f"input{_}{__}.txt"
        f = open(format, "w")
        n = randint(1, 30)
        n = n * n
        k = n
        f.write(str(n) + " " + str(k) + "\n")
        item = []
        for i in range(n):
            W = randint(1, 20) * 10
            L = randint(1, 20) * 10
            f.write(str(W) + " " + str(L) + "\n")
        for i in range(k):
            W = randint(21, 30) * 10
            L = randint(21, 30) * 10
            C = randint(1, 100)
            f.write(str(W) + " " + str(L) + " " + str(C) + "\n")
        f.close()
    
