
import numpy as np 

colors = ['red', 'blue', 'green', 'orange', 'black', 'magenta', 'brown', 'cyan']

labels = ['Random', 'Eps=0.1', 'Eps=0.05', 'Eps=0.02', 'Eps= 0, q_init =0', 'q_init=2', 'q_init=5', 'altModel', 'altModel_qinit2', 'altModel2', 'Decreasing Eps, q_init =2']


with open("invalidRatio.txt") as f:
    for i in xrange(11):
        count = i+1
        data1 = f.readline()
        content = np.asarray(map(float, data1.split()))
        while count <5:    
            content += np.asarray(map(float,f.readline().split()))
            count += 1
        content = content/5
        if not i in [0,1,2,3,5,6,7,8,9]:            
            plt.plot(content, color= colors[i-4], label = labels[i])
    plt.legend()
    plt.xlabel('Number of Trials')
    plt.ylabel('Fraction of Invalid Moves')
    plt.show()

