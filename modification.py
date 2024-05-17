import os
import pandas as pd
from dhanhq import dhanhq
from datetime import datetime

client_id = "1102743720"
access_token  =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE3MzAzNjI5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjc0MzcyMCJ9.Z5dInFugshNE1mB70IeW4DTWthBIhubmXKEibNqOQFPrhSdaSCHBL7hynAi6M-u4Cv82oEXg1rVf95G4pyITng"
dhan = dhanhq(client_id, access_token)

# leg_name
def get_leg_name(leg_name):
    if leg_name == "entry" :
        return 'ENTRY_LEG'
    elif leg_name == "target" :
        return 'TARGET_LEG'
    elif leg_name == "put" :
        return 'sl'

def modify_order(leg_name) :
    order = dhan.modify_order(
        order_id=order_id,
        order_type=dhan.LIMIT,
        leg_name=leg_name,
        quantity=40,
        price=3345.8,
        disclosed_quantity=10,
        trigger_price=0,
        validity=dhan.DAY)
    return order
leg_name = ''
order_id = ''
