import pandas as pd 
import streamlit as st
import numpy as np
import scipy.stats as sta
import matplotlib.pyplot as plt

st.set_page_config(page_title='Kantar', page_icon=':email', layout="wide") 

st.info ("""## Warning the underliying assumption is that the data is normally distributed """)

def get_data():
    df = pd.read_parquet('/Users/ruddirodriguez/Documents/MetrixLab/Data/Kantar.parquet')
    df['Country'] = df['Country'].str.rstrip()
    df_bm = pd.read_parquet('/Users/ruddirodriguez/Documents/MetrixLab/Data/BM.parquet')
    return df,df_bm

df,df_bm = get_data()

st.sidebar.markdown("## Select a country")

country_list = df.Country.unique()
country = st.sidebar.selectbox("Country", country_list,index=0)

df_f = df[(df['Country'] == country) ]

st.sidebar.markdown("## Select a Medium")

Medium_Final_list = df_f.Medium_Final.unique()
Medium_Final = st.sidebar.selectbox("Medium", Medium_Final_list,index=0)

st.sidebar.markdown("## Select a Gender")

Gender_list = df_f.Gender.unique()
Gender = st.sidebar.selectbox("Gender", Gender_list,index=0)

#st.sidebar.markdown("## Select a Format")

Format_Other_list = df_f.Format_Other.unique()
Format_Other = st.sidebar.selectbox("Format", Format_Other_list,index=0)

df_ff = df_f[(df_f['Medium_Final'] == Medium_Final) & (df_f['Gender'] == Gender) & (df_f['Format_Other'] == Format_Other)]


score = st.number_input("Score",min_value=0,max_value=100,value=50)
st.info("""
  ### Reference Values    
   """)
try:
    st.dataframe(df_f[['30th percentile','Median','70th percentile','std']].head(1))

    percentile = (1-sta.norm.cdf(-(score - df_ff['Median'])/df_ff['std']))*100

    st.metric("Percentile of the new Score", percentile)
except Exception as e:
    st.info("""
    ## There are not enough data to calculate the percentile    
     """)
    

df_bmm = df_bm.groupby('Country').filter(lambda x : len(x)>8).copy()
df_bmmm = df_bmm[(df_bmm['Country'] == country) ]
alpha = 0.05

def plot_hist(data):
    fig, ax = plt.subplots()
    ax.hist(data)
    return fig



if df_bmmm.shape[0]<8:
    st.info("""
    ## There are not enough data to determine if the underlying distributon is Gausian or not , use it with caution   
     """)
     

else:
    if Gender  == "Female":

        k2, p = sta.shapiro(df_bmmm.dropna()['UM - Female'])
        if p > alpha:
	        st.info('Sample looks Gaussian (fail to reject H0) p > 0.05')
        else:
	        st.info('Sample does not look Gaussian (reject H0) p < 0.05') 
        fig = plot_hist(df_bmmm.dropna()['UM - Female'])
        st.pyplot(fig)
    else: 
        k2, p = sta.shapiro(df_bmmm.dropna()['UM - Male'])
        if p > alpha:
	        st.info('Sample looks Gaussian (fail to reject H0) p > 0.05')
        else:
	        st.info('Sample does not look Gaussian (reject H0) p < 0.05 ') 
        fig = plot_hist(df_bmmm.dropna()['UM - Male'])    
        st.pyplot(fig)
    st.metric("p-value", p) 


  

         



