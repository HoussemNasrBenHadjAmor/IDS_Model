import sys
import datetime
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.utils import to_categorical
import keras
from joblib import load

# Get the nb_rows of previous save or initiate it to 0
def get_nb_rows(path):
    nb_rows = 0
    # Check if the file exists
    if os.path.isfile(path):
        # Check if the file is non-empty
        if os.path.getsize(path) > 0:
            # Open the file
            with open(path, 'r') as file:
                # Get the rows number value
                content = file.read()
                nb_rows = int(content)
            # File is not empty, close the file
    return nb_rows

# Check if we kill the script in case of empty file
def check_if_run_program(df):
    if df.shape[0] == 0:
        print('exit')
        exit()

# Remove rows that contain columns head values
def remove_columns_rows_values(df):
    mask = df.apply(lambda row: all(row == df.columns), axis=1)
    df = df[~mask]
    return df

# Reshape the output instances data
def reshape_data(df,nb_rows):
    end = df.shape[0]
    df= df.iloc[nb_rows:end-1, :]
    df = df.reset_index(drop=True)
    return df

# Normalization of the data
def normalize_data(df):
    # Data Normalization
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df),columns=df.columns)
    return df_scaled

# Remove any duplicate rows and remove the Label column
def drop_duplicate(df):
    df= df.drop_duplicates(keep='first',ignore_index=True)
    return df

# Filter our csv file data
def filter_data(df):
    # Removing space in all features names
    df.rename(columns=lambda x: x.lstrip(), inplace=True)

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

    # The df is composed of int64 and float64 types --> convert the df to just float64 before the normalization process
    df = df.astype('float64')
    
    return df

# Load our CNN model
def load_model(path):
    model = keras.models.load_model(path)
    return model

# Load our encoder
def load_encoder(path):
    label_encoder = load(path)
    return label_encoder

# Predict the  class of each sample using the trained model
def predict_class(model,df):
    predictions = model.predict(df)
    return predictions

# Save file as scv
def save_csv(df, nb_rows, path):
    if nb_rows == 0 or not os.path.exists(path):
        # Create a new file and write the DataFrame
        df.to_csv(path, index=False)
    else:
        df.to_csv(path, mode='a', header=False, index=False)

# Update nb_rows text file in the end of the whole process 
def update_nb_rows(current_directory, path, nb_rows):
    current_date = datetime.datetime.now().strftime("%Y_%m_%d") 
    new_path = f"{current_directory}/rows/nb_rows_{current_date}.txt" 

    # Check if the file exists
    if os.path.isfile(path):
        os.remove(path)
        with open(new_path, 'w') as file:
            file.write(str(nb_rows))
    else:
        # File doesn't exist, create a new one
        with open(new_path, 'w') as file:
            file.write(str(nb_rows))

#csv_path, nb_rows_path, model_path, encoder_path:
current_directory = sys.argv[1]
csv_path =  sys.argv[2]
nb_rows_path = sys.argv[3]
model_path = sys.argv[4]
encoder_path = sys.argv[5]
current_date = datetime.datetime.now().strftime("%Y_%m_%d") 
new_csv_path = f"{current_directory}/csv_classification/{current_date}.csv"

# Read our csv data
df = pd.read_csv(csv_path)

# Remove the columns values in the rows
df=remove_columns_rows_values(df)

# Check if we run our program or we'll kill the script and  exit
check_if_run_program(df)

nb_rows = get_nb_rows(nb_rows_path)

# Drop duplicates
df= drop_duplicate(df)

# Keep some unused columns so later we could concatinate them with the final predicted data 
df_droped = df[['Flow ID', 'Src IP', 'Dst IP','Src Port', 'Protocol','Timestamp']]

# Drop some columns first to convert our csv data to the old data structure so that our CNN model can predict the classes.
df = df.drop(columns=['Flow ID','Src IP','Dst IP','Src Port','Protocol','Timestamp','Label'],axis=1)

# Rename columns to fit to our CNN trained model structure
df.rename(columns={'Dst Port':'Destination Port',
                   'Tot Fwd Pkts':'Total Fwd Packets',
                   'Tot Bwd Pkts':'Total Backward Packets',
                   'TotLen Fwd Pkts':'Total Length of Fwd Packets',
                   'TotLen Bwd Pkts':'Total Length of Bwd Packets',
                   'Fwd Pkt Len Max':'Fwd Packet Length Max',
                   'Fwd Pkt Len Min':'Fwd Packet Length Min',
                   'Fwd Pkt Len Mean':'Fwd Packet Length Mean',
                   'Fwd Pkt Len Std':'Fwd Packet Length Std',
                   'Bwd Pkt Len Max':'Bwd Packet Length Max',
                   'Bwd Pkt Len Min':'Bwd Packet Length Min',
                   'Bwd Pkt Len Mean':'Bwd Packet Length Mean',
                   'Bwd Pkt Len Std':'Bwd Packet Length Std',
                   'Flow Byts/s':'Flow Bytes/s',
                   'Flow Pkts/s':'Flow Packets/s',
                   'Fwd IAT Tot':'Fwd IAT Total',
                   'Bwd IAT Tot':'Bwd IAT Total',
                   'Fwd Header Len':'Fwd Header Length',
                   'Bwd Header Len':'Bwd Header Length',
                   'Fwd Pkts/s':'Fwd Packets/s',
                   'Bwd Pkts/s':'Bwd Packets/s',
                   'Pkt Len Min':'Min Packet Length',
                   'Pkt Len Max':'Max Packet Length',
                   'Pkt Len Std':'Packet Length Std',
                   'Pkt Len Var':'Packet Length Variance',
                   'FIN Flag Cnt':'FIN Flag Count',
                   'SYN Flag Cnt':'SYN Flag Count',
                   'RST Flag Cnt':'RST Flag Count',
                   'PSH Flag Cnt':'PSH Flag Count',
                   'ACK Flag Cnt':'ACK Flag Count',
                   'URG Flag Cnt':'URG Flag Count',
                   'CWE Flag Cnt':'CWE Flag Count',
                   'ECE Flag Cnt':'ECE Flag Count',
                   'Pkt Size Avg':'Average Packet Size',
                   'Fwd Seg Size Avg':'Avg Fwd Segment Size',
                   'Bwd Seg Size Avg':'Avg Bwd Segment Size',
                   'Fwd Byts/b Avg':'Avg Bwd Segment Size',
                   'Fwd Byts/b Avg': 'Fwd Avg Bytes/Bulk',
                   'Fwd Pkts/b Avg': 'Fwd Avg Packets/Bulk',
                   'Fwd Blk Rate Avg': 'Fwd Avg Bulk Rate',
                   'Bwd Byts/b Avg': 'Bwd Avg Bytes/Bulk',
                   'Bwd Pkts/b Avg': 'Bwd Avg Packets/Bulk',
                   'Bwd Blk Rate Avg': 'Bwd Avg Bulk Rate',
                   'Subflow Fwd Pkts': 'Subflow Fwd Packets',
                   'Subflow Fwd Byts': 'Subflow Fwd Bytes',
                   'Subflow Bwd Pkts': 'Subflow Bwd Packets',
                   'Subflow Bwd Byts': 'Subflow Bwd Bytes',
                   'Init Fwd Win Byts': 'Init_Win_bytes_forward',
                   'Fwd Act Data Pkts': 'act_data_pkt_fwd',
                   'Fwd Seg Size Min':'min_seg_size_forward',} , inplace=True)

# Duplicate our Fwd Header Length so that our CNN trained model doesn't complain about it while predicting
df.insert(loc=55, column='Fwd Header Length.1', value=df['Fwd Header Length'])

# Load our CNN model
cnn_model = load_model(model_path)

# Load our encoder
label_encoder = load_encoder(encoder_path)

# Filter our reshaped data to fit to our training CNN model
df = filter_data(df)

# Nomalize our data before sending it to CNN model
df_normalized = normalize_data(df)

# Pedict classes using our cnn model
predictions = predict_class(cnn_model,df_normalized)

# Inverse transform one-hot encoded labels to original string labels
predicted_labels_str = label_encoder.inverse_transform(predictions.argmax(axis=1))

# Add our Label column to our normalized dataframe
df_normalized['Label'] = predicted_labels_str

# Concatinate the columns such as 'Flow ID', 'Src IP', 'Dst IP','Src Port', 'Protocol','Timestamp' to our final original dataframe
df_normalized = pd.concat([df_droped, df_normalized], axis=1)

# Add our Label column to our original dataframe
df['Label'] = predicted_labels_str

# Concatinate the columns such as 'Flow ID', 'Src IP', 'Dst IP','Src Port', 'Protocol','Timestamp' to our final original dataframe
df = pd.concat([df_droped, df], axis=1)

# Here need to save the new nb_rows by adding 
new_nb_rows = nb_rows + df.shape[0]

# update_nb_row(path, new_nb_rows)
update_nb_rows(current_directory,nb_rows_path,new_nb_rows)

# Here we save the new predicted dataframe to csv file
save_csv(df,nb_rows,new_csv_path)

nb_begnin = (df['Label']=='BENIGN').sum()
print(f'moyenne nb BENIGN: {nb_begnin/df.shape[0]}')


print('+++ Model Classification Ended Successfully :)')
