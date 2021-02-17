
def func (x):
    import math
    return (x - math.cos(x))

def bisection (a,b):

    if (func(a) * func(b) >= 0):
        print ("Você não assumiu valores corretos para a e b")
        return
    c = a
    while ((b-a) >= 0.00001):

        c = (a+b)/2

        if (func(c) == 0):
            break
        if (func (c) * func(a) < 0):
            b = c
        else:
            a = c
    print ("O valor de f(x) = x - cos(x) é:", c)

a = 0
b = 1

bisection(a,b)


