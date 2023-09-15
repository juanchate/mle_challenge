# MLE Challenge Documentation
 

## Overview
 
This project involves the development of a Machine Learning model to predict flight delays. The solution includes data preprocessing, model training, model evaluation, and model deployment.
## Changes Made
 

### Data Preprocessing
 

#### Update get_period_day function
The function get_period_day was updated to become inclusive. Previously, it was producing a significant number of nulls because the comparison was done using greater than (>) and less than (<) operators instead of greater than or equal to (>=) and less than or equal to (<=). The updated function is as follows:
```
def get_period_day(date):  
    date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()  
    morning_min = datetime.strptime("05:00", '%H:%M').time()  
    morning_max = datetime.strptime("11:59", '%H:%M').time()  
    afternoon_min = datetime.strptime("12:00", '%H:%M').time()  
    afternoon_max = datetime.strptime("18:59", '%H:%M').time()  
    evening_min = datetime.strptime("19:00", '%H:%M').time()  
    evening_max = datetime.strptime("23:59", '%H:%M').time()  
    night_min = datetime.strptime("00:00", '%H:%M').time()  
    night_max = datetime.strptime("4:59", '%H:%M').time()  
      
    if(date_time >= morning_min and date_time <= morning_max):  
        return 'mañana'  
    elif(date_time >= afternoon_min and date_time <= afternoon_max):  
        return 'tarde'  
    elif(  
        (date_time >= evening_min and date_time <= evening_max) or  
        (date_time >= night_min and date_time <= night_max)  
    ):  
        return 'noche'  
 ```

#### Fix delay rate calculation
 
The delay rate calculation was fixed in the get_rate_from_column function. Previously, the total was divided by delays[name], but this was corrected to delays[name] / total.
### Data Visualization
 
The plt.ylim of the plots was adjusted to improve visibility.
### Feature Selection
 
The features variable was adjusted to be derived from training_data instead of data. The top 10 features were hard-coded and used for model training.
### Model Selection
 
The Logistic Regression model was chosen over XGBoost Classifier. Both models produced similar results, but the Logistic Regression model was chosen because it is lighter, has fewer dependencies, and is more interpretable.
### Model Training and Prediction
 
The DelayModel class was created in model.py to handle data preprocessing, model training, and prediction.

The class includes functions to preprocess the data, fit the model, reorder the features, get the minimum difference in time, and make predictions. It also includes an initialization function that sets up the model and the top features to use.
### API Development
 
The FastAPI framework was used to develop an API for the model. The API includes two endpoints: a health check endpoint (/health) and a prediction endpoint (/predict).

The prediction endpoint takes a list of flights as input and returns a list of delay predictions.
### CI/CD Pipeline
 
A CI/CD pipeline was set up using GitHub Actions. The pipeline includes two workflows: Continuous Integration (CI) and Continuous Delivery (CD).

The CI workflow builds the Docker image, runs the model and API tests, and pushes the Docker image to Google Container Registry (GCR) if all tests pass.

The CD workflow is triggered on every push to the 'main' branch. It deploys the application to Google Cloud Run using the image stored in GCR.

### Docker
 
Docker was used to containerize the application. The Dockerfile includes instructions to set up the environment, copy local code to the container image, install the dependencies, and run the web service at container startup. Here's the Dockerfile:
```
# Use the official lightweight Python image.    
FROM python:3.9-slim  
  
# Install make    
RUN apt-get update && apt-get install -y make    
    
# Allow statements and log messages to immediately appear in the Cloud Run logs    
ENV PYTHONUNBUFFERED True    
    
# Copy local code to the container image.    
WORKDIR /app    
COPY . ./    
    
# Install production and test dependencies.    
RUN pip install -r requirements.txt -r requirements-test.txt  
    
# Run the web service on container startup.    
CMD uvicorn challenge.api:app --host 0.0.0.0 --port $PORT    
```

### Testing
 
All tests run successfully and the reports folder was generated, containing the test results.
### Deployment
 
The application was deployed on Google Cloud Run and is accessible at the URL: https://mle-challenge-service-qtbuusv5tq-rj.a.run.app
### Google Cloud Platform (GCP) Setup
 
A service account was created on GCP with the necessary permissions for Docker and for CI/CD setup. This includes permissions to access Google Cloud Registry (GCR), to deploy services on Google Cloud Run, and to access necessary secrets in the CI/CD pipeline.

The service account's secret was added to the GitHub repository to allow GitHub Actions to interact with GCP.
### Git Workflow
 
A logical Git workflow similar to GitFlow was maintained, with a 'main' branch for production code and individual feature branches for development and experimentation.