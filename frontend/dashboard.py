import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import os
import json

# Set page title and layout
st.set_page_config(
    page_title="Reddit Social Media Insights Dashboard", 
    page_icon=":bar_chart:",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("Navigation")
sections = {
    "Overview": "#overview",
    "Temporal Analysis": "#temporal-analysis",
    "Topic Distribution": "#topic-distribution",
    "Narrative Flow": "#narrative-flow",
    "Sentiment Analysis": "#sentiment-analysis",
    "External Domains": "#domains"
}
for section, link in sections.items():
    st.sidebar.markdown(f"[{section}]({link})", unsafe_allow_html=True)

# JavaScript for smooth scrolling
scroll_script = """
<script>
    function scrollToSection(id) {
        document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
    }
</script>
"""
st.markdown(scroll_script, unsafe_allow_html=True)

# Header and Introduction
st.title("Reddit Social Media Insights Dashboard 🔎")
st.markdown("""
## <a name='overview'>Overview</a>
This dashboard provides insights into Reddit posts, analyzing trends, topics, and sentiment across different subreddits. 
It aims to explore:
- The temporal trends in post activity
- The distribution of topics across subreddits
- The flow of narratives connecting different communities
- The sentiment expressed by users over time
""", unsafe_allow_html=True)

# Section 1: Temporal Analysis
st.header("Temporal Analysis", anchor="temporal-analysis")
st.write("### Number of Posts Over Time")
st.write("This line chart shows the number of posts over time, including a 15-day rolling average to identify trends.")
with open("plots/posts_overtime.html", 'r', encoding="utf-8") as f:
    components.html(f.read(), height=600, width=2000, scrolling=True)

# Section 2: Topic Distribution
st.header("Topic Distribution", anchor="topic-distribution")
st.write("### Distribution of Topics by Subreddit")
st.write("This visualization highlights the most dominant topics in each subreddit, reflecting community interests.")
with open("plots/topics_in_posts.html", 'r', encoding="utf-8") as f:
    components.html(f.read(), height=600, width=2000, scrolling=True)

# Section 3: Narrative Flow
st.header("Narrative Flow", anchor="narrative-flow")
st.write("### Flow of Narratives Across Subreddits")
st.write("This Pyvis graph shows how different narratives spread across subreddits, revealing shared interests or diverging opinions.")
with open("plots/narrative_spread.html", 'r', encoding="utf-8") as f:
    components.html(f.read(), height=600, width=2000, scrolling=True)

# Section 4: Sentiment Analysis
st.header("Sentiment Analysis", anchor="sentiment-analysis")
st.write("This visualization shows how sentiment varies between different subreddits, identifying communities with predominantly positive or negative discussions.")
with st.container():
    col1, col2= st.columns(2)
    with col1:
        st.write("#### Sentiment Distribution")
        with open("plots/sentiment_histogram.html", 'r', encoding="utf-8") as f:
            components.html(f.read(), height=600, width=800, scrolling=True)
    with col2:
        st.write("#### Sentiment Heatmap")
        with open("plots/sentiment_heatmap.html", 'r', encoding="utf-8") as f:
            components.html(f.read(), height=600, width=800, scrolling=True)
    st.markdown('<div style="margin-top: -100px;"></div>', unsafe_allow_html=True) 
    st.write("#### Average Sentiment Score Over Time")
    with open("plots/sentiment_avg.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, scrolling=True)

st.header("External Domains", anchor="domains")
st.write("What are the most popular domains shared on the posts of this data?")
col1, col2 = st.columns(2)
with col1:
    st.write("#### Domain Distribution by Subreddit")
    with open("plots/domain_subreddit.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, scrolling=True)
with col2:
    st.write("#### Overall Domain Distribution")
    with open("plots/domains_piechart.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, scrolling=True)