# Customer Support Chat Analysis

## Overview
This project processes customer support chat logs using *Google Gemini API* to evaluate chat quality based on predefined criteria.

## Features
- Reads customer support chat data from input.csv
- Evaluates each message based on:
  - Greeting & Introduction
  - Understanding the Issue
  - Empathy
  - Clarity of Response
  - Resolution Provided
  - Response Time
  - Professionalism & Politeness
  - Follow-up Provided
- Saves the analysis results to customer_support_analysis.csv

## Installation
### 1. Clone the repository:
bash
 git clone https://github.com/RubyJiu/data-structure.git
 cd data-structure

### 2. Set up your API key:
Create a .env file and add:
env
GEMINI_API_KEY=your_api_key_here


## Usage
### 1. Generate input data (optional):
bash
python generateinput.py

### 2. Run the analysis:
bash
python drai.py input.csv

### 3. Output:
Results are saved in customer_support_analysis.csv.

## Notes
- Ensure your API key is valid.
- Modify generateinput.py to create custom datasets.

## License
MIT License

HW1 is about basketball
HW2 is about customer support chat analysis
HW3 is playwright-login
HW 4 is SumPDF
HW 5 is Customer-service-analytics
期末 is final-project
期末專題影片就放在「期末專題影片」檔案裡面
