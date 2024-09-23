#---------------------------------------------------------------------------------------------------------------------------------
### Authenticator
#---------------------------------------------------------------------------------------------------------------------------------
import streamlit as st
#---------------------------------------------------------------------------------------------------------------------------------
### Import Libraries
#---------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#----------------------------------------

st.set_page_config(initial_sidebar_state = "expanded")

with st.sidebar:
  st.caption('👩🏻‍💼 Clinical trial')
  s1, s2, s3 = st.columns((2.5,1.2,1))
  sb = s1.selectbox('', ['DUMMY'], label_visibility="collapsed")
  with s2.popover("📥"): st.html("<h1>Config</h1>")
  s3.button('💾')
