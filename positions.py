import os
import pandas as pd
from dhanhq import dhanhq
from datetime import datetime

client_id = "1102743720"
access_token  =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE3MzAzNjI5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc0MzcyMCJ9.Z5dInFugshNE1mB70IeW4DTWthBIhubmXKEibNqOQFPrhSdaSCHBL7hynAi6M-u4Cv82oEXg1rVf95G4pyITng"
dhan = dhanhq(client_id, access_token)

# positions
def get_positions(dhan):
    data_positions = dhan.get_positions()
    positions = pd.DataFrame(data_positions['data'])
    positions_specified = pd.DataFrame(positions[['tradingSymbol', 'securityId', 'positionType', 'buyAvg', 'buyQty', 'sellAvg', 'sellQty', 'realizedProfit', 'unrealizedProfit']])
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = "positions"
    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, f"positions_{current_date}.csv")
    positions_specified.to_csv(filename, index=False)
    # positions.to_csv(filename, index=False) # Full File
    return positions_specified
positions_specified = get_positions(dhan)
print(positions_specified)


