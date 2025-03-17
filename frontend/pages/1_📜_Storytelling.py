import streamlit as st
import backoff
import requests
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

load_dotenv()
# Streamlit UI setup
st.set_page_config(page_title="Storytelling", layout="centered", page_icon="📜")

st.title("Storytelling with Data 📜")

st.write("Input a query about the data or some aspect of it, to generate a narrative response. \n This aims to provide insights and analysis based on the available visualizations in the dashboard, and tell a story with data.")
class Response(BaseModel):
    narrative: str
    graphs: List[int]

graphs_descriptions = {
    1:"""This chart shows the number of posts over time across various political subreddits, using a 15-day rolling average to smooth trends. From August 2024 to early 2025, post activity remained low and stable, but around January-February 2025, some subreddits saw a sharp increase, likely due to a major political event.
Key trends:
Politics and socialism subreddits had the biggest spikes.
Democrats and Republican subreddits also grew but more gradually.
PoliticalDiscussion stayed more stable.
When to use this chart:
To analyze online political engagement trends before major events.
To compare subreddit activity over time in response to political changes.
To track how different political communities react to events.""",
2:""" This chart shows how different topic themes are distributed across each political subreddit, using stacked bars to represent the percentage of posts. Each bar (labeled by subreddit on the x-axis) is divided into color-coded segments for topics like personal perspectives on socialism, public opinion on Trump, online racial group dynamics, and more.

Key points:

Each subreddit has a unique topic mix, reflecting community interests (e.g., one may focus more on socialism, another on budget policy).
Bars add up to 100% per subreddit, making it easy to compare dominant conversation themes at a glance.
When to use:

To compare topic focus across political communities.
To understand how different subreddits prioritize or discuss certain political themes.
To spot community-specific trends in political discourse.""",
3: """ This visualization is a network diagram showing how different political subreddits are connected based on their relationships (e.g., shared discussions or user overlap). Each node is a subreddit, and the lines between them represent the strength or frequency of their connections.

Key points:

Nodes closer together or with thicker lines tend to have stronger connections or more shared interest.
Each node is color-coded, making it easy to distinguish subreddits at a glance.
The structure highlights clusters of closely related communities.
When to use:

To see how different political subreddits relate to each other.
To identify clusters or groups that share common topics.
To explore how online communities overlap or diverge in their political discussions.""",
4: """This chart is a **histogram** showing how posts are distributed across **sentiment scores** ranging from **-1** (negative) to **+1** (positive). The y-axis shows the **number of posts** at each sentiment level. Notably, there’s a **tall bar** at **0**, indicating that **most posts** are neutral or close to neutral in sentiment, with fewer posts at the more **positive** or **negative** ends of the scale.

**Key points:**
- **Peak around 0:** Most posts have a **neutral** sentiment.
- **Smaller bars** at both ends: Relatively fewer posts show **strongly positive** or **strongly negative** sentiment.

**When to use:**
- To quickly see how **positive, negative, or neutral** a set of posts is.
- To understand the **overall tone** of conversations in political subreddits.
- As a **starting point** for deeper analysis into why certain posts lean more positive or negative. """,
5: """This heatmap displays how **posts are distributed** across **sentiment score ranges** (x-axis) for each **subreddit** (y-axis). Darker or more intense colors indicate **higher numbers of posts** in that sentiment range.  

Key points:  
- Each row represents a subreddit, each column a **range of sentiment scores** (from negative to positive).  
- The **color scale** shows how many posts fall into each sentiment range.  
- You can quickly see **which sentiment ranges** are most common for each subreddit.  

When to use:  
- To **compare** the **sentiment distribution** across multiple subreddits.  
- To identify which subreddits have **higher negative or positive** sentiment.  
- To **spot trends** in overall tone across different communities. """,
6: """ This line chart shows how the **average sentiment score** changes from **August 2024** to **March 2025**. The x-axis is the date, and the y-axis represents the **mean sentiment** (ranging roughly from negative to positive). Early on, sentiment appears to **fluctuate** with both positive and negative swings. Over time, it tends to **stabilize** closer to **neutral** (around zero), suggesting that overall conversation mood levels out toward the end of the period.

**Key points:**
- **Time-based changes** in sentiment, with notable ups and downs early on.
- Gradual **stabilization** near a neutral score.

**When to use:**
- To understand **how sentiment shifts** over a specific time frame.
- To **identify periods** of heightened negativity or positivity.
- To **correlate sentiment changes** with major events or trends.""",
7: """ This **stacked bar chart** shows how often different **news domains** (x-axis) are shared across various **political subreddits** (color-coded segments). The y-axis represents the **number of shares** for each domain. For example, “self.Conservative” has the highest share count overall, while **reuters.com** also shows a large total. Each bar is divided into sections for subreddits like Conservative, Liberal, Republican, etc., revealing **which communities** share **which sources** most often.

**When to use:**
- To see how **domain popularity** varies by subreddit.  
- To compare **media source usage** across different political communities.  
- To spot **patterns or preferences** in news-sharing behavior.""",
8: """ 
This **pie chart** shows the **overall share** of different **news domains** across all subreddits. Each slice represents a **domain**, with its size indicating the **percentage** of total shares. For instance, **youtube.com** has the largest share, followed by **self.Conservative**, then various news sites like **nytimes.com**, **thehill.com**, and **apnews.com**.

**Key points:**
- It gives a **quick overview** of which domains are most popular.
- It highlights the **dominance** of certain domains compared to others.
- It shows **relative proportions** rather than absolute numbers.

**When to use:**
- To **spot top domains** or sources in an overall dataset.
- To **illustrate the balance** between user-generated (self) content and external news sources.
- To see if **certain outlets** are **heavily favored** across political communities.
"""

}
system_message = SystemMessagePromptTemplate.from_template(
    """
    You are an analytical assistant skilled in interpreting data visualizations and generating insightful narratives based on user queries. 
    You have access to a set of visualizations described below. 
    Your task is to generate a coherent narrative that answers the user’s query, integrating relevant data insights and citing appropriate figures for reference.
    Each figure is identified by a unique figure number and contains valuable information. When citing figures, use the format: (Figure X), where X is the corresponding figure number. 
    Also, for each figure used, return a list containing the figure numbers, like [1,2,3].
    Cite only the most relevant figures that directly support your response.
    Here are the available visualizations:
    {graphs_descriptions}
    Ensure that your response is:
    - Clear and concise, directly answering the query.
    - Well-supported, using figures where necessary.
    - Coherent, presenting a logical flow in the story.
    - Objective, relying on data from the figures without speculation.
    Do not format the output in markdown, do not use triple backticks (` ``` `) or JSON code blocks.
    Ensure that the response is a valid JSON object that follows the expected schema.
    {format_instructions}
    """
)

human_message = HumanMessagePromptTemplate.from_template("Here is the user-query:\n\n{query}\n\nPlease provide a narrative that answers the user's query, integrating relevant data insights and citing appropriate figures for reference.")
parser = JsonOutputParser(pydantic_object=Response)


@backoff.on_exception(backoff.expo, (requests.exceptions.HTTPError, RuntimeError, ValueError), max_tries=3)
def query_gemini(llm, user_input):
    try:
        response = llm.invoke(user_input)
        return response
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            return "⚠️ The AI model is temporarily unavailable. Please try again later."
        else:
            return f"⚠️ Unexpected HTTP error: {e.response.status_code}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a query about the data...")
if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                chat_prompt = ChatPromptTemplate(
                    messages=[system_message, human_message],
                    partial_variables={
                        "query": user_input,
                        "graphs_descriptions": "\n".join([f"{k}: {v}" for k, v in graphs_descriptions.items()]),
                        "format_instructions": parser.get_format_instructions()}
                )
                llm_out = query_gemini(llm, chat_prompt.format_messages())
                parsed_output = parser.invoke(llm_out)
                st.write(parsed_output["narrative"])
            except Exception as e:
                st.write(f"An error occurred: {str(e)}")
        

