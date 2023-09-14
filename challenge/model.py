import pandas as pd  
import numpy as np  
from datetime import datetime  
from sklearn.model_selection import train_test_split  
from sklearn.linear_model import LogisticRegression  
from typing import Tuple, Union, List  
  
class DelayModel:  
  
    def __init__(self):  
        self._model = None  
        self.top_features = [  
            "OPERA_Latin American Wings",  
            "MES_7",  
            "MES_10",  
            "OPERA_Grupo LATAM",  
            "MES_12",  
            "TIPOVUELO_I",  
            "MES_4",  
            "MES_11",  
            "OPERA_Sky Airline",  
            "OPERA_Copa Air"  
        ]  
  
    def preprocess(self, data: pd.DataFrame, target_column: str = None) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:  
        features = pd.concat([  
            pd.get_dummies(data['OPERA'], prefix='OPERA'),  
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),  
            pd.get_dummies(data['MES'], prefix='MES')],  
            axis=1)

        # Check for unknown values
        if 'MES' in data and data['MES'].max() > 12:
            raise ValueError("Unknown value in MES column")
        
        known_opera_values = set(['American Airlines',
                                'Air Canada',
                                'Air France',
                                'Aeromexico',
                                'Aerolineas Argentinas',
                                'Austral',
                                'Avianca',
                                'Alitalia',
                                'British Airways',
                                'Copa Air',
                                'Delta Air',
                                'Gol Trans',
                                'Iberia',
                                'K.L.M.',
                                'Qantas Airways',
                                'United Airlines',
                                'Grupo LATAM',
                                'Sky Airline',
                                'Latin American Wings',
                                'Plus Ultra Lineas Aereas',
                                'JetSmart SPA',
                                'Oceanair Linhas Aereas',
                                'Lacsa'])
        
        if 'OPERA' in data and not set(data['OPERA'].unique()).issubset(known_opera_values):
            raise ValueError("Unknown value in OPERA column")
        
        # Ensure only columns in top_features are selected
        for col in features.columns:
            if col not in self.top_features:
                features.drop(col, axis=1, inplace=True)
        
        features = self.reorder_features(features)  # Move this line up to ensure all top_features are present
        features = features.fillna(False).astype(int)  # Fill NaN values with False and cast to int 
    
        if target_column:  
            data['min_diff'] = data.apply(self._get_min_diff, axis=1)  
            threshold_in_minutes = 15  
            data[target_column] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)  
            target = data[[target_column]]  # Return target as DataFrame
            return features, target  
        return features  
  
  
    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:  
        x_train, _, y_train, _ = train_test_split(features, target, test_size=0.33, random_state=42)  
        y_train = y_train.values.ravel()  # Convert target DataFrame to 1D array
  
        n_y0 = len(y_train[y_train == 0])  
        n_y1 = len(y_train[y_train == 1])  
  
        self._model = LogisticRegression(class_weight={1: n_y0/len(y_train), 0: n_y1/len(y_train)})  
        self._model.fit(x_train, y_train)  
  
    def predict(self, features: pd.DataFrame) -> List[int]:  
        if self._model is None:
            # If model isn't trained, train it with default data
            default_data = pd.read_csv(filepath_or_buffer="./data/data.csv")
            default_features, default_target = self.preprocess(default_data, target_column="delay")
            self.fit(default_features, default_target)
            
        features = self.reorder_features(features)  
        return self._model.predict(features).tolist()  
  
    def reorder_features(self, features: pd.DataFrame) -> pd.DataFrame:  
        missing_cols = set(self.top_features) - set(features.columns)  
        for c in missing_cols:  
            features[c] = 0  
        return features[self.top_features] 
  
    def _get_min_diff(self, data: pd.Series) -> float:  
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')  
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')  
        return ((fecha_o - fecha_i).total_seconds()) / 60  
