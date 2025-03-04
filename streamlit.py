import json
import streamlit as st
from datetime import datetime
from langchain_community.llms import Together
from langchain.tools import TavilySearchResults
from langgraph.graph import StateGraph
from langchain.pydantic_v1 import BaseModel

# Load API keys from Streamlit secrets
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

# Initialize free LLM (Together AI - Mistral-7B)
llm = Together(model="mistralai/Mistral-7B-Instruct-v0.2", together_api_key=TOGETHER_API_KEY)

# Define State Schema for LangGraph
class ResearchState(BaseModel):
    query: str
    results: str = ""  # Stores search results
    sources: list = []  # Stores URLs of sources
    response: str = ""  # Stores final answer

# Define Research Agent (Collects information)
def research_agent(state: ResearchState):
    try:
        search_tool = TavilySearchResults(api_key=TAVILY_API_KEY)
        search_results = search_tool.run(state.query)  # Fetch results

        extracted_results = []
        sources = []

        for result in search_results:
            extracted_results.append(result["content"])  # Extract text
            sources.append(result["url"])  # Extract URL

        return ResearchState(
            query=state.query,
            results="\n".join(extracted_results),
            sources=sources
        )
    except Exception as e:
        st.error(f"Error in research agent: {e}")
        return state

# Define Answer Drafting Agent (Processes and drafts response)
def answer_agent(state: ResearchState):
    try:
        sources_text = "\n".join(state.sources)  # Format sources
        prompt = f"""
        Based on the research findings below, draft a well-structured answer:
        Query: {state.query}
        Research Data: {state.results}
        Sources: {sources_text}
        """
        response = llm.predict(prompt)
        
        return ResearchState(
            query=state.query,
            results=state.results,
            sources=state.sources,
            response=response
        )
    except Exception as e:
        st.error(f"Error in answer agent: {e}")
        return state

# Create Agent Graph with Schema
graph = StateGraph(ResearchState)
graph.add_node("research", research_agent)
graph.add_node("answer", answer_agent)
graph.add_edge("research", "answer")
graph.set_entry_point("research")

# Compile the graph
research_pipeline = graph.compile()

# Function to execute research pipeline
def execute_agents(query):
    initial_state = ResearchState(query=query).dict()  # Convert to dictionary
    final_state = research_pipeline.invoke(initial_state)  # Invoke pipeline

    # Extract results properly
    final_answer = final_state["response"]
    search_results = final_state["results"]
    sources = final_state["sources"]

    # Save results locally
    save_results(query, search_results, sources, final_answer)

    return final_answer, sources

# Function to save results locally as JSON
def save_results(query, search_results, sources, final_answer):
    data = {
        "query": query,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "search_results": search_results,
        "sources": sources,
        "final_answer": final_answer
    }
    filename = f"research_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Results saved to {filename}")

# Streamlit UI
st.title("🔍 Deep Research AI Agentic System")
query = st.text_input("📌 Enter your research topic:")

if st.button("🚀 Run Research"):
    if query:
        st.write("🔍 Searching... Please wait.")
        result, sources = execute_agents(query)

        st.subheader("📌 Final Answer:")
        st.write(result)

        if sources:
            st.subheader("📄 Sources:")
            for url in sources:
                st.markdown(f"🔗 [{url}]({url})", unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please enter a research topic.")
