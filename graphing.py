import numpy as np
import matplotlib.pyplot as plt



def normal(x, sig, mu):
    return (1/np.sqrt(2*np.pi*sig)*np.exp((-1*(x-mu)**2)/2*sig))



fun1 = np.arange(0,14,0.01)

res1 = normal(fun1,0.2,6)

fun2 = np.arange(8,22,0.01)
res2 = normal(fun2,0.2,16)

plt.plot(fun1,res1, label = 'Load')
plt.plot(fun2,res2, label = 'Resistance')
plt.legend(loc ='best')
plt.savefig("LSD.png")
plt.show()
