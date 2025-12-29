from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.web_search import search_web
from tools.file_writer import save_report

def create_research_agent(api_key: str):
    """
    Creates a research agent with web search and file writing capabilities.
    
    Flow:
    1. Receives user question
    2. Decides if it needs to search web
    3. Synthesizes information
    4. Optionally saves report
    5. Returns answer
    """
    
    # Define the LLM
    llm = ChatOpenAI(
        model="gpt-5.2",
        temperature=0,
        api_key=api_key
    )
    
    # Define available tools
    tools = [search_web, save_report]
    
    # Create system prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research assistant. 
        Use the search_web tool to find information when needed.
        Use the save_report tool to save your findings if the user asks.
        Be concise and cite sources."""),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # Create executor (runs the agent loop)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5
    )
    
    return agent_executor
