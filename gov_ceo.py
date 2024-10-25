from openai import OpenAI
import streamlit as st

query_params = st.query_params

def generate_solution(departments, concern_text, city):
    # Initialize the OpenAI client correctly
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Define the system prompt
    system_prompt = f"You are the chief executive of the {departments} of {city}. Your goal is to address the following public concern in a professional and effective manner."
    
    # Define the user prompt
    user_prompt = f"""
    Public Concern:
    "{concern_text}"
    
    As the chief executive of the {departments}, provide a detailed action plan to address this concern. The solution should be practical, feasible, and considerate of the community's needs of {city}.
    """
    
    try:
        # Call the OpenAI API with correct syntax
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Changed from gpt-4 to gpt-3.5-turbo
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5  # Adjust as needed
        )
        
        # Extract the response content correctly
        solution = response.choices[0].message.content
        return solution
        
    except Exception as e:
        st.error(f"Error generating solution: {str(e)}")
        return f"Unable to generate solution: {str(e)}"
