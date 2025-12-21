from agents.research_agent import create_research_agent
from utils.config import get_openai_api_key

def main():
    """
    Main execution flow:
    1. Load configuration
    2. Create agent
    3. Get user input
    4. Run agent
    5. Display results
    """
    
    # Load API key
    api_key = get_openai_api_key()
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        return
    
    # Create the agent
    print("Initializing Research Agent...\n")
    agent = create_research_agent(api_key)
    
    # Interactive loop
    print("Research Agent Ready! (type 'exit' to quit)\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            # Run the agent
            response = agent.invoke({"input": user_input})
            print(f"\nAgent: {response['output']}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")

if __name__ == "__main__":
    main()