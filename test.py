import tkinter as tk
from tkinter import messagebox

# Function to place order and display result
def place_order_from_gui():
    symbol = symbol_entry.get()
    lot_multiplier = int(lot_multiplier_entry.get())
    price = float(price_entry.get())
    bo_profit_value = float(bo_profit_entry.get())
    bo_stop_loss_Value = float(bo_stop_loss_entry.get())

    order_id = place_order(symbol, lot_multiplier, price, bo_profit_value, bo_stop_loss_Value)

    if isinstance(order_id, str):
        messagebox.showerror("Error", order_id)
    else:
        status = order_id['status']
        remarks = order_id['remarks']
        order_df = pd.DataFrame(order_id['data'])
        order_df['Status'] = status
        order_df['Remarks'] = remarks
        result_text.config(state='normal')
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, order_df.to_string(index=False))
        result_text.config(state='disabled')

# Create the main window
root = tk.Tk()
root.title("Trading Order Placement")

# Create input fields for order parameters
symbol_label = tk.Label(root, text="Symbol:")
symbol_label.pack()
symbol_entry = tk.Entry(root)
symbol_entry.pack()

lot_multiplier_label = tk.Label(root, text="Lot Multiplier:")
lot_multiplier_label.pack()
lot_multiplier_entry = tk.Entry(root)
lot_multiplier_entry.pack()

price_label = tk.Label(root, text="Price:")
price_label.pack()
price_entry = tk.Entry(root)
price_entry.pack()

bo_profit_label = tk.Label(root, text="BO Profit Value:")
bo_profit_label.pack()
bo_profit_entry = tk.Entry(root)
bo_profit_entry.pack()

bo_stop_loss_label = tk.Label(root, text="BO Stop Loss Value:")
bo_stop_loss_label.pack()
bo_stop_loss_entry = tk.Entry(root)
bo_stop_loss_entry.pack()

# Button to place the order
submit_button = tk.Button(root, text="Place Order", command=place_order_from_gui)
submit_button.pack()

# Result display area
result_label = tk.Label(root, text="Order Details:")
result_label.pack()
result_text = tk.Text(root, height=20, width=80, state='disabled')
result_text.pack()

# Start the GUI main loop
root.mainloop()
