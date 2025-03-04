# 🌍 Deep Research AI Agentic System  

## 🚀 Overview  
The **Deep Research AI Agentic System** is an advanced research automation tool that utilizes **LangChain**, **LangGraph**, and **Tavily** to gather online information and draft structured responses using an LLM (**Mistral-7B via Together AI**).  

This system features a **dual-agent architecture**:
1. **Research Agent**: Uses Tavily to extract relevant information from the web.
2. **Answer Drafting Agent**: Processes the extracted information and generates a well-structured response.  

## 🛠️ Features  
✅ Automated online research using Tavily Search API  
✅ Dual-agent pipeline for research and response generation  
✅ LLM-powered summarization using **Mistral-7B (Together AI)**  
✅ Uses **LangGraph** for structured agent workflows  
✅ Saves research results in JSON format for reference  

## 📌 Tech Stack  
- **Python**  
- **LangChain** & **LangGraph**  
- **Tavily API**  
- **Together AI (Mistral-7B)**  
- **Streamlit** (for UI)  

## 📦 Installation  
1️⃣ Clone the repository  
```bash
git clone https://github.com/yourusername/deep-research-ai.git
cd deep-research-ai
2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Set up API keys
Create a .env file and add:
TAVILY_API_KEY=your_tavily_api_key  
TOGETHER_API_KEY=your_together_ai_key

4️⃣ Run the application
streamlit run app.py

📜 Usage
Enter a research query in the UI
The Research Agent gathers online information
The Answer Agent drafts a response
The final answer is displayed and saved in JSON format

