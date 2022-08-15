 ##########################################
### Required libraries
##########################################
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

##########################################
### Web app layout
##########################################
st.sidebar.header("Dither Check")
sovdither = st.sidebar.file_uploader(label="Ramform Sovereign dither file")
sftdither = st.sidebar.file_uploader(label="Sanco Swift dither file")
line = st.sidebar.text_input(label="Enter linename name: (ex: 1410B)")
seq = st.sidebar.text_input(label="Enter sequence number: (ex: 003)")
exporting = st.sidebar.button(label="Export the data")
tab1, tab2, tab3 = st.tabs(["Data", "Statistics", "Duplicate"])

##########################################
### The code
##########################################
if sovdither is not None and sftdither is not None:
    with tab1:
        # SOV dither dataframe
        sov = pd.read_csv(sovdither,skiprows=1,usecols=[2,3])
        sov.columns = ["Shot", "Dither"]
        sov["Vessel"] = 1

        # SFT dither dataframe
        sft = pd.read_csv(sftdither,skiprows=1,usecols=[2,3])
        sft.columns = ["Shot", "Dither"]
        sft["Vessel"] = 2
        
        # concatenating the dataframes and sorting by shot
        total = pd.concat(objs=[sov,sft]).sort_values(by="Shot").reset_index().drop("index",axis=1)

        st.text("Final file will look like this:")
        st.table(total)

    with tab2:
        fig = go.Figure(data=go.Scatter(x=total["Shot"], y=total["Dither"]))
        fig.update_layout(xaxis_title="Shots",
             yaxis_title="Dither values (ms)",
             height=600,width=1200,template="seaborn")

        st.table(total["Dither"].describe())
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        dup = sft[sft["Dither"].diff()==0]
        st.table(dup)
        

else:
    st.text("Please upload both files")

##########################################
### Exporting final file
##########################################
if exporting == True:
        # create the final dither.csv file
        total.to_csv(f"C22A{line}{seq}-Dither.csv",index=False)
        st.sidebar.text(f"File C22A{line}{seq}-Dither.csv ready")

        # move the original fither files to the "done" folder
        os.replace(f"R:/Projects/2022040/Navigation/Navproc/dither_check/{sovdither.name}", f"R:/Projects/2022040/Navigation/Navproc/dither_check/done/{sovdither.name}")
        os.replace(f"R:/Projects/2022040/Navigation/Navproc/dither_check/{sftdither.name}", f"R:/Projects/2022040/Navigation/Navproc/dither_check/done/{sftdither.name}")
        os.replace(f"R:/Projects/2022040/Navigation/Navproc/dither_check/C22A{line}{seq}-Dither.csv", f"R:/Projects/2022040/LineLogs/Seq{seq}/C22A{line}{seq}-Dither.csv")
