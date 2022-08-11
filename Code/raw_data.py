import pandas as pd 
import numpy as np
import scipy.stats as st

def get_data():
    df = pd.read_excel('Data/Kantar ML UM norm comp 20220714.xlsx',sheet_name='Sheet1')
    return df

def new_features(df):

    df = df[df['Measure'].str.contains("Box")]

    df["Gender"] = np.where(df["Measure"].str.contains("female"),"Female","Male")
    
    df["Medium_Final"] = np.where(df["Solution"].str.contains("Digital"),"Digital","TV")
    
    df[['Country', 'Format_Other']] = df['Country'].str.split('-', 1, expand=True)
    return df
   
def std_calc(df):
    df ['std'] = round((df['30th percentile']-df_f['Median'])/st.norm.ppf(0.3),1)
    return df

def main():
    df = get_data()
    df_f = new_features(df)
    df_f = std_calc(df_f)
    df_f.to_parquet('Data/Kantar.parquet')

if __name__ == '__main__':
    main()

