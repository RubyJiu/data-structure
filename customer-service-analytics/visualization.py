import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configure matplotlib backend and font
matplotlib.use('Agg')
matplotlib.rc('font', family='Microsoft JhengHei')  # Use Microsoft JhengHei for Chinese characters

def generate_sentiment_plot(customer_id, customer_data):
    """
    Generate a trend chart based on customer service chat sentiment and save as a .png file.
    
    Parameters:
    customer_id (str): Customer ID or name
    customer_data (DataFrame): DataFrame containing 'Date', 'Sentiment_Score', and 'Category' columns
    
    Returns:
    output_path (str): Path to the saved image file
    """

    # Set output directory
    output_dir = "static/sentiment_charts"
    os.makedirs(output_dir, exist_ok=True)

    # Process data
    customer_data["Date"] = pd.to_datetime(customer_data["Date"], errors="coerce")
    customer_data["Sentiment_Score"] = pd.to_numeric(customer_data["Sentiment_Score"], errors="coerce")

    # Calculate average sentiment
    avg_sentiment = customer_data["Sentiment_Score"].mean()

    # Create plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(x="Date", y="Sentiment_Score", data=customer_data, marker="o", label="Sentiment Scores", color="blue", errorbar=None)
    plt.axhline(y=avg_sentiment, color='orange', linestyle='--', label=f"Average Sentiment ({avg_sentiment:.2f})")
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score")
    plt.title(f"Customer {customer_id} - Sentiment Trend Analysis")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.ylim(-1, 1)  # Set sentiment score range to -1 to 1

    # Save image
    output_path = os.path.join(output_dir, f"sentiment_{customer_id}.png")
    plt.savefig(output_path)
    plt.close()

    return output_path

def generate_category_distribution(customer_id, customer_data):
    """
    Generate a pie chart showing the distribution of customer service categories.
    
    Parameters:
    customer_id (str): Customer ID or name
    customer_data (DataFrame): DataFrame containing 'Category' column
    
    Returns:
    output_path (str): Path to the saved image file
    """
    
    # Set output directory
    output_dir = "static/category_charts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Count categories
    category_counts = customer_data["Category"].value_counts()
    
    # Create plot
    plt.figure(figsize=(10, 7))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', 
            shadow=True, startangle=90, colors=sns.color_palette("pastel"))
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title(f"Customer {customer_id} - Service Category Distribution")
    plt.tight_layout()
    
    # Save image
    output_path = os.path.join(output_dir, f"categories_{customer_id}.png")
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def generate_response_time_plot(customer_id, customer_data):
    """
    Generate a bar chart showing average response times by category.
    
    Parameters:
    customer_id (str): Customer ID or name
    customer_data (DataFrame): DataFrame containing 'Category' and 'Response_Time_Minutes' columns
    
    Returns:
    output_path (str): Path to the saved image file
    """
    
    # Set output directory
    output_dir = "static/response_time_charts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate average response time by category
    avg_response_times = customer_data.groupby("Category")["Response_Time_Minutes"].mean().sort_values(ascending=False)
    
    # Create plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=avg_response_times.index, y=avg_response_times.values, palette="viridis")
    plt.xlabel("Category")
    plt.ylabel("Average Response Time (minutes)")
    plt.title(f"Customer {customer_id} - Average Response Time by Category")
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    plt.tight_layout()
    
    # Save image
    output_path = os.path.join(output_dir, f"response_time_{customer_id}.png")
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def generate_operator_performance_plot(operator_data):
    """
    Generate a bar chart showing operator performance metrics.
    
    Parameters:
    operator_data (DataFrame): DataFrame containing operator performance data
    
    Returns:
    output_path (str): Path to the saved image file
    """
    
    # Set output directory
    output_dir = "static/operator_charts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate metrics for each operator
    operator_metrics = operator_data.groupby("Operator_Name").agg({
        "Sentiment_Score": ['mean', 'count'],
        "Response_Time_Minutes": 'mean'
    }).round(2)
    
    operator_metrics.columns = ['avg_sentiment', 'total_chats', 'avg_response_time']
    operator_metrics = operator_metrics.sort_values(by='avg_sentiment', ascending=False)
    
    # Create plot
    plt.figure(figsize=(12, 8))
    
    # Create a grid for subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot average sentiment
    sns.barplot(x=operator_metrics.index, y=operator_metrics['avg_sentiment'], ax=ax1, palette="viridis")
    ax1.set_title("Operator Performance - Average Sentiment")
    ax1.set_ylabel("Average Sentiment Score")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    ax1.grid(True, axis='y')
    
    # Plot response time
    sns.barplot(x=operator_metrics.index, y=operator_metrics['avg_response_time'], ax=ax2, palette="viridis")
    ax2.set_title("Operator Performance - Average Response Time")
    ax2.set_ylabel("Average Response Time (minutes)")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
    ax2.grid(True, axis='y')
    
    plt.tight_layout()
    
    # Save image
    output_path = os.path.join(output_dir, "operator_performance.png")
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def generate_customer_complaints_plot(customer_data):
    """
    Generate a bar chart showing customer complaint patterns.
    
    Parameters:
    customer_data (DataFrame): DataFrame containing customer data
    
    Returns:
    output_path (str): Path to the saved image file
    """
    
    # Set output directory
    output_dir = "static/customer_charts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate metrics for each customer
    customer_metrics = customer_data.groupby("Customer_Name").agg({
        "Sentiment_Score": ['mean', 'count'],
        "Response_Time_Minutes": 'mean'
    }).round(2)
    
    customer_metrics.columns = ['avg_sentiment', 'total_chats', 'avg_response_time']
    customer_metrics = customer_metrics.sort_values(by='total_chats', ascending=False).head(10)
    
    # Create plot
    plt.figure(figsize=(12, 8))
    
    # Create a grid for subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot number of chats
    sns.barplot(x=customer_metrics.index, y=customer_metrics['total_chats'], ax=ax1, palette="viridis")
    ax1.set_title("Top 10 Customers by Number of Chats")
    ax1.set_ylabel("Number of Chats")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    ax1.grid(True, axis='y')
    
    # Plot average sentiment
    sns.barplot(x=customer_metrics.index, y=customer_metrics['avg_sentiment'], ax=ax2, palette="viridis")
    ax2.set_title("Customer Sentiment Analysis")
    ax2.set_ylabel("Average Sentiment Score")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
    ax2.grid(True, axis='y')
    
    plt.tight_layout()
    
    # Save image
    output_path = os.path.join(output_dir, "customer_complaints.png")
    plt.savefig(output_path)
    plt.close()
    
    return output_path
