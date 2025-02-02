import pandas as pd
import numpy.random as rnp
from plotly.subplots import make_subplots
import plotly.graph_objects as go

values_1 = rnp.randint(70, 120, 12)
values_2 = rnp.randint(70, 120, 12)
date_series_1 = pd.date_range(start='1/1/2021', periods=12, freq='M')
date_series_2 = pd.date_range(start='1/1/2021', periods=12, freq='M')
df_1 = pd.DataFrame(data=[date_series_1, values_1]).T
df_1[0] = pd.to_datetime(df_1[0], format='%Y-%m')
df_1[1] = df_1[1].astype('int')
df_1 = df_1.rename(columns={0: 'date', 1: 'value'})
df_1['index'] = 1
df_2 = pd.DataFrame(data=[date_series_2, values_2]).T
df_2[0] = pd.to_datetime(df_2[0], format='%Y-%m')
df_2[1] = df_2[1].astype('int')
df_2 = df_2.rename(columns={0: 'date', 1: 'value'})
df_2['index'] = 2
df_3 = pd.concat([df_1, df_2])

df_4 = df_3.groupby(['index'])['value'].mean().reset_index()
df_4_1 = df_4.loc[0]
df_4_2 = df_4.loc[1]

list_names = ['1', '2']

fig = make_subplots(rows = 1,cols = 2)
fig.add_trace(go.Scatter(x=df_1["date"], y=df_1["value"], name=list_names[0], marker=dict(color='green')),row = 1,col = 1)
fig.add_trace(go.Scatter(x=df_2["date"], y=df_2["value"], name=list_names[1], marker=dict(color='orange')),row = 1,col = 1)
fig.add_trace(go.Bar(x=['1'], y=[df_4_1['value']] , name=list_names[0], marker=dict(color='green'), ),row = 1,col = 2)
fig.add_trace(go.Bar(x=['2'], y=[df_4_2['value']], name=list_names[1], marker=dict(color='orange')),row = 1,col = 2)
fig.update_layout(title = "My first figure", legend=dict(title='Group'))
fig.show()