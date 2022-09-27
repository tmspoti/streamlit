import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime
from datetime import datetime
import datetime as dt
import pandas as pd
from dateutil.relativedelta import relativedelta  # to add days or years
from matplotlib import pyplot as plt
st.title("AWS Kühlanlage Sensoren")

start_time = st.slider(
     "Zeitraum auswählen",
     value=(datetime(2020, 7, 20, 0, 0), datetime(2020, 9, 5, 10, 00)),
     format="MM/DD/YY")
# st.write("Start time:", start_time)
start_date = start_time[0]
end_date = start_time[0]

def plot():

    # Datei einlesen
    df = pd.read_csv("KuehlanlageCombined4 (1).csv")

    # alle verschiedenen Dateinamen
    clist = df["Name"].unique().tolist()


    # Dropdownmenü zur Auswahl
    countries = st.sidebar.multiselect("Sensor auswählen", clist)
    st.subheader("Auswahl: {}".format(", ".join(countries)))

    dfs = {country: df[df["Name"] == country] for country in countries}

    # chart 1
    figvibr = go.Figure(layout=go.Layout(title='Vibration zu Zeit', yaxis = dict(
      title = 'Vibration',
      showgrid = True,
      zeroline = True,
      showline = True,
      showticklabels = True,
      gridwidth = 1 )))

    for country, df in dfs.items():
        figvibr = figvibr.add_trace(go.Scatter(x=df["Datetime"], y=df["Vibration RMS Velocity"], name=country))

    # chart 2
    figtemp = go.Figure(layout=go.Layout(title='Temperatur nach Zeit', yaxis = dict(
      title = 'Temperatur',
      showgrid = True,
      zeroline = True,
      showline = True,
      showticklabels = True,
      gridwidth = 1 )))
    for country, df in dfs.items():
        figtemp = figtemp.add_trace(go.Scatter(x=df["Datetime"], y=df["Temperature" ], name=country))

    col1, col2 = st.columns(2)

    col1.plotly_chart(figvibr)    # chart 1
    col2.plotly_chart(figtemp)    # chart 2


plot()
