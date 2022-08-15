# MetrixLab

## Usage 

1- Create the conda enviroment using the venv.yml file
*  conda env create -file path/venv.yml --p path/venv

2- Activate the conda enviroment. 
* conda env activate path/venv

3- Inside the conda enviroment run:
* streamlit run path/Dashboard.py

## Notes
### Percentile calculation for the new scores

z = (mu - score) / std
percentile = scipy.stats.norm.cdf (z)

Even thought the raw data is the 30th,70th and 50th percentile

To calculate the std we use the following formula:

std = (mu - score) / z=st.norm.ppf(0.3="30th")

we colud assume a perfect normality then std/2 = median-30th percentile, the above defintion is more general and account for some dviation from normality.

### Data transformations

From the original excel files few features were extracted and others were created.

From the Kantar file:   
1- Column solution was used to create the Medium_Final column Digital/TV.  
2- With the column measure the Gender feature was created and only the aggregates values were selected for the final table.
~~~~
df = df[df['Measure'].str.contains("Box")]

df["Gender"] = np.where(df["Measure"].str.contains("female"),"Female","Male")
~~~~

### Data structure.

The final files were saved as parquet files.

## Issues

1- A better solution must be implemented to split the column country into Country/Format  
2- To Round all the numeric values  
3- The percentiles must be show like 30th instead of a number   


