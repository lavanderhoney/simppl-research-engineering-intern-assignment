import streamlit as st
import plotly.express as px
import pandas as pd
import os
import plotly.io as pio  # Import plotly.io
import plotly.graph_objects as go
import json
import streamlit.components.v1 as components


import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="DataDashboard", page_icon=":bar_chart:",layout="wide")

st.title(":bar_chart: Dashboard")
st.markdown("### Overivew of the Reddit Posts Dataset")

st.write("Below is a word cloud of the most common words in the dataset.")
st.image("plots/word_cloud.png", caption="Figure 1: Word Cloud of the most common words in the dataset")

st.write("Below is a treemap which shows the distribution of the number of posts per subreddit.")
with open("plots/subreddit_posts.html", 'r', encoding="utf-8") as f:
    html_string = f.read()
components.html(html_string, height=600,  width=2000, scrolling=True)

st.write("Below is a line chart which shows the number of posts, with a rolling average of 15 days, over the time period in the given data.")
with open("plots/posts_overtime.html", 'r', encoding="utf-8") as f:
    html_string = f.read()
components.html(html_string, height=600,  width=2000, scrolling=True)

st.write("This is the distribution of topics in each subreddit in the dataset")
with open("plots/topics_in_posts.html", 'r', encoding="utf-8") as f:
    html_string = f.read()
components.html(html_string, height=600,  width=2000, scrolling=True)

with open("plots/crosspost_network.html", 'r', encoding="utf-8") as f:
    html_string = f.read()
components.html(html_string, height=600,  width=2000, scrolling=True)