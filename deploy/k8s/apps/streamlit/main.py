from datetime import timedelta
from postgres_conn import PostgresHandler
import streamlit as st

st.title("API Usage Dashboard")

postgres_handler = PostgresHandler()
df = postgres_handler.fetch_data()

DATE_FMT = "%Y-%m-%d"
start_time = st.sidebar.date_input("Start date").strftime(DATE_FMT)
end_time = (st.sidebar.date_input("End date") + timedelta(days=1)).strftime(DATE_FMT)

df_filter = df[df["created_at"].between(start_time, end_time, inclusive="both")] 

if df_filter.empty:
    st.write("There are no requests for the selected timeframe. :sleeping:")
else:
    st.subheader("Data Sample")
    st.dataframe(
        df_filter,
        height=(len(df_filter) + 1) * 30,
        use_container_width=True,
        hide_index=True
    )
    st.divider()
    st.subheader("APIs Overview")
    api_counts = df_filter['api_name'].value_counts()
    st.bar_chart(api_counts, horizontal=True, use_container_width=True)