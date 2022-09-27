import streamlit as st
import pyodbc
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt

st.title("AWWWS Kühlanlage Sensoren")

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )
conn = init_connection()

#Perform query.
#Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from dbo.datavis;")

df = pd.DataFrame((tuple(t) for t in rows))
df.columns =['KorosionsrateSilber', 'RestschichtdickeSilber', 'KorosionsrateKupfer', 'RestschichtdickeKupfer', 'Temperatur', 'Luftfeuchtigkeit', 'Differenzdruck', 't',]

st.write(df.head(10))

plt.plot(df.t[:50], df.Temperatur[:50])

#start_time = st.slider(
#     "Zeitraum auswählen",
#     value=(datetime(2020, 7, 20, 0, 0), datetime(2020, 9, 5, 10, 00)),
#     format="MM/DD/YY")
## st.write("Start time:", start_time)
#start_date = start_time[0]
#end_date = start_time[0]
#
#def plot():
#
#    # alle verschiedenen Dateinamen
#    clist = df["Name"].unique().tolist()
#
#
#    # Dropdownmenü zur Auswahl
#    countries = st.sidebar.multiselect("Sensor auswählen", clist)
#    st.subheader("Auswahl: {}".format(", ".join(countries)))
#
#    dfs = {country: df[df["Name"] == country] for country in countries}
#
#    # chart 1
#    figvibr = go.Figure(layout=go.Layout(title='Vibration zu Zeit', yaxis = dict(
#      title = 'Vibration',
#      showgrid = True,
#      zeroline = True,
#      showline = True,
#      showticklabels = True,
#      gridwidth = 1 )))
#
#    for country, df in dfs.items():
#        figvibr = figvibr.add_trace(go.Scatter(x=df["Datetime"], y=df["Vibration RMS Velocity"], name=country))
#
#    # chart 2
#    figtemp = go.Figure(layout=go.Layout(title='Temperatur nach Zeit', yaxis = dict(
#      title = 'Temperatur',
#      showgrid = True,
#      zeroline = True,
#      showline = True,
#      showticklabels = True,
#      gridwidth = 1 )))
#    for country, df in dfs.items():
#        figtemp = figtemp.add_trace(go.Scatter(x=df["Datetime"], y=df["Temperature" ], name=country))
#
#    col1, col2 = st.columns(2)
#
#    st.plotly_chart(figvibr)    # chart 1
#    st.plotly_chart(figtemp)    # chart 2
#
#
#plot()
