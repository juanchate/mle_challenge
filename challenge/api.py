from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import pandas as pd
from .model import DelayModel

app = FastAPI()

# Create an instance of the model
model = DelayModel()

# Define a data type for the input of the /predict endpoint
class PredictRequest(BaseModel):
    flights: list[dict]

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: PredictRequest) -> dict:
    try:
        # Convert the list of dictionaries to DataFrame
        data_df = pd.DataFrame(request.flights)  # Use 'flights' instead of 'data'
        
        # Preprocess the data
        features = model.preprocess(data_df)
        
        # Make the prediction
        predictions = model.predict(features)
        
        # Return the response
        return {
            "predict": predictions
        }
    except ValueError as e:  # Capture validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:  # Capture other errors
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":  
    port = int(os.environ.get("PORT", 8080))  
    uvicorn.run(app, host="0.0.0.0", port=port) 