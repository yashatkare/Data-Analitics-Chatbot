# FastAPI SmartDataframe API

This FastAPI application allows users to upload CSV or Excel files and perform queries using natural language processing with the help of PandasAI and OpenAI's GPT. It also supports generating and serving visualizations based on the data.

## Features

- Upload CSV or Excel files to be processed.
- Query the data using natural language.
- Generate and retrieve visualizations as images.
- CORS enabled for cross-origin requests.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yashatkare/Data-Analitics-Chatbot.git
    cd Data-Analitics-Chatbot
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

4. Visit `index.html` to interact with the API.

## API Endpoints

- **POST /uploadfile/**: Upload a CSV or Excel file.
- **GET /query/**: Query the uploaded data using a natural language prompt.
- **GET /image/{image_name}**: Retrieve generated images.

## Sample Data

Use the `test-data.csv` file provided in the repository for testing.

## Video Tutorial

For a detailed walkthrough of how to use this application, watch the [video tutorial](./video.mp4).
