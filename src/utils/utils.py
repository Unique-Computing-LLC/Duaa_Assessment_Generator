import pandas as pd

def read_csv_as_dict(file_path):
    # Read csv file using pandas
    df = pd.read_csv(file_path)
    
    # Convert dataframe to list of dictionaries
    dict_list = df.to_dict(orient='records')
    
    return dict_list