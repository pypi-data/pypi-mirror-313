import eyes17.eyes
p = eyes17.eyes.open()

from matplotlib import pyplot as plt
x,y = p.capture1('A1',1000,10)
plt.plot(x,y)
plt.show()
