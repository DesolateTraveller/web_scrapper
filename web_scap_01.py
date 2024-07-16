import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from scipy.stats import zscore

# Load the dataset
@st.cache_data(ttl="2h")
def load_file(file):
    file_extension = file.name.split('.')[-1]
    if file_extension == 'csv':
        df = pd.read_csv(file, sep=None, engine='python', encoding='utf-8', parse_dates=True, infer_datetime_format=True)
    elif file_extension in ['xls', 'xlsx']:
        df = pd.read_excel(file)
    else:
        st.error("Unsupported file format")
        df = pd.DataFrame()


file = st.sidebar.file_uploader("**:blue[Choose a file]**",
                                    type=["csv", "xls", "xlsx"], 
                                    accept_multiple_files=False, 
                                    key="file_upload")
if file:
    df = load_file(file)
    st.sidebar.divider()

    # Streamlit app title
    st.title('Anomaly Detection in Time Series Data')

    # Display the raw data
    st.subheader('Raw Data')
    st.write(df)

    # Display the plot of the time series
    st.subheader('Time Series Plot')
    fig = px.line(df, x=df.index, y='Value', title='Time Series Data')
    st.plotly_chart(fig)

# Isolation Forest
st.subheader('Isolation Forest')
if st.checkbox('Detect Anomalies using Isolation Forest'):
    isolation_forest = IsolationForest(contamination=0.01)
    df['anomaly_if'] = isolation_forest.fit_predict(df[['Value']])
    anomalies_if = df[df['anomaly_if'] == -1]
    fig_if = px.scatter(df, x=df.index, y='Value', color='anomaly_if', title='Isolation Forest Anomalies')
    fig_if.add_scatter(x=anomalies_if.index, y=anomalies_if['Value'], mode='markers', name='Anomalies', marker=dict(color='red'))
    st.plotly_chart(fig_if)

# Z-Score
st.subheader('Z-Score')
if st.checkbox('Detect Anomalies using Z-Score'):
    df['z_score'] = zscore(df['Value'])
    df['anomaly_z'] = df['z_score'].apply(lambda x: 1 if np.abs(x) > 3 else 0)
    anomalies_z = df[df['anomaly_z'] == 1]
    fig_z = px.scatter(df, x=df.index, y='Value', color='anomaly_z', title='Z-Score Anomalies')
    fig_z.add_scatter(x=anomalies_z.index, y=anomalies_z['Value'], mode='markers', name='Anomalies', marker=dict(color='red'))
    st.plotly_chart(fig_z)

# DBSCAN
st.subheader('DBSCAN')
if st.checkbox('Detect Anomalies using DBSCAN'):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[['Value']])
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    df['anomaly_db'] = dbscan.fit_predict(df_scaled)
    anomalies_db = df[df['anomaly_db'] == -1]
    fig_db = px.scatter(df, x=df.index, y='Value', color='anomaly_db', title='DBSCAN Anomalies')
    fig_db.add_scatter(x=anomalies_db.index, y=anomalies_db['Value'], mode='markers', name='Anomalies', marker=dict(color='red'))
    st.plotly_chart(fig_db)

# Local Outlier Factor (LOF)
st.subheader('Local Outlier Factor (LOF)')
if st.checkbox('Detect Anomalies using LOF'):
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.01)
    df['anomaly_lof'] = lof.fit_predict(df[['Value']])
    anomalies_lof = df[df['anomaly_lof'] == -1]
    fig_lof = px.scatter(df, x=df.index, y='Value', color='anomaly_lof', title='LOF Anomalies')
    fig_lof.add_scatter(x=anomalies_lof.index, y=anomalies_lof['Value'], mode='markers', name='Anomalies', marker=dict(color='red'))
    st.plotly_chart(fig_lof)

# Sidebar for user inputs
st.sidebar.header('User Inputs')
contamination = st.sidebar.slider('Contamination', 0.01, 0.1, 0.01)
eps = st.sidebar.slider('DBSCAN eps', 0.1, 1.0, 0.5)
min_samples = st.sidebar.slider('DBSCAN min_samples', 1, 20, 5)
n_neighbors = st.sidebar.slider('LOF n_neighbors', 1, 50, 20)

# Update the models with user inputs
if contamination:
    isolation_forest.set_params(contamination=contamination)
    lof.set_params(contamination=contamination)

if eps and min_samples:
    dbscan.set_params(eps=eps, min_samples=min_samples)

if n_neighbors:
    lof.set_params(n_neighbors=n_neighbors)
