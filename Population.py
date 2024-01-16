import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

df = pd.read_csv(URL, dtype={'Quarter': str, 
                            'Canada': np.int32,
                            'Newfoundland and Labrador': np.int32,
                            'Prince Edward Island': np.int32,
                            'Nova Scotia': np.int32,
                            'New Brunswick': np.int32,
                            'Quebec': np.int32,
                            'Ontario': np.int32,
                            'Manitoba': np.int32,
                            'Saskatchewan': np.int32,
                            'Alberta': np.int32,
                            'British Columbia': np.int32,
                            'Yukon': np.int32,
                            'Northwest Territories': np.int32,
                            'Nunavut': np.int32})
quarters = df["Quarter"].str.slice(0,2).drop_duplicates().sort_values()
locations = df.columns[1:]
df['date']=(df['Quarter'].str.slice(3,7)+df["Quarter"].str.slice(1,2)).astype(int)

st.title("Population of Canada")
st.markdown("Source table can be found [here](https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv)")

with st.expander("See full data table"):
    st.write(df.drop(["date"],axis=1))


with st.form("form_key"):
    col1, col2, col3 = st.columns(3)

    col1.write("Choose a starting date")
    starting_quarter = col1.selectbox(key="start_q",label="Quarter",
                             options=quarters,index=2)
    starting_year = col1.slider(key="start_y",value=1991,label="Year",min_value=1991,
                                max_value=2023,step=1)
    
    col2.write("Choose a end date")
    ending_quarter = col2.selectbox(key="end_q",index=0,label="Quarter",
                             options=quarters)
    ending_year = col2.slider(key="end_y",value=2023,label="Year",min_value=1991,
                                max_value=2023,step=1)
    
    col3.write("Choose a location")
    loc = col3.selectbox(key=5, label="Choose a location",
                         options=locations,index=0)
    
    submit_btn = st.form_submit_button(label="Analyze", type="primary")

starting_date = int(str(starting_year)+starting_quarter[-1])
ending_date = int(str(ending_year)+ending_quarter[-1])

if (df['date']==starting_date).any() and (df['date']==ending_date).any():
    if starting_date < ending_date:
        df_set_index = df.set_index("Quarter")

        starting_value_index = starting_quarter+" "+str(starting_year)
        starting_value = df_set_index.loc[starting_value_index,loc]

        ending_value_index = ending_quarter+" "+str(ending_year)
        ending_value = df_set_index.loc[ending_value_index,loc]

        df_date_filtered = df[(df["date"]>=starting_date) & (df["date"]<=ending_date)]

        diff = round((ending_value - starting_value)/starting_value*100,ndigits=2)

        tab1, tab2 = st.tabs(["Population change", "Compare"])

        with tab1:
            tab1.subheader(f"Population change from {starting_quarter} \
                        {starting_year} to {ending_quarter} {ending_year}")
            col1_in_tab1, col2_in_tab1 = st.columns(2)

            with col1_in_tab1:
                st.metric(label=f"{starting_quarter} {starting_year}",
                            value=starting_value)
                st.metric(label=f"{ending_quarter} {ending_year}",
                            value=ending_value,delta=f"{diff}%")
            
            with col2_in_tab1:
                fig, ax = plt.subplots()
                
                ax.plot(df_date_filtered["Quarter"],df_date_filtered[loc])
                ax.set_xticks([ax.get_xticks()[0], ax.get_xticks()[-1]])
                plt.xlabel("Time")
                plt.xticks(rotation=30)
                plt.ylabel("Population")
                st.pyplot(fig)

        with tab2:
            tab2.subheader(f"Compare with other locations")
            locs_selected = st.multiselect(label="Choose other locations",options=locations,
                            default=loc)

            fig, ax = plt.subplots()
            for i in locs_selected:
                ax.plot(df_date_filtered["Quarter"],df_date_filtered[i])
            ax.set_xticks([ax.get_xticks()[0], ax.get_xticks()[-1]])
            plt.xlabel("Time")
            plt.xticks(rotation=30)
            plt.ylabel("Population")
            st.pyplot(fig)
    else:
        st.error("Dates don't work. Start date must come before end date", icon="🚨")    
else:
    st.error('No data available. Check your quarter and year selection', icon="🚨")
