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
    "External Domains": "#domains",
    "Misinformation Analysis": "#misinformation"
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
st.header("Overview", anchor="overview")
st.markdown("""
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
with st.expander("🔎 What does this graph tell us?"):
    st.markdown("""
                🚀 We observe fluctuations in the number of posts. Peaks might correlate with trending topics, news events, or major discussions.\n 
                These peaks appear around Feb 2025
                """)

with open("plots/posts_overtime.html", 'r', encoding="utf-8") as f:
    components.html(f.read(), height=600, width=2000, scrolling=True)

# Section 2: Topic Distribution
st.header("Topic Distribution", anchor="topic-distribution")
st.write("### Distribution of Topics by Subreddit")
st.write("This visualization highlights the most dominant topics in each subreddit, reflecting community interests.")
with st.expander("🔎 What does this graph tell us?"):
        st.markdown("""
                    This bar chart shows which topics are popular among the subreddits.\n 
                    The common topic of discourse among all the subreddits is "Personal Perspectives on Socialism/Anarchism. This gives us an idea of the mindset of the users in these subreddits.\n
                    While there are some topics that are unique to a particular subreddit, there are also some topics that are common across multiple subreddits. This could indicate shared interests or discussions that transcend subreddit boundaries.
                 """)

with open("plots/topics_in_posts.html", 'r', encoding="utf-8") as f:
    components.html(f.read(), height=600, width=2000, scrolling=True)

# Section 3: Narrative Flow
st.header("Narrative Flow", anchor="narrative-flow")
st.write("### Flow of Narratives Across Subreddits")
st.write("This Pyvis graph shows how different narratives spread across subreddits, revealing shared interests or diverging opinions.")
with st.expander("🔎 What does this graph tell us?"):
        st.markdown("""
                    Here the size of the nodes indicates the number of posts in that subreddit. The thickness of the edges indicates the number of posts that are shared between the subreddits. \n
                This gives us an idea of the flow of narratives across different subreddits. \n 
                 The narratives here are defined by the keyowrds in the posts. The graph shows that there are some topics that are common across multiple subreddits, while there are some topics that are unique to a particular subreddit.\n
                 The wordcloud bellow shows the most common keywords and their frequencies. This gives us an idea of the topics that are being discussed in the posts.
                 """)

with open("plots/narrative_spread.html", 'r', encoding="utf-8") as f:
    components.html(f.read(), height=600, width=2000, scrolling=True)
st.image("plots/word_cloud.png", width=800)


# Section 4: Sentiment Analysis
st.header("Sentiment Analysis", anchor="sentiment-analysis")
st.write("This visualization shows how sentiment varies between different subreddits, identifying communities with predominantly positive or negative discussions.")
with st.container():
    with st.expander("🔎 What does this graph tell us?"):
        st.markdown(""" 
                 With these two graphs, we get an overiew of the sentiment distribution across the subreddits and in general.\n
                 It is clear that the posts in the given data are mostly having a neutral sentiment, indicated by the large number of posts in the neutral range in the histogram.\n
                 The heatmap shows the sentiment distribution across the subreddits. The sentiment is mostly neutral across all the subreddits, with some extremes, like r/WorldPolitics being most neutral, r/Socialism being most positive, and r/Liberal being most negative. These are reflected by the color intensity in the heatmap.
                 """)
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
    st.write("### Sentiment Over Time")
    with st.expander("🔎 What does this graph tell us?"):
        st.markdown(""" 
                    This line chart shows how the average sentiment accross all the communities changes over time. \n
                 Intererstingly, the average sentiment is neutral at the time of peak post activity, around Feb 2025. This could indicate that the users are discussing a wide range of topics, with varying sentiments. \n
                 The sentiments fluctuate before this time, indicating that the discussions are varied and not focused on a single topic.
                 """)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.write("#### Avg Sentiment score over time")
            with open("plots/sentiment_avg.html", 'r', encoding="utf-8") as f:
                components.html(f.read(), height=600, scrolling=True)
        with col2:
            st.write("#### Count of positive and negative sentiments over time")
            with open("plots/sentiment_overtime.html", "r", encoding="utf-8") as f:
                components.html(f.read(), height=600, scrolling=True)

st.header("External Domains", anchor="domains")
st.write("What are the most popular domains shared on the posts of this data?")
with st.expander("🔎 What does this graph tell us?"):
    st.markdown(""" 
                These two graphs show from where the redditors are sharing the content. The first graph shows the distribution of domains across the subreddits, while the second graph shows the overall distribution of domains. \n
             We can judge the credibility of information flowing through the subreddits by looking at the domains. Among the top 15 domains, there are no controversial domains used.\n
             The most common domain is youtube.com, used most by r/Republican
             """)
col1, col2 = st.columns(2)
with col1:
    st.write("#### Domain Distribution by Subreddit")
    with open("plots/domain_subreddit.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, scrolling=True)
with col2:
    st.write("#### Overall Domain Distribution")
    with open("plots/domains_piechart.html", 'r', encoding="utf-8") as f:
        components.html(f.read(), height=600, scrolling=True)
        
st.header("Misinformation Analysis", anchor="misinformation")
st.write("To gauge the misinformation in the dataset, I've used a pre-trained BERT model to classify the posts as fake or not.")

st.write("### Fake vs. Real Posts: Counts and Engagement Metrics")
with st.expander("🔎 What does this graph tell us?"):
    st.markdown(""" 
                The graph shows the distribution of fake and real news across the data. \n
             The model has classified the posts as fake or real based on the content. The posts are mostly real, with only a relatively few fake posts. \n
             The bar charts for each engagement metrics,i.e, avg. number of upvote ratio, number of comments, and number of crossposts, such that the count for fake news is comparable to the count for real news. \n
             This gives us an idea of the engagement of the fake news posts compared to the real news posts. \n
             Clearly the fake posts recieve as much engagement as real posts, which shows the typical characteristcs of social media.
             """)
with open("plots/fake_news_bar.html", "r", encoding="utf-8") as f:
    components.html(f.read(), height=600, scrolling=True)
    

st.write("### Scatter Matrix of Engagement Features by Fake/Real Posts")
with st.expander(" 🔎 What does this graph tell us?"):
    st.markdown("""
                This is a scatter plot matrix which compares the relation between the engagement metrics, and the relation to fake/real posts.
                The values of score, num of comments,and crossposts have been normalized in the range of 0-1, to be compatible with upvote-ratio. \n
                It shows if fake vs. real posts exhibit distinct patterns in upvotes, scores, comments, or crossposts. \n
                This can give us an idea of how the engagement metrics are related to the fake/real news posts. \n
                The scatter plot matrix shows that the fake news posts have a similar distribution of engagement metrics as the real news posts. This indicates that the fake news posts are not easily distinguishable based on the engagement metrics alone.  
                """
                )
with open("plots/fake_news_scatter.html", "r", encoding="utf-8") as f:
    components.html(f.read(), height=1200, scrolling=True)