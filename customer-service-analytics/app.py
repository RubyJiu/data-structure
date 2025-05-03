import os
import asyncio
import json
import threading
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from google import genai
from visualization import generate_sentiment_plot, generate_category_distribution, generate_response_time_plot
from chat_analysis import analyze_customer_chats

# Initialize Flask and SocketIO
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
socketio = SocketIO(app, async_mode='threading')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load .env and initialize Gemini
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Global variable to store the most recently uploaded data
uploaded_data = {}

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        socketio.emit('update', {'message': '🟢 File uploaded successfully, starting analysis...'})
        threading.Thread(target=background_task, args=(file_path,)).start()
        return 'File uploaded and processing started.', 200

def background_task(file_path):
    try:
        df = pd.read_csv(file_path)

        # Get customer_id from filename (e.g., CUST001.csv -> customer_id = CUST001)
        customer_id = os.path.splitext(os.path.basename(file_path))[0]

        # Store data in global variable for chat context
        global uploaded_data
        uploaded_data = {
            'customer_id': customer_id,
            'df': df,
            'file_path': file_path
        }

        # Generate visualizations
        sentiment_plot_path = generate_sentiment_plot(customer_id, df)
        category_plot_path = generate_category_distribution(customer_id, df)
        response_time_plot_path = generate_response_time_plot(customer_id, df)

        # Notify frontend that plots are ready
        socketio.emit('plots_generated', {
            'sentiment_plot_url': '/' + sentiment_plot_path,
            'category_plot_url': '/' + category_plot_path,
            'response_time_plot_url': '/' + response_time_plot_path
        })

        # Run chat analysis
        asyncio.run(analyze_customer_chats(socketio, customer_id, df))
    except Exception as e:
        socketio.emit('update', {'message': f"❌ Error during analysis: {str(e)}"})
        socketio.emit('chat_response', {
            'message': f"I encountered an error while analyzing the uploaded data: {str(e)}",
            'error': True
        })

# Gemini chat support with real-time responses and data awareness
@socketio.on('chat_message')
def handle_user_chat(data):
    try:
        user_message = data.get('message', '')
        customer_id = data.get('customer_id', None)
        
        # Create a thread to handle the chat response
        def process_chat():
            try:
                # Check if we have data to reference
                if uploaded_data and 'df' in uploaded_data and 'customer_id' in uploaded_data:
                    df = uploaded_data['df']
                    current_customer_id = uploaded_data['customer_id']
                    
                    # Create a context-aware prompt
                    stats_context = f"""
                    You are an AI assistant helping with customer service chat analysis. You have access to the following data for customer {current_customer_id}:
                    
                    Summary statistics:
                    - Total chats: {len(df)}
                    - Average sentiment score: {df['Sentiment_Score'].mean():.2f} (range: -1 to 1)
                    - Most common category: {df['Category'].value_counts().index[0]}
                    - Average response time: {df['Response_Time_Minutes'].mean():.2f} minutes
                    - Date range: {df['Date'].min()} to {df['Date'].max()}
                    
                    Full data (first few rows):
                    {df.head().to_string()}
                    
                    The user is asking: {user_message}
                    
                    Provide a helpful, accurate response based on this customer service data. If they ask about specific dates, categories, sentiment scores, or response times, look at the data and give precise answers.
                    """
                    
                    # Generate response from Gemini with context
                    response = client.models.generate_content(
                        model="gemini-1.5-flash-8b",
                        contents=stats_context
                    )
                else:
                    # No data available, inform the user
                    if "sentiment" in user_message.lower() or "customer" in user_message.lower() or "chat" in user_message.lower():
                        response_text = "I don't have any customer data to analyze yet. Please upload a CSV file first."
                    else:
                        # Generate a general response
                        response = client.models.generate_content(
                            model="gemini-1.5-flash-8b",
                            contents=f"The user asks: {user_message}. Respond helpfully but if they ask about customer data, explain that they need to upload a CSV file first."
                        )
                        response_text = response.text
                
                # Send response back to client
                socketio.emit('chat_response', {
                    'message': response.text if 'response' in locals() and hasattr(response, 'text') else response_text,
                    'timestamp': pd.Timestamp.now().isoformat()
                })
            except Exception as e:
                socketio.emit('chat_response', {
                    'message': f"Error generating response: {str(e)}",
                    'error': True
                })
        
        # Start processing in a separate thread
        threading.Thread(target=process_chat).start()
        return {'status': 'processing'}
    
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# API endpoint for getting customer statistics
@app.route('/api/customer/<customer_id>/stats', methods=['GET'])
def get_customer_stats(customer_id):
    try:
        # Find the customer's data file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{customer_id}.csv")
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Customer data not found'}), 404
            
        # Load and analyze data
        df = pd.read_csv(file_path)
        stats = {
            'customer_id': customer_id,
            'total_chats': len(df),
            'average_sentiment': float(df['Sentiment_Score'].mean()),
            'positive_chats': int(len(df[df['Sentiment_Score'] > 0.3])),
            'negative_chats': int(len(df[df['Sentiment_Score'] < -0.3])),
            'top_category': df['Category'].value_counts().index[0],
            'avg_response_time': float(df['Response_Time_Minutes'].mean())
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/sentiment_charts', exist_ok=True)
    os.makedirs('static/category_charts', exist_ok=True)
    os.makedirs('static/response_time_charts', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
    # Start the application
    socketio.run(app, debug=True)
