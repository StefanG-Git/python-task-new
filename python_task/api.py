import json

import pandas as pd
from flask import Flask, request

from utils.data_utils import *
from utils.request_utils import get_request_resource_as_json

app = Flask(__name__)

RESOURCE_URL = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"

SUFFIX = "_drop"
OUTER_MERGE = "outer"

HU_COLUMN = "hu"
KURZNAME_COLUMN = "kurzname"


@app.route("/api/data", methods=["POST"])
def process_data():
    # TODO edit csv receiving and add validation
    local_data_df = pd.read_csv("resources/vehicles.csv", sep=";")
    # Download resource data
    resource_data = get_request_resource_as_json(url=RESOURCE_URL, headers=request.headers)
    # Create DataFrame from the resource data
    request_data_df = pd.DataFrame(resource_data)
    # Get the common columns from both DataFrames
    common_columns = get_common_columns_from_dfs(request_data_df, local_data_df)
    # Remove the merge column from the common columns list
    common_columns.remove(KURZNAME_COLUMN)
    # Merge both DataFrames
    merged_df = merge_dataframes(local_data_df, request_data_df, OUTER_MERGE, KURZNAME_COLUMN, ("", SUFFIX))
    # Filter rows where "hu" column is Null
    filtered_df = filter_rows_with_null_values_from_df(merged_df, HU_COLUMN)
    # Replace Null values from the duplicate column
    clean_df = replace_null_values_in_df(filtered_df, common_columns, SUFFIX)
    # Drop the duplicate columns
    clean_df = drop_suffix_columns_from_df(clean_df, common_columns, SUFFIX)

    # Return merged and filtered data
    return json.loads(clean_df.to_json(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
