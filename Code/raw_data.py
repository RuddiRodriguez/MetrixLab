import pandas as pd 
import numpy as np
import scipy.stats as st

def get_data():
    df = pd.read_excel('Data/Kantar ML UM norm comp 20220714.xlsx',sheet_name='Sheet1')
    df_r = pd.read_excel('Data/Calculate_BM_Percentiles_Unstereotype 20220705.xlsx',header = 18)
    return df, df_r

def new_features(df):

    df = df[df['Measure'].str.contains("Box")]

    df["Gender"] = np.where(df["Measure"].str.contains("female"),"Female","Male")
    
    df["Medium_Final"] = np.where(df["Solution"].str.contains("Digital"),"Digital","TV")
    
    df[['Country', 'Format_Other']] = df['Country'].str.split('-', 1, expand=True)
    df['Country'] = df['Country'].replace(' ','')
    return df
   
def std_calc(df):
    df ['std'] = round((df['30th percentile']-df['Median'])/st.norm.ppf(0.3),1)
    return df

def cleaning(df):
    dic_country = {'UK':'United Kingdom',
            'US':'USA',
            'United States':'USA',
            'United States of America':'USA',
            }
    df['Country'] = df['Country'].map(dic_country).fillna(df['Country'])
    return df
        


def main():
    df, df_r = get_data()
    df_r = df_r[['Final','Format – other','Country','UM - Female','UM - Male']]
    df_r = cleaning(df_r)
    df_f = new_features(df)
    df_f = std_calc(df_f)
    df_f.to_parquet('Data/Kantar.parquet')
    df_r.to_parquet('Data/BM.parquet')

if __name__ == '__main__':
    main()

