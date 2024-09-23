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

col1, col2, col3 = st.sidebar.columns(3)
col1.write('test')
col2.button('Click me')
with st.sidebar.popover('Popover with columns (WORKING)'):
        col1, col2 = st.columns(2)
            col1.write('INSIDE THE POPOVER')
            col2.button('DO SOMETHING')

with col3.popover('Popover with columns (NOT WORKING)'):
            col1, col2 = st.columns(2)
            col1.write('INSIDE THE POPOVER')
            col2.button('DO SOMETHING')
