import os
import pandas as pd
from dhanhq import dhanhq
from datetime import datetime

client_id = "1102743720"
access_token  =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE3MzAzNjI5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc0MzcyMCJ9.Z5dInFugshNE1mB70IeW4DTWthBIhubmXKEibNqOQFPrhSdaSCHBL7hynAi6M-u4Cv82oEXg1rVf95G4pyITng"
dhan = dhanhq(client_id, access_token)

# Load symbols from CSV
def get_symbol_details(custom_symbol):
    df = pd.read_csv('sym.csv', low_memory=False)  # Load the DataFrame here
    try:
        row = df[df['SEM_CUSTOM_SYMBOL'] == custom_symbol].iloc[0]
        return {
            'security_id': int(row['SEM_SMST_SECURITY_ID']),
            'lot_units': int(row['SEM_LOT_UNITS'])
        }
    except IndexError:
        print("Symbol not found in the CSV file.")
        return None

def place_order(symbol, lot_multiplier, price, bo_profit_value, bo_stop_loss_Value):
    symbol_details = get_symbol_details(symbol)
    if symbol_details:
        quantity = symbol_details['lot_units'] * lot_multiplier
        order_id = dhan.place_slice_order(
            transaction_type=dhan.BUY,
            exchange_segment=dhan.NSE_FNO,
            product_type=dhan.BO,
            order_type=dhan.LIMIT,
            validity='DAY',
            security_id=symbol_details['security_id'],
            quantity=quantity,                            
            disclosed_quantity=0,
            price=price,
            trigger_price=0,
            after_market_order=False,
            bo_profit_value=bo_profit_value,
            bo_stop_loss_Value=bo_stop_loss_Value)
        return order_id
    else:
        return "Error: Unable to place order due to missing symbol details."

# Example usage
symbol = "NIFTY 16 MAY 22100 CALL"
lot_multiplier = 1
price = 100
bo_profit_value = 40
bo_stop_loss_Value = 5

order_id = place_order(symbol, lot_multiplier, price, bo_profit_value, bo_stop_loss_Value)

# Extract the status and remarks
status = order_id['status']
remarks = order_id['remarks']

# Convert the 'data' list (which contains order details) to a DataFrame
order_df = pd.DataFrame(order_id['data'])

# Add the status and remarks to the DataFrame as new columns
order_df['Status'] = status
order_df['Remarks'] = remarks

# Print the DataFrame
print("Order Details:")
print(order_df)