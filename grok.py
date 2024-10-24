import streamlit as st
import openai
import datetime as dt
import json

import concern as concern

# Access API keys
api_key = openai.api_key = st.secrets["X_API_KEY"]

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

def __get_completion(prompt: str, system_prompt:str) -> str:
    completion = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message



def __get_concerns_json(sectors, departments, city):
    today = dt.datetime.now()
    response = __get_completion(
        prompt=f"""

        Today is {today}
        
        **Instructions:**

        1. **Monitor Social Media Content:**
           - Focus on posts from residents of **{city}**.
           - Analyze content related to the following sector(s): **{sectors}**.

        2. **Identify Key Concerns:**
           - Extract the main issues or topics that are frequently mentioned or are gaining traction.
           - Pay attention to emerging trends, recurring complaints, or significant events.

        3. **Determine the Degree of Concern:**
           - Assess whether each issue is:
             - 3 - A trending topic (high frequency, widespread discussion).
             - 2 - An emerging concern (growing mentions, increasing attention).
             - 1 - A sporadic mention (infrequent, isolated cases).

        4. **Associate Concerns with Departments:**
           - Match each identified concern with the following appropriate government department responsible for addressing it: **{departments}**.

        5. **Provide Structured Output:**
           - Present the findings in the following JSON format:

             {{
               "sector": "[Sector Name]",
               "department": "[Corresponding Department Name]",
               "concern": "[Brief description of the public concern]",
               "degree": "[Trending/Emerging/Sporadic]"
               "degree_level": [3/2/1]
             }}

        6. **Ensure Anonymity and Privacy:**
           - Do not include any personally identifiable information (PII) from social media users.
           - Summarize content without quoting or referencing specific individuals.

        7. **Maintain Professionalism:**
           - Use clear, concise language suitable for government officials.
           - Focus on actionable insights that can aid in decision-making.

        **Example Output:**
        
        [
          {{
            "sector": "Elderly Services",
            "department": "Department of Aging or Senior Services",
            "concern": "People are increasingly posting about the lack of accessible transportation options for seniors.",
            "degree": "It is becoming a trending issue among the community.
            "degree_level": 3
          }},
          {{
            "sector": "Public Safety",
            "department": "Police Department",
            "concern": "Residents are posting more about delayed emergency response times in certain neighborhoods.",
            "degree": "This concern is emerging as a significant topic on social media."
            "degree_level": 2
          }},
          {{
            "sector": "Housing and Urban Development",
            "department": "Housing Authority",
            "concern": "There is a growing number of posts about the shortage of affordable housing and rising rent prices.",
            "degree": "It's becoming a widespread concern among city residents."
            "degree_level": 3
          }}
        ]
        
        Just output the json.
        """,
        system_prompt="You are an AI assistant designed to help monitor and analyze social media posts related to government-sensitive sectors in a specified city. Your primary goal is to identify and summarize key public concerns that may require attention from the corresponding government departments.",
    )

    json_response = response.content.strip("```json").strip("```")

    print(json_response)
    
    return json.loads(json_response)


# Gets the conserns and returns as list of ```Concern``` objects
def get_concerns(sectors, departments, city):
    data_list = __get_concerns_json(sectors, departments, city)
    # Create a list of Concern instances
    concerns = [concern.Concern.from_dict(item) for item in data_list]

    return concerns
  
  
  
def get_concerns_mock(sectors, city):
    # Mocked response data
    mocked_response = [
      {
        "sector": "Education",
        "department": "South Salt Lake School District",
        "concern": "Parents and teachers are increasingly concerned about overcrowded classrooms affecting educational quality.",
        "degree": "Emerging",
        "degree_level": 2
      },
      {
        "sector": "Public Safety",
        "department": "South Salt Lake Police Department",
        "concern": "A series of posts highlight concerns about the frequency of petty thefts in local parks.",
        "degree": "Sporadic",
        "degree_level": 1
      },
      {
        "sector": "Public Health",
        "department": "South Salt Lake Health Department",
        "concern": "Residents are discussing the need for more accessible mental health services, especially for young adults.",
        "degree": "Emerging",
        "degree_level": 2
      },
      {
        "sector": "Transportation",
        "department": "South Salt Lake Public Works",
        "concern": "Complaints about potholes and deteriorating road conditions are trending, particularly in residential areas.",
        "degree": "Trending",
        "degree_level": 3
      }
    ]
    # Create a list of Concern instances
    concerns = [concern.Concern.from_dict(item) for item in mocked_response]
    
    return concerns