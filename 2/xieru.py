import pandas as pd

# Specify the paths
csv_file_path = 'E:\\pythonProject_mathorcup\\2\\result\\result.csv'
excel_file_path = 'E:\\ocdata\\3_Test\\Test_results.xlsx'  # Define the output Excel file path

# Read the CSV file
data = pd.read_csv(csv_file_path)

# Write the data to an Excel file
data.to_excel(excel_file_path, index=False, engine='openpyxl')
