from langchain.tools import tool
from duckduckgo_search import DDGS

@tool
def search_web(query: str) -> str:
    """
    Searches the web for information.
    Use this when you need current information or facts.
    """
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No results found."
        
        formatted = "\n\n".join([
            f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}"
            for r in results
        ])
        return formatted
    except Exception as e:
        return f"Search error: {str(e)}"