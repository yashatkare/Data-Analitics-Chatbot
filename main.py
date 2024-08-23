from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import JSONResponse, FileResponse
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
import pandas as pd
import io
import os
from fastapi.middleware.cors import CORSMiddleware
import traceback
import numpy as np

app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity, you can restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
llm = OpenAI(api_token="sk-proj-abHkjRmhthPclRybI1rGT3BlbkFJ8Z9CsIJZVVp9XpKIdME2")
global_df = None

@app.post("/uploadfile/")
async def root(file: UploadFile = File(...)):
    global global_df
    try:
        # Read the uploaded file into a pandas DataFrame
        # print("File:", file)
        contents = await file.read()
        # print("File Contents:", type(contents))  # Debugging line
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents), encoding='ISO-8859-1')
        else:
            df = pd.read_excel(io.BytesIO(contents))
        # print("DataFrame:", type(df))  # Debugging line
        
        # Convert the DataFrame to a SmartDataframe
        global_df = SmartDataframe(df, config={"llm": llm, "open_charts": False, "varbose": True, "use_error_correction_framework": True, "max_retries":3, "save_logs":False, "enable_cache": False, "save_charts":True }, )
        
        return JSONResponse(content={"message": "File uploaded and processed successfully."})
    except Exception as e:
        # full error message
        print("Error:", e)
        
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.get("/query/")
async def query_data(query: str):
    global global_df
    
    if global_df is None:
        return JSONResponse(content={"error": "No data uploaded yet."}, status_code=400)
        # Process the query with the SmartDataframe
    try:
        result = global_df.chat(query)
        print("Result:", result)
        print("Type:", type(result))
        if isinstance(result, pd.DataFrame):
            # replace nan with None
            result = result.replace(np.nan, None)
            print("Result without nan:", result)
            # Convert the DataFrame to a JSON-compatible format
            result_json = result.to_dict(orient='records')
            print("Result JSON:", result_json)
            return JSONResponse(content={"result": result_json})
        # if result contain os-path
        elif isinstance(result, str) and os.path.exists(result):
            # rename image name
            # import random
            # NEW_NAME = F'chart-{random.randint(1000, 9999)}.png'
            # image_name = os.path.basename(result)
            # new_image_path = os.path.join('exports/charts', NEW_NAME)
            # os.rename(result, new_image_path)
            # result = new_image_path

            image_path = result
            return JSONResponse(content={"result": result, "image_path": image_path})
        
        else:
            # print("Result:", result) # Debugging line
            # print("Type:", type(result))
            return JSONResponse(content={"result": str(result)})
    
    except Exception as e:
        print("Error:", e)  # Debugging line
        print(traceback.format_exc())
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
@app.get("/image/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join("exports/charts", image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return JSONResponse(content={"error": "Image not found"}, status_code=404)