import pandas as pd
from src.gen_files import paths as p
import os

def convert_csv_to_html(csv_file_path, output_html_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to an HTML table
    html_table = df.to_html(index=False)

    # Write the HTML table to a file
    with open(output_html_path, 'w') as html_file:
        html_file.write(html_table)

# Example usage
csv_file_path = p.testng_server_csv_path
output_html_path = os.path.join(p.output_dir, 'testng_to_server.html')
convert_csv_to_html(csv_file_path, output_html_path)
print('created at ' + output_html_path)
