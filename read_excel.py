import pandas as pd

spreadsheet_file = pd.ExcelFile("C:\\Users\\DELL\\Downloads\\practice.xlsx")
worksheet = spreadsheet_file.sheet_names
append_data = []

for sheet_data_name in worksheet:
    details = "phone"
    df = pd.read_excel(spreadsheet_file,sheet_data_name, header=0)
    print(df)
    #df = df[["COID",details]]