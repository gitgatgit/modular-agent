from langchain.tools import tool
import os

@tool
def save_report(content: str, filename: str = "report.txt") -> str:
    """
    Saves text content to a file in the output directory.
    Use this to save research reports or summaries.
    """
    try:
        os.makedirs("output", exist_ok=True)
        filepath = os.path.join("output", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"Successfully saved to {filepath}"
    except Exception as e:
        return f"Error saving file: {str(e)}"