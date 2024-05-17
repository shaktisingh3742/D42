import os
import pandas as pd
from dhanhq import dhanhq
from datetime import datetime

client_id = "1102743720"
access_token  =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE3MzAzNjI5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc0MzcyMCJ9.Z5dInFugshNE1mB70IeW4DTWthBIhubmXKEibNqOQFPrhSdaSCHBL7hynAi6M-u4Cv82oEXg1rVf95G4pyITng"
dhan = dhanhq(client_id, access_token)

# order_list
def get_order_list(dhan):
    data_order_list = dhan.get_order_list()
    order_list = pd.DataFrame(data_order_list['data'])
    order_list_specified = pd.DataFrame(order_list[['orderId', 'tradingSymbol', 'securityId', 'transactionType', 'quantity', 'price', 'orderStatus']])
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = "order_list"
    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, f"order_list_{current_date}.csv")
    order_list_specified.to_csv(filename, index=False)
    # order_list.to_csv(filename, index=False) # Full File
    return order_list_specified
order_list_specified = get_order_list(dhan)
print(order_list_specified)

 