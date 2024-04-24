import pandas as pd
import glob

def sort_dataframe_by_datetime(df, datetime_column):
    """
    Sorts the DataFrame based on the specified datetime column.
    
    Parameters:
        df (pandas.DataFrame): The input DataFrame.
        datetime_column (str): The name of the datetime column to sort by.
        
    Returns:
        pandas.DataFrame: The sorted DataFrame.
    """
    if datetime_column not in df.columns:
        print(f"Error: '{datetime_column}' column not found in the DataFrame.")
        return None
    
    # Convert the datetime column to datetime type
    df[datetime_column] = pd.to_datetime(df[datetime_column])
    
    # Sort the DataFrame based on the datetime column
    sorted_df = df.sort_values(by=datetime_column)
    
    return sorted_df


def combine_csv_files(input_folder, output_file):
    # Get a list of all CSV files in the input folder
    csv_files = glob.glob( './*.csv')
    print(csv_files)
   
    # Initialize an empty list to hold DataFrames
    dfs = []
    
    # Read each CSV file and append its DataFrame to the list
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        dfs.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Write the combined DataFrame to a new CSV file
    combined_df = sort_dataframe_by_datetime(combined_df, "Timestamp")
    combined_df.to_csv(output_file, index=False)
    print("Combined CSV file saved successfully!")

# Example usage:
input_folder = ''  # Path to the folder containing CSV files
output_file = 'combined_data.csv'  # Path for the combined CSV file
combine_csv_files(input_folder, output_file)
