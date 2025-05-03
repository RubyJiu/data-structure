# Customer Service Analytics Application

A web-based dashboard for analyzing customer service chat data using AI-powered insights.

## Features

- File upload for customer service chat data (CSV format)
- Real-time data visualization with multiple chart types:
  - Sentiment trend analysis
  - Category distribution
  - Response time analysis
- AI-powered chat analysis
- Interactive chat assistant for data inquiries
- Real-time updates via WebSocket communication

## Project Structure

```
customer-service-analytics/
├── app.py                # Main Flask application
├── config.py             # Configuration file
├── chat_analysis.py      # Chat analysis module
├── visualization.py      # Data visualization module
├── static/               # Static files (auto-created)
│   ├── sentiment_charts/     # Sentiment visualizations
│   ├── category_charts/      # Category visualizations
│   └── response_time_charts/ # Response time visualizations
├── templates/            # HTML templates
│   └── index.html        # Main page template
└── uploads/              # Uploaded data files (auto-created)
```

## Requirements

```
flask==2.3.3
flask-socketio==5.3.6
pandas==2.2.0
matplotlib==3.7.2
seaborn==0.12.2
python-dotenv==1.0.0
google-generativeai==0.3.1
werkzeug==2.3.7
```

## Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install flask flask-socketio pandas matplotlib seaborn python-dotenv google-generativeai werkzeug
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Running the Application

1. Activate the virtual environment:
   ```
   .\venv\Scripts\activate
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Data Format

The application expects CSV files with the following columns:
- `Date`: Date of the customer service chat (YYYY-MM-DD format)
- `Sentiment_Score`: Numerical sentiment score (-1.0 to 1.0)
- `Category`: Category of the customer service issue (e.g., Billing, Technical, Account)
- `Response_Time_Minutes`: Time taken to respond to the customer (in minutes)

Example:
```
Date,Sentiment_Score,Category,Response_Time_Minutes
2025-01-01,0.8,Billing,5
2025-01-02,-0.3,Technical,12
2025-01-03,0.5,Account,3
```

## License

MIT
