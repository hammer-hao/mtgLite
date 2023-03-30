from model_combat.combat import game
from tqdm import tqdm
import pandas as pd
train_df=pd.DataFrame()
for i in tqdm(range(10000)):
    thisgame=game()
    if len(thisgame.columns)==102:
        train_df=pd.concat([train_df, thisgame.sample(n=1)])
train_df.to_csv('training_df.csv')
gamestate=train_df.iloc[:,:-1]
outcome=train_df.iloc[:,-1]

from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt

pca=PCA(n_components=2)
transformed=pca.fit_transform(gamestate)
fig, ax = plt.subplots(figsize=(6, 6))
sns.scatterplot(x = transformed[:,0], y= transformed[:,1], hue = outcome)
plt.show()


import tensorflow as tf
print("TensorFlow version:", tf.__version__)
print(tf.reduce_sum(tf.random.normal([1000, 1000])))