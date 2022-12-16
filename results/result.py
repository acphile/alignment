import matplotlib.pyplot as plt
import numpy as np

s = np.loadtxt('opt.csv', delimiter=',', dtype=np.float)
t = np.loadtxt('time.csv', delimiter=',', dtype=np.float)
fig = plt.figure()
l1, = plt.plot(t[:,0], t[:,1], color ='r')
l2, = plt.plot(t[:,0], t[:,3], color ='g')
l3, = plt.plot(t[:,0], t[:,2], color ='b')
plt.legend(handles=[l1,l2,l3],labels=['gloabl','fast','block'],loc='best')
plt.xlabel('Sequence Length', fontweight ='bold', fontsize = 15)
plt.ylabel('Running Time (s)', fontweight ='bold', fontsize = 15)
plt.title('Time Complexity Analysis', fontweight ='bold')

fig = plt.figure()

# set width of bar
barWidth = 0.25

# Set position of bar on X axis
br1 = np.arange(len(s))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

# Make the plot
plt.bar(br1, s[:,1], color ='r', width = barWidth,
		edgecolor ='grey', label ='global')
plt.bar(br2, s[:,3], color ='g', width = barWidth,
		edgecolor ='grey', label ='fast')
plt.bar(br3, s[:,2], color ='b', width = barWidth,
		edgecolor ='grey', label ='block')

# Adding Xticks
plt.xlabel('Sequence Length', fontweight ='bold', fontsize = 15)
plt.ylabel('Score', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(s))],np.array(s[:,0], dtype = np.int))
plt.title('Optimality Analysis', fontweight ='bold')
plt.legend()
plt.show()

plt.show()