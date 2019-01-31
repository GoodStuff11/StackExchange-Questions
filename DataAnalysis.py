import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Data/SE Questions Physics.txt', error_bad_lines=False, sep='\|\ \ \ \|', engine='python')
print(df)
#print(df['views'].mean()/df['votes'].mean())
#h = df.hist(column='views', bins=50)
#plt.yscale('log')
#plt.show()
