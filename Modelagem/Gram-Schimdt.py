import numpy as np


w1 = np.array([1,2,0,1])

w2 = np.array([2,-1,5,-1])

w3 = np.array([-1,1,-3,2])

v1 = w1

v2 = w2 - (((w2 @ v1)/(v1 @ v1))*v1)

v3 = w3 - ((w3 @ v1)/(v1 @ v1)*v1) - ((w3 @ v2)/(v2 @ v2)*v2)
print (v1)
print (v2)
print (v3)
print (int(v1 @ v2))
print (int(v1 @ v3))
print (int(v2 @ v3))
