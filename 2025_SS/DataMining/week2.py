import pandas as pd
import numpy as np 

s = pd.Series([1,3,5,7,8])

np.random.randn(6,4)

df = pd.DataFrame(np.random.randn(6,4), index=[11,12,14,15,16,17],
columns=['A','B','C','D'])

arr = np.random.randn(6,4)

arr[0]
arr[:,0]

df['A']
df[['A','B']]

df.dtypes

df.head()
df.head(3)

df.tail()
df.tail(3)

df.index
df.columns

df.to_numpy
df.values

df.T

df.sort_index()
df.sort_index(ascending=False)

df2 = pd.DataFrame(np.random.randint(0,3,size(6,4)), columns=['A','B','C','D'])
df2

df2.sort_values(by='A')
df2.sort_values(by=['A', 'B'])

df2.sort_values(by=['A', 'B'], ascending=False)
df2.sort_values(by=['A', 'B'], ascending=[False,True])

df.loc[[11,12]]
df.loc[[11,12].['A','B']]

df.iloc[[0,1]]
df.iloc[[0,1],[0,1]]

df[df['A']> 0]
df[df['B']> 0]

df2[df2['A']==0]
df2[df2['B'].isin([0,1])]

df2['E'] = ["one","one","two","three","four","three"]
df2['F'] = df['A']

type(df['A'])
df['A']

s = pd.Series([1,2,3,4,5,6], index=[1, 3, 5, 7, 9, 11])

df2['F'] = s
s.values
df2['F'] = s.values


df2['E'] = [1,2,3, np.nan, 5,7]
df

df.dropna()

df.fillna(value=5)

df.mean()
df.mean(axis=1)

df.var()
df.std()
df(quantile(0.5))
df(quantile(0.25))
df(quantile(0.75))
df.min()
df.max()

df.describe()

df2['E'].value_counts()

pd.concat((df,df2))

pd.concat((df,df2), axis=1)

left = pd.DataFrame({'key':['one','two','three','four'], 'x1':np.random.rand(4), 'x2':np.random.rand(4)})
right= pd.DataFrame({'key':['one','three','five','six','seven'], 'x3' :np.random.rand(5), 'x4':np.random.rand(5)})

left.merge(right, on=['key'], how='inner')
left.merge(right, on=['key'], how='left')
left.merge(right, on=['key'], how='right')
left.merge(right, on=['key'], how='outer')

df2.groupby(['E'])['A'].mean()
df2.groupby(['E'])['B'].sum()
df2.groupby(['E'])['B'].min()