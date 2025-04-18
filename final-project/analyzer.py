import pandas as pd
from datetime import datetime
import numpy as np

def analyze_chat_data(csv_file):
    # Load the data
    df = pd.read_csv(csv_file)
    
    # Basic statistics
    stats = {
        'total_messages': len(df),
        'unique_customers': len(df[df['sender'] == 'customer']),
        'average_response_time': calculate_response_time(df),
        'issue_distribution': analyze_issues(df),
        'sentiment_distribution': analyze_sentiment(df),
        'daily_activity': analyze_daily_activity(df)
    }
    
    return stats

def calculate_response_time(df):
    # Calculate average response time between customer and agent
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    response_times = []
    for i in range(1, len(df)):
        if df.iloc[i-1]['sender'] == 'customer' and df.iloc[i]['sender'] == 'agent':
            response_times.append((df.iloc[i]['timestamp'] - df.iloc[i-1]['timestamp']).total_seconds())
    
    if response_times:
        return np.mean(response_times)
    return 0

def analyze_issues(df):
    # Count occurrences of each issue category
    return df[df['sender'] == 'customer']['issue_category'].value_counts().to_dict()

def analyze_sentiment(df):
    # Count occurrences of each sentiment
    return df['sentiment'].value_counts().to_dict()

def analyze_daily_activity(df):
    # Group by date and count messages
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    return df.groupby('date').size().to_dict()

def print_analysis(stats):
    print("\n=== Chat Data Analysis ===\n")
    print(f"Total Messages: {stats['total_messages']}")
    print(f"Unique Customers: {stats['unique_customers']}")
    print(f"Average Response Time: {stats['average_response_time']:.2f} seconds\n")
    
    print("=== Issue Distribution ===")
    for issue, count in stats['issue_distribution'].items():
        print(f"{issue}: {count} occurrences")
    
    print("\n=== Sentiment Distribution ===")
    for sentiment, count in stats['sentiment_distribution'].items():
        print(f"{sentiment}: {count} messages")
    
    print("\n=== Daily Activity ===")
    for date, count in stats['daily_activity'].items():
        print(f"{date}: {count} messages")

if __name__ == "__main__":
    stats = analyze_chat_data("chat_data.csv")
    print_analysis(stats)