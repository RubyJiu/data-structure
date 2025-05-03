import os
import asyncio
from dotenv import load_dotenv
from flask_socketio import SocketIO
from google import genai

# Load environment variables from .env file
load_dotenv()

async def analyze_customer_chats(socketio, customer_id, customer_data):
    """
    Run analysis on customer service chat data and send updates via SocketIO.
    
    Parameters:
    socketio: SocketIO instance for real-time communication
    customer_id: Customer identifier
    customer_data: DataFrame containing customer chat data
    """
    try:
        # Emit status update
        socketio.emit('update', {'message': '🟢 Starting customer chat analysis...'})
        
        # Get API key from environment
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        
        # Create Gemini client
        client = genai.Client(api_key=gemini_api_key)
        model = "gemini-1.5-flash-8b"
        
        # Create analysis prompt with customer data
        avg_sentiment = customer_data["Sentiment_Score"].mean()
        positive_chats = len(customer_data[customer_data["Sentiment_Score"] > 0.3])
        negative_chats = len(customer_data[customer_data["Sentiment_Score"] < -0.3])
        neutral_chats = len(customer_data) - positive_chats - negative_chats
        
        # Get most common categories
        top_categories = customer_data["Category"].value_counts().head(3).to_dict()
        categories_str = ", ".join([f"{cat} ({count} chats)" for cat, count in top_categories.items()])
        
        # Calculate average response time
        avg_response_time = customer_data["Response_Time_Minutes"].mean()
        
        analysis_prompt = f"""
        Analyze the following customer service chat data for customer ID: {customer_id}
        
        Summary statistics:
        - Total number of chats: {len(customer_data)}
        - Average sentiment score: {avg_sentiment:.2f} (range: -1 to 1)
        - Positive chats: {positive_chats}
        - Negative chats: {negative_chats}
        - Neutral chats: {neutral_chats}
        - Top categories: {categories_str}
        - Average response time: {avg_response_time:.2f} minutes
        - Date range: {customer_data['Date'].min()} to {customer_data['Date'].max()}
        
        As a customer service analyst and customer experience expert, please provide:
        1. A detailed analysis of this customer's interaction patterns
        2. Identification of pain points and positive experiences
        3. Specific recommendations for improving this customer's experience
        4. Strategies for customer service representatives to better handle this customer
        
        Format your response in clear sections with headers.
        """
        
        socketio.emit('update', {'message': '🧠 Generating customer service analysis...'})
        
        # Generate analysis using Gemini
        response = client.models.generate_content(
            model=model,
            contents=analysis_prompt
        )
        
        analysis = response.text
        
        # Send updates
        socketio.emit('update', {'message': '📊 Analysis complete!'})
        
        # Send final analysis
        socketio.emit('analysis_complete', {
            'customer_id': customer_id,
            'analysis': analysis
        })
        
        return analysis
        
    except Exception as e:
        socketio.emit('update', {'message': f"❌ Error in analysis: {str(e)}"})
        return f"Error: {str(e)}"

# For standalone testing
if __name__ == '__main__':
    import pandas as pd
    
    # Create dummy data
    data = {
        'Date': pd.date_range(start='2025-01-01', periods=10),
        'Sentiment_Score': [0.8, -0.3, 0.5, -0.7, 0.2, 0.1, -0.5, 0.9, 0.3, -0.2],
        'Category': ['Billing', 'Technical', 'Account', 'Technical', 'Billing', 
                     'Account', 'Technical', 'Billing', 'Account', 'Technical'],
        'Response_Time_Minutes': [5, 12, 3, 15, 8, 4, 20, 6, 7, 10]
    }
    df = pd.DataFrame(data)
    
    # Mock SocketIO
    class MockSocketIO:
        def emit(self, event, data):
            print(f"Event: {event}, Data: {data}")
    
    # Run test
    asyncio.run(analyze_customer_chats(MockSocketIO(), "CUST001", df))
