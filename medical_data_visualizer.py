import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# 1 create relative path and open the .csv
csv_file    = os.path.join(os.path.dirname(os.path.abspath(__file__)),'medical_examination.csv')
df          = pd.read_csv(csv_file)

# 2 create new column to check overweight: above IMC is considered overweight
df['overweight']    = ((df['weight'] / ((df['height'] / 100) ** 2)) > 25.0).astype(int) # .astype is used to asign the value as integer instead of bool (TRUE or FALSE)


# 3 standarization of variables
df['cholesterol'] = (df['cholesterol'] > 1).astype(int) # compare each item of cholesterol: (if > 1 = 1) and (if <= 1 = 0) .astype is used to asign the value as integer instead of bool (TRUE or FALSE)
df['gluc']        = (df['gluc'] > 1).astype(int)        # compare each item of gluc       : (if > 1 = 1) and (if <= 1 = 0) .astype is used to asign the value as integer instead of bool (TRUE or FALSE)

# 4 Draw the Categorical Plot in the draw_cat_plot function.
def draw_cat_plot():

    # 5 Create a DataFrame for the cat plot using pd.melt 
    df_cat = pd.melt(
                frame       = df,
                id_vars     = 'cardio',  
                value_vars  = ['cholesterol','gluc','smoke','alco','active','overweight']
                )

    # 6 Group and reformat the data in df_cat to split it by cardio.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size()
    
    # 7
    df_cat = df_cat.reset_index(name='total')
    chart = sns.catplot(
                        data = df_cat,
                        x = 'variable',
                        y = 'total',
                        hue = 'value',
                        col = 'cardio',
                        kind = 'bar'
                        )
    # 8
    fig = chart.figure

    # 9
    fig.savefig('catplot.png')
    return fig

# 10 Draw the Heat Map in the draw_heat_map function.
def draw_heat_map():
    
    # 11 cleaning data
    df_heat = df[
                (df['ap_lo']  <= df['ap_hi'])                   &
                (df['height'] >= df['height'].quantile(0.025))  &
                (df['height'] <= df['height'].quantile(0.975))  &
                (df['weight'] >= df['weight'].quantile(0.025))  &
                (df['weight'] <= df['weight'].quantile(0.975))
                ]

    # 12 creating correlation matrix
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    fig, ax= plt.subplots(figsize=(12, 10))
    fig.show()
    
    # 15
    sns.heatmap(
                corr,
                mask=mask,
                annot=True,
                fmt=".1f",
                ax=ax
                )


    # 16
    fig.savefig('heatmap.png')
    return fig
