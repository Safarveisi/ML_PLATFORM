from postgres_conn import PostgresHandler
import streamlit as st

st.title("API Usage Dashboard")
st.markdown("""
    <style>
    .main .block-container {
        max-width: 800px;
        padding: 2rem;
        padding-top: 5rem;
    }
    </style>
    """, unsafe_allow_html=True)

postgres_handler = PostgresHandler()
df = postgres_handler.fetch_data()

st.subheader("Data Sample")
st.dataframe(df.head()) 

st.subheader("APIs Overview")
api_counts = df['api_name'].value_counts()
st.bar_chart(api_counts)