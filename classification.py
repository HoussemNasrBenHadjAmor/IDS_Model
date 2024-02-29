import datetime
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import keras



# Fetching  the data from CSV file and converting it into DataFrame object
file_date = f"{datetime.datetime.now().strftime("%Y-%m-%d")}_Flow.csv"
file_path = os.path.join(os.getcwd(),file_date)
df = pd.read_csv(file_path)

#df.rename(columns=lambda x: x.lstrip(), inplace=True)
#df.drop(columns=['Flow ID','Src IP','Dst IP','Src Port','Protocol','Timestamp'],inplace=True)
#df.rename(columns={'Dst Port':'Destination'})
# Filter our csv file
def filterData(df):
    # Removing space in all features names
    df.rename(columns=lambda x: x.lstrip(), inplace=True)

    #drop the empty label column
    df.drop('Label', axis=1)

    # Remove any duplicate rows and remove the Label column
    df= df.drop_duplicates(keep='first',ignore_index=True)
    df=df.drop('Label',axis=1)

    # Checking if any column contains a NAN value and display its name
    nan_check = df.isna().any()
    columns_with_nan = nan_check[nan_check]

    # Remove the NAN values from our dataset and replace them with the mean of the specific column values
    for i in columns_with_nan.keys():
        df[i] = df[i].fillna(df[i].mean())

    # Remove the INF values from our dataset and replace them with the max of the specific column values
    pd.options.mode.use_inf_as_na = True
    max_values = df.max(axis=0).tolist()
    max_value= np.float64(max_values).max()
    df.replace([np.inf, -np.inf, np.nan], max_value, inplace=True)

    # The df is composed of int64 and float64 types --> convert the df to just float64 before the normalization
    df = df.astype('float64')

    # Data Normalization
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df),columns=df.columns)

    print(df_scaled.head())
    
    # Return the filtered df
    return df_scaled



# load our CNN model
def loadModel():
    model = keras.models.load_model('CNN.md5')
    return model 

# Predict the  class of each sample using the trained model
def predictClass():
    predictions = ''
    return predictions



# Reshape the output instance (add one dimension at the end as classification class)
def reshapeCSV():
    csv=''
    return csv


# Save file as scv 
def  saveAsCsv(df):
    df=''
    return df

filtered_data = filterData(df)
cnn_model = loadModel()

predictions = cnn_model.predict(filtered_data)

print(predictions)