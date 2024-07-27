# AI Analysis Streamlit App 🤖

## Description
This Streamlit application provides an interactive platform for data analysis 
using Artificial Intelligence. Users can upload data, perform various 
analyses, and create interactive visualizations.

## Features

### 1. Data Upload
- **Upload CSV Files**: Users can upload CSV files, which are then displayed and 
analyzed within the app.

### 2. Data Display
- **Data Preview**: After uploading, the first few rows of the data are 
displayed.
- **Data Description**: Statistical metrics such as mean, median, and standard 
deviation are calculated and shown.

### 3. Data Analysis
- **Automatic Analysis**: The AI performs automatic analysis of the uploaded 
data, providing insights and summaries.
- **Custom Queries**: Users can ask specific questions about the data, which 
the AI will answer.

### 4. Data Visualization
- **Interactive Charts**: The app offers various interactive charts and 
visualizations based on the uploaded data.
- **Chart Types**: Supported chart types include scatter plots, line plots, 
bar charts, and more.

## Usage
1. Visit the application at [https://ai-analysis.streamlit.app/]
(https://ai-analysis.streamlit.app/).
2. Upload your CSV file.
3. Explore the various analysis and visualization options.
4. Ask custom queries to the AI for specific insights into your data.

## Requirements
- A modern web browser (Chrome, Firefox, Edge, Safari)

## Installation (Local)
If you wish to run the app locally:

1. Get an OpenAI API key and set it as an environment variable in an `.env` file.

2. Clone the repository:
   ```bash
   git clone https://github.com/AdrianW10/data-analysis-tool.git

3. Run the app:   
    ```bash
    pip install -r requirements.txt
    streamlit run main.py

## Configuration
The tool is already preconfigured and requires no further settings. 
However, if necessary, you can adapt the `config.toml` file in the `.streamlit` 
folder to change the colors and font of the tool.
