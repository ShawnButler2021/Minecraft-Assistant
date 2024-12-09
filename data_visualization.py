import pickle
import pandas as pd
from matplotlib import pyplot as plt

folder = 'base_rewards'
file = 'crafting'

rewards = None
with open(f'{folder}\\{file}.list', 'rb') as f:
	rewards = pickle.load(f)
x_values = [i+1 for i in range(len(rewards))]


data = {'Rewards': rewards}
df = pd.DataFrame(data = data)


df.plot()
plt.title(f'{file.title()} Base Rewards')
plt.show()

