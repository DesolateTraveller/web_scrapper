import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from scipy.stats import zscore

# Function to load data
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

# Streamlit app title
st.title('Anomaly Detection in Time Series Data')

# Sidebar for user inputs
st.sidebar.header('User Inputs')
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=['csv'])

contamination = st.sidebar.slider('Contamination', 0.01, 0.1, 0.05, key='contamination')
eps = st.sidebar.slider('DBSCAN eps', 0.1, 1.0, 0.5, key='eps')
min_samples = st.sidebar.slider('DBSCAN min_samples', 1, 20, 5, key='min_samples')
n_neighbors = st.sidebar.slider('LOF n_neighbors', 1, 50, 20, key='n_neighbors')

if uploaded_file is not None:
    df = load_data(uploaded_file)
    target_variable = st.sidebar.multiselect("**Target (Dependent) Variable**", df.columns, default='value')

    # Display the raw data
    st.subheader('Raw Data')
    st.write(df)


    # Function to plot anomalies
    def plot_anomalies(df, color_column, title):
        fig = px.scatter(df, x=df.index, y='Value', color=color_column, title=title, template="plotly_dark")
        anomalies = df[df[color_column] == -1]
        fig.add_scatter(x=anomalies.index, y=anomalies['Value'], mode='markers', name='Anomalies', marker=dict(color='red', size=10))
        st.plotly_chart(fig)

    # Isolation Forest
    st.subheader('Isolation Forest')
    if st.checkbox('Detect Anomalies using Isolation Forest'):
        isolation_forest = IsolationForest(contamination=contamination)
        df['anomaly_if'] = isolation_forest.fit_predict(df[['Value']])
        plot_anomalies(df, 'anomaly_if', 'Isolation Forest Anomalies')

    # Z-Score
    st.subheader('Z-Score')
    if st.checkbox('Detect Anomalies using Z-Score'):
        df['z_score'] = zscore(df['Value'])
        df['anomaly_z'] = df['z_score'].apply(lambda x: 1 if np.abs(x) > 3 else 0)
        plot_anomalies(df, 'anomaly_z', 'Z-Score Anomalies')

    # DBSCAN
    st.subheader('DBSCAN')
    if st.checkbox('Detect Anomalies using DBSCAN'):
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df[['Value']])
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        df['anomaly_db'] = dbscan.fit_predict(df_scaled)
        plot_anomalies(df, 'anomaly_db', 'DBSCAN Anomalies')

    # Local Outlier Factor (LOF)
    st.subheader('Local Outlier Factor (LOF)')
    if st.checkbox('Detect Anomalies using LOF'):
        lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
        df['anomaly_lof'] = lof.fit_predict(df[['Value']])
        plot_anomalies(df, 'anomaly_lof', 'LOF Anomalies')


else:
    st.info('Please upload a CSV file to proceed.')
