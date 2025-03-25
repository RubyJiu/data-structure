import os
import json
import time
import pandas as pd
import sys
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

# Load API key from .env file
load_dotenv()

# Define evaluation categories
EVALUATION_CRITERIA = [
    "Greeting & Introduction",
    "Understanding the Issue",
    "Empathy",
    "Clarity of Response",
    "Resolution Provided",
    "Response Time",
    "Professionalism & Politeness",
    "Follow-up Provided"
]

def parse_response(response_text):
    """Parse the JSON response from Gemini API and handle unexpected formats."""
    cleaned = response_text.strip()

    # Debugging: Print the raw response to check what Gemini API is returning
    print("Raw API Response:", cleaned)

    # Ensure we are removing markdown-style code blocks
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    # Try parsing the response into JSON
    try:
        result = json.loads(cleaned)

        # Ensure all expected keys are present
        for item in EVALUATION_CRITERIA:
            if item not in result:
                result[item] = ""

        return result
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}")
        print("Response Text:", cleaned)
        return {item: "" for item in EVALUATION_CRITERIA}  # Return empty values on failure

def select_text_column(df: pd.DataFrame) -> str:
    """Select the most relevant column containing dialogue text."""
    preferred_columns = ["message", "conversation", "chat", "text"]
    for col in preferred_columns:
        if col in df.columns:
            return col
    return df.columns[0]

def process_batch(client, messages: list, delimiter="-----"):
    """Send batched customer support chat logs to Gemini for analysis."""
    prompt = (
        "You are a customer service quality analyst. Assess each chat message based on the following criteria:\n"
        + "\n".join(EVALUATION_CRITERIA) +
        "\n\nFor each chat log, return a JSON response with each criterion as a key (1 for yes, blank for no)."
        f"\nSeparate JSON responses with: {delimiter}\n"
        "Ensure that the response is strictly formatted as valid JSON.\n"
        "Example Response Format:\n"
        "```json\n"
        "{\n"
        '"Greeting & Introduction": "1",\n'
        '"Understanding the Issue": "",\n'
        '"Empathy": "1",\n'
        '"Clarity of Response": "1",\n'
        '"Resolution Provided": "1",\n'
        '"Response Time": "",\n'
        '"Professionalism & Politeness": "1",\n'
        '"Follow-up Provided": ""\n'
        "}\n"
        "```\n"
    )

    batch_text = f"\n{delimiter}\n".join(messages)
    content = prompt + "\n\n" + batch_text

    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=[content])

        # Debugging: Print the full response before processing
        print("Full API Response:", response.text)

        parts = response.text.split(delimiter)
        results = [parse_response(part.strip()) for part in parts if part.strip()]

        # If Gemini returns too many or too few responses, adjust
        if len(results) > len(messages):
            results = results[:len(messages)]
        elif len(results) < len(messages):
            results.extend([{item: "" for item in EVALUATION_CRITERIA}] * (len(messages) - len(results)))

        return results
    except Exception as e:
        print(f"API Call Error: {e}")
        return [{item: "" for item in EVALUATION_CRITERIA} for _ in messages]

def main():
    if len(sys.argv) < 2:
        print("Usage: python support_analysis.py <path_to_csv>")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_csv = "customer_support_analysis.csv"
    if os.path.exists(output_csv):
        os.remove(output_csv)
    
    df = pd.read_csv(input_csv)
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("Missing GEMINI_API_KEY environment variable.")
    client = genai.Client(api_key=gemini_api_key)
    
    text_col = select_text_column(df)
    print(f"Using column '{text_col}' for chat analysis.")
    
    batch_size = 10
    total = len(df)
    for start_idx in range(0, total, batch_size):
        end_idx = min(start_idx + batch_size, total)
        batch = df.iloc[start_idx:end_idx]
        messages = [str(d).strip() for d in batch[text_col].tolist()]
        batch_results = process_batch(client, messages)
        batch_df = batch.copy()
        for item in EVALUATION_CRITERIA:
            batch_df[item] = [res.get(item, "") for res in batch_results]
        if start_idx == 0:
            batch_df.to_csv(output_csv, index=False, encoding="utf-8-sig")
        else:
            batch_df.to_csv(output_csv, mode='a', index=False, header=False, encoding="utf-8-sig")
        print(f"Processed {end_idx}/{total} records.")
        time.sleep(1)
    
    print("Analysis complete. Results saved in:", output_csv)

if __name__ == "__main__":
    main()
