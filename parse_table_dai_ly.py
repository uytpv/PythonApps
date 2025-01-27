import pandas as pd
import chardet

# Read in HTML data as a DataFrame
file = 'parse_table_dai_ly.html'

# Detect the file encoding
with open(file, 'rb') as f:
    result = chardet.detect(f.read())
file_encoding = result['encoding']

# Read the file with the detected encoding
data = pd.read_html(file, encoding=file_encoding)

# Select the table you want to convert to Excel
table = data[0] # or data[n] where n is the index of the table

# Convert to the desired encoding
table = table.applymap(lambda x: x.encode(file_encoding).decode('utf-8') if isinstance(x, str) else x)


# Save table as an Excel file
table.to_excel('daily.xlsx', index=False)