import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="January Flight Statistics",
                   page_icon=":airplane:",
                   layout="wide"
                   )

df = pd.read_excel(
    io='Airline Time Delays.xlsx',
    engine='openpyxl',
    sheet_name='Airline Time Delays',
    nrows=2464 
)

df.columns = df.columns.str.replace(' ', '_')

# ---- Sidebar ---- #
st.sidebar.header("Filters:")

airline = st.sidebar.multiselect(
    "Airlines:",
    options=df["Airline"].unique(),
    default=df["Airline"].unique()
)

dom = st.sidebar.multiselect(
    "Day of the Month:",
    options=df["Day_of_Month"].unique(),
    default=df["Day_of_Month"].unique()
)

dow = st.sidebar.multiselect(
    "Day of the Week:",
    options=df["Day_of_Week"].unique(),
    default=df["Day_of_Week"].unique()
)

df_selection = df.query(
    "Airline == @airline & Day_of_Month == @dom & Day_of_Week == @dow"
)

#st.dataframe(df_selection)

# ---- Main Page ---- #
st.title(":airplane: January Flight Statistics")
st.markdown("##")

# ---- KPIs ---- #
average_delay = round(df_selection["Arrival_Delay"].mean(), 1)
distance_flown = int(df_selection["Distance"].sum())
average_flight_time = round(df_selection["Elapsed_Time"].mean(), 1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average Arrival Delays:")
    st.subheader(f"{average_delay} minutes")
with middle_column:
    st.subheader("Distance Flown this Month:")
    st.subheader(f"{distance_flown:,} kilometers")
with right_column:
    st.subheader("Average Flight Time:")
    st.subheader(f"{average_flight_time} minutes")

st.markdown("---")

# ---- Flights By Airline ---- #
flights_by_airline = df_selection['Airline'].value_counts().reset_index()
flights_by_airline.columns = ['Airline', 'Flights']

airline_flights = px.bar(
    flights_by_airline,
    x="Flights",
    y="Airline",
    orientation="h",
    title="<b>Flights By Airlines This Month</b>",
    color_discrete_sequence=["#ff4b4b"] * len(flights_by_airline),
    template="plotly_white"
)

airline_flights.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# ---- Flight Time By Airline ---- #
flight_time_by_airline = df_selection.groupby(by=["Airline"])[["Elapsed_Time"]].sum().sort_values(by="Elapsed_Time")

airline_time = px.bar(
    flight_time_by_airline,
    x=flight_time_by_airline.index,
    y="Elapsed_Time",
    title="<b>Flight Time By Airlines This Month</b>",
    color_discrete_sequence=["#ff4b4b"] * len(flight_time_by_airline),
    template="plotly_white"
)

airline_time.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(
        showgrid=False,
        title="Flight Time"
    ),  
)

# ---- Putting Charts Next to Each Other ---- #
left_column, right_column = st.columns(2)
left_column.plotly_chart(airline_time, use_container_width=True)
right_column.plotly_chart(airline_flights, use_container_width=True)

# ---- Hide StreamLit Style ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
