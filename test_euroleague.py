import pandas as pd
import numpy as nb
import plotly.express as px
import streamlit as st

data = pd.read_excel("08042023/sportsref_download")
st.write(data)
