import argparse
import json
from datetime import datetime
from distutils import util

import openpyxl
import pandas as pd
import requests

from utils.data_utils import *
from utils.request_utils import get_access_token

TODAY = datetime.now()

HU_COLUMN = "hu"
RNR_COLUMN = "rnr"
GRUPPE_COLUMN = "gruppe"
LABEL_IDS_COLUMN = "labelIds"

CSV_FILE_PATH = "resources/vehicles.csv"
OUTPUT_DATA_PATH = f"output_data/vehicles_{TODAY.isoformat()}.xlsx".replace(":", ".")

AUTH_URL = "https://api.baubuddy.de/index.php/login"
AUTH_PAYLOAD = {
    "username": "365",
    "password": "1"
}
AUTH_HEADERS = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}

ACCESS_TOKEN = get_access_token(
    url=AUTH_URL,
    json=AUTH_PAYLOAD,
    headers=AUTH_HEADERS
)

API_URL = "http://127.0.0.1:5000/api/data"
API_HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

COLOR_API_URL = "https://api.baubuddy.de/dev/index.php/v1/labels/"

parser = argparse.ArgumentParser(description="Enter required columns and whether to add background color on rows")
parser.add_argument("-k", "--keys", type=str, nargs="+", required=True)
parser.add_argument("-c", "--colored", type=lambda x: bool(util.strtobool(x)), default=True)

# Extract input parameters
args = parser.parse_args()
input_columns = args.keys
to_add_background_color = args.colored

# Add mandatory columns to `input_columns`
required_columns = add_unique_items_to_list(input_columns, RNR_COLUMN, GRUPPE_COLUMN)

# Get data from API
logger.info("Extracting data...")

response = requests.post(url=API_URL, headers=API_HEADERS, params={"csv_file_path": CSV_FILE_PATH})
data = json.dumps(response.json())

logger.info("Data extracted successfully!")

# Create DataFrame from the data
df = pd.read_json(data)
# Sort DataFrame by "gruppe" column
sorted_df = sort_dataframe(df, GRUPPE_COLUMN, True)
sorted_df = sorted_df.reset_index(drop=True)
# Drop columns from the DataFrame that are not in the input
final_df = drop_mismatch_columns(sorted_df, required_columns)

# Create workbook
wb = openpyxl.Workbook()
ws = wb.active
# Write the data from pandas Dataframe to workbook
write_data_from_pandas_dataframe_to_worksheet(final_df, ws)

# Tint the cell's text in workbook if "labelIds" is given in the input
if LABEL_IDS_COLUMN in required_columns:
    add_font_color_to_worksheet_cells(
        final_df[LABEL_IDS_COLUMN],
        ws,
        COLOR_API_URL,
        API_HEADERS
    )

# Color rows by date in workbook if add_background_color is True
if to_add_background_color:
    add_background_color_to_worksheet_cells(ws, HU_COLUMN, TODAY)

# Save the data after the transformations as xlsx file
logger.info("Saving data...")

wb.save(OUTPUT_DATA_PATH)
wb.close()

logger.info("Data saved successfully!")
