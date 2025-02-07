import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df = pd.read_csv(r'Z:\DATASETS\demographic_data.csv')
df = df.drop(['State FIPS Code', 'County FIPS Code', 'Total Population', 'FIPS'], axis=1)

df_state = df
df_state['total_male_population_state'] = df_state.groupby(['State'])['Male Population'].transform('sum')
df_state['total_female_population_state'] = df_state.groupby(['State'])['Female Population'].transform('sum')
df_state['total_white_alone_state'] = df_state.groupby(['State'])['White Alone'].transform('sum')
df_state['total_black_alone_state'] = df_state.groupby(['State'])['Black or African American Alone'].transform('sum')
df_state['total_hispanic_alone_state'] = df_state.groupby(['State'])['Hispanic or Latino'].transform('sum')
df_state = df_state.drop(['Male Population', 'Female Population', 'Total Race Responses',
                          'White Alone', 'Black or African American Alone',
                          'Hispanic or Latino', 'County'], axis=1).drop_duplicates(subset=['State'])

df_state_sex = df_state[['State', 'total_male_population_state', 'total_female_population_state']]
df_state_sex = df_state_sex.T.reset_index()
df_state_sex.columns = df_state_sex.iloc[0]
df_state_sex = df_state_sex.iloc[1:]

df_state_race = df_state[['State', 'total_white_alone_state', 'total_black_alone_state', 'total_hispanic_alone_state']]

df_state_race = df_state_race.T.reset_index()
df_state_race.columns = df_state_race.iloc[0]
df_state_race = df_state_race.iloc[1:]

columns1 = list(df_state_race.columns)[1:]

fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
for i, col in enumerate(columns1):
    fig.add_trace(go.Pie(labels=df_state_race['State'], 
                         values=df_state_race[col], 
                         name=col,
                         legendgroup="group1",
                         legendgrouptitle_text="First Group Title"), row=1, col=1)

for i, col in enumerate(columns1):
    fig.add_trace(go.Pie(labels=df_state_sex['State'], 
                         values=df_state_sex[col], 
                         name=f"{col}_other",
                         legendgroup="group2",
                         legendgrouptitle_text="Second Group Title"), row=1, col=2)

fig.data[0].visible = True
fig.data[2].visible = True

buttons = []
for idx, col in enumerate(columns1):
    visible = [False] * len(fig.data)
    visible[idx] = True
    visible[len(columns1) + idx] = True
    buttons.append(dict(label=col,
                        method="update",
                        args=[{"visible": visible}]))

fig.update_layout(
    updatemenus=[
        dict(
            type="dropdown",
            direction="down",
            showactive=True,
            x=0.1,
            y=1.2,
            buttons=buttons
        )
    ]
)
fig.show()