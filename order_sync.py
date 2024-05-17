import time
import pandas as pd
from dhanhq import dhanhq

# Initialize master and slave accounts
master_dhan = dhanhq("master_client_id", "master_access_token")
slave_dhan = dhanhq("slave_client_id", "slave_access_token")

# Function to fetch pending orders and save them to CSV
def fetch_and_save_pending_orders(account, filename):
    orders = account.get_order_list()
    pending_orders = [order for order in orders if order['order_status'] == 'PENDING']
    df = pd.DataFrame(pending_orders)
    df.to_csv(filename, index=False)

# Function to compare and modify/cancel orders in slave account
def compare_and_modify_orders(master_orders, slave_orders):
    if not master_orders:  # If no pending orders in master account, cancel all orders in slave account
        for order in slave_orders:
            slave_dhan.cancel_order(order['order_id'])
    else:
        for master_order in master_orders:
            for slave_order in slave_orders:
                if master_order['trading_symbol'] == slave_order['trading_symbol'] and \
                   master_order['security_id'] == slave_order['security_id'] and \
                   master_order['quantity'] != slave_order['quantity'] or \
                   master_order['price'] != slave_order['price'] or \
                   master_order['leg_name'] != slave_order['leg_name'] or \
                   master_order['drv_option_type'] != slave_order['drv_option_type'] or \
                   master_order['drv_strike_price'] != slave_order['drv_strike_price'] or \
                   master_order['order_type'] != slave_order['order_type'] or \
                   master_order['transaction_type'] != slave_order['transaction_type']:
                    slave_dhan.modify_order(slave_order['order_id'], 
                                            master_order['order_type'], 
                                            master_order['leg_name'], 
                                            master_order['quantity'], 
                                            master_order['price'], 
                                            master_order['trigger_price'], 
                                            master_order['disclosed_quantity'], 
                                            master_order['validity'])
                    break  # Assuming one order can be modified at a time

# Main loop
while True:
    fetch_and_save_pending_orders(master_dhan, "master_pending_orders.csv")
    fetch_and_save_pending_orders(slave_dhan, "slave_pending_orders.csv")
    
    master_pending_orders_df = pd.read_csv("master_pending_orders.csv")
    slave_pending_orders_df = pd.read_csv("slave_pending_orders.csv")
    
    compare_and_modify_orders(master_pending_orders_df.to_dict('records'), slave_pending_orders_df.to_dict('records'))
    
    time.sleep(60)  # Sleep for 60 seconds before fetching orders again
