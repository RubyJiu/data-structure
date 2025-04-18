from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os

class ChatReportGenerator:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)
        self.styles = getSampleStyleSheet()
        
    def create_report(self, output_file="chat_analysis_report.pdf"):
        doc = SimpleDocTemplate(output_file)
        elements = []
        
        # Add title
        elements.append(Paragraph("Chat Analysis Report", self.styles["Title"]))
        elements.append(Spacer(1, 20))
        
        # Basic Statistics
        stats = self._get_basic_stats()
        elements.extend(self._create_stats_section(stats))
        
        # Issue Distribution Chart
        issue_chart = self._create_issue_distribution_chart()
        elements.extend(self._create_chart_section("Issue Distribution", issue_chart))
        
        # Sentiment Analysis Chart
        sentiment_chart = self._create_sentiment_chart()
        elements.extend(self._create_chart_section("Sentiment Analysis", sentiment_chart))
        
        # Response Time Analysis
        response_time_chart = self._create_response_time_chart()
        elements.extend(self._create_chart_section("Response Time Analysis", response_time_chart))
        
        try:
            # Generate PDF
            doc.build(elements)
            print(f"Report generated successfully: {output_file}")
            
            # Clean up all temporary files
            temp_files = [f for f in os.listdir('.') if f.startswith('temp_') and f.endswith('.png')]
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Warning: Failed to remove temporary file {temp_file}: {str(e)}")
        
        except Exception as e:
            print(f"Error generating report: {str(e)}")
            # Clean up any temporary files if error occurs
            temp_files = [f for f in os.listdir('.') if f.startswith('temp_') and f.endswith('.png')]
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Warning: Failed to remove temporary file {temp_file}: {str(e)}")
            raise
        
        return output_file

    def _get_basic_stats(self):
        return {
            'total_messages': len(self.df),
            'unique_customers': len(self.df[self.df['sender'] == 'customer']),
            'average_response_time': self._calculate_response_time(),
            'issue_distribution': self._analyze_issues(),
            'sentiment_distribution': self._analyze_sentiment()
        }

    def _calculate_response_time(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df = self.df.sort_values('timestamp')
        
        response_times = []
        for i in range(1, len(self.df)):
            if self.df.iloc[i-1]['sender'] == 'customer' and self.df.iloc[i]['sender'] == 'agent':
                response_times.append((self.df.iloc[i]['timestamp'] - self.df.iloc[i-1]['timestamp']).total_seconds())
        
        return np.mean(response_times) if response_times else 0

    def _analyze_issues(self):
        return self.df[self.df['sender'] == 'customer']['issue_category'].value_counts().to_dict()

    def _analyze_sentiment(self):
        return self.df['sentiment'].value_counts().to_dict()

    def _create_stats_section(self, stats):
        elements = []
        elements.append(Paragraph("Basic Statistics", self.styles["Heading2"]))
        
        # Create table for statistics
        data = [
            ["Total Messages", stats['total_messages']],
            ["Unique Customers", stats['unique_customers']],
            ["Average Response Time", f"{stats['average_response_time']:.2f} seconds"]
        ]
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        return elements

    def _create_issue_distribution_chart(self):
        issues = self._analyze_issues()
        labels = list(issues.keys())
        sizes = list(issues.values())
        
        plt.figure(figsize=(6, 4))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Issue Distribution')
        plt.tight_layout()
        
        return plt

    def _create_sentiment_chart(self):
        sentiment = self._analyze_sentiment()
        labels = list(sentiment.keys())
        sizes = list(sentiment.values())
        
        plt.figure(figsize=(6, 4))
        plt.bar(labels, sizes)
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.tight_layout()
        
        return plt

    def _create_response_time_chart(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df = self.df.sort_values('timestamp')
        
        response_times = []
        for i in range(1, len(self.df)):
            if self.df.iloc[i-1]['sender'] == 'customer' and self.df.iloc[i]['sender'] == 'agent':
                response_times.append((self.df.iloc[i]['timestamp'] - self.df.iloc[i-1]['timestamp']).total_seconds())
        
        plt.figure(figsize=(6, 4))
        plt.hist(response_times, bins=10)
        plt.title('Response Time Distribution')
        plt.xlabel('Response Time (seconds)')
        plt.ylabel('Frequency')
        plt.tight_layout()
        
        return plt

    def _create_chart_section(self, title, chart):
        elements = []
        elements.append(Paragraph(title, self.styles["Heading2"]))
        
        try:
            # Create a safe filename
            safe_title = title.replace(" ", "_").replace("(", "").replace(")", "")
            temp_file = f"temp_{safe_title}.png"
            
            # Save chart with proper format
            chart.savefig(temp_file, bbox_inches='tight', dpi=300)
            plt.close()
            
            # Wait for file to be fully written
            import time
            time.sleep(0.1)  # Small delay to ensure file is fully written
            
            # Verify file exists and has content
            if not os.path.exists(temp_file):
                raise FileNotFoundError(f"Failed to create chart file: {temp_file}")
                
            # Get file size to verify it's not empty
            file_size = os.path.getsize(temp_file)
            if file_size < 100:  # Minimum size for a valid PNG
                raise ValueError(f"Chart file is empty or invalid: {temp_file}")
                
            # Add image to PDF
            img = Image(temp_file, width=400, height=300)
            elements.append(img)
            
            # Add some space after the image
            elements.append(Spacer(1, 20))
            
        except Exception as e:
            print(f"Error processing {title} chart: {str(e)}")
            elements.append(Paragraph(f"Error displaying {title} chart: {str(e)}", self.styles["Normal"]))
        
        return elements

if __name__ == "__main__":
    generator = ChatReportGenerator("chat_data.csv")
    generator.create_report()