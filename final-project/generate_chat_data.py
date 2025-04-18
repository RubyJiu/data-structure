import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
import json

# Load API key from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Missing GEMINI_API_KEY environment variable.")

client = genai.Client(api_key=gemini_api_key)

def generate_chat_data(num_records=50):
    # Prompt for generating realistic chat data
    prompt = """
    Generate realistic customer support chat data with the following structure:
    - message: The chat message content
    - timestamp: When the message was sent (in ISO format)
    - sender: Either 'customer' or 'agent'
    - issue_category: The type of issue (e.g., 'Technical', 'Billing', 'Account')
    - sentiment: The sentiment of the message ('positive', 'negative', 'neutral')
    
    Generate {num_records} records of chat data in JSON format.
    Return the data as a simple JSON array without any markdown formatting.
    """
    
    # Generate data using Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt.format(num_records=num_records)]
    )
    
    # Clean the response text
    response_text = response.text
    # Remove markdown formatting
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    
    try:
        # Parse the JSON response
        chat_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response text: {response_text}")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(chat_data)
    
    # Save to CSV
    output_file = "chat_data.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    
    print(f"Generated {len(df)} chat records and saved to {output_file}")
    return df

if __name__ == "__main__":
    generate_chat_data()