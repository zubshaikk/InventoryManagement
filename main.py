import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import create_connection, create_item, select_all_items, create_inventory_table, update_item, delete_item_by_id


database = "inventory.db"
conn = create_connection(database) #Connects to the database, if it doesn't exist, it creates it
create_inventory_table(conn)


def clear_entries():
    """
    Clears the text entries in the GUI.
    """
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)


def add_item():
    """
    Function to Add new items to the database.

    Retrieves the item name, quantity, and price from the GUI input fields.
    Validates the quantity and price inputs.
    If the inputs are valid, the item is created in the database and a success message is displayed.
    If there is an error, an error message is displayed.

    Returns:
        None
    """
    if conn:
        item_name = name_var.get()
        quantity_str = quantity_var.get()
        price_str = price_var.get() 

        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity should be a non-negative integer.")
        except ValueError:
            messagebox.showerror("Error", "Quantity should be a non-negative integer.")
            return  

       
        try:
            price = float(price_str) 
            if price < 0.0:
                raise ValueError("Price should be a non-negative number.")
        except ValueError:
            messagebox.showerror("Error", "Price should be a non-negative number.")
            return  

        try:
            create_item(conn, (item_name, quantity, price))
            messagebox.showinfo("Success", "Item added successfully")
            clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item to database: {e}")
    else:
        messagebox.showerror("Error", "No database connection")


def view_all_items():
    """
    Function to view all items in the inventory.

    This function retrieves all items from the database and displays them in a new window using a Treeview widget.
    Each item is displayed with its ID, Item Name, Quantity, and Price.
    Double-clicking on an item opens a new window to update or delete the item.

    Parameters:
    None

    Returns:
    None
    """
    if conn:
        items = select_all_items(conn)
        if items:
            # A new window for view all items
            new_window = tk.Toplevel(root)
            new_window.title("Inventory")

            # Create a Treeview widget
            tree = ttk.Treeview(new_window, columns=('ID', 'Item Name', 'Quantity', 'Price'), show='headings')
            tree.column('ID', width=60)
            tree.column('Item Name', width=150)
            tree.column('Quantity', width=100)
            tree.column('Price', width=100)
            tree.heading('ID', text='ID')
            tree.heading('Item Name', text='Item Name')
            tree.heading('Quantity', text='Quantity')
            tree.heading('Price', text='Price')
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            for item in items:
                tree.insert('', 'end', values=item)


            scrollbar = ttk.Scrollbar(new_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Function to open the update window
            def open_update_window(item_values):
                update_window = tk.Toplevel(new_window)
                update_window.title("Update Item")

                # Entry fields to update item details
                tk.Label(update_window, text='Quantity').pack()
                quantity_var_update = tk.IntVar(value=item_values[2])  
                quantity_entry_update = tk.Entry(update_window, textvariable=quantity_var_update)
                quantity_entry_update.pack()

                tk.Label(update_window, text='Price').pack()
                price_var_update = tk.DoubleVar(value=item_values[3]) 
                price_entry_update = tk.Entry(update_window, textvariable=price_var_update)
                price_entry_update.pack()

                # Update functionality
                def update_item_details():
                    update_item(conn, (quantity_var_update.get(), price_var_update.get(), item_values[0]))  # ID is passed here
                    update_window.destroy()
                    new_window.destroy()  # Refresh list by destroying and reopening
                    view_all_items()

                # Delete functionality
                def delete_item_details():
                    # Ask for confirmation before deletion
                    response = messagebox.askyesno("Confirm", "Are you sure you want to delete this item?")
                    if response:
                        delete_item_by_id(conn, item_values[0])  
                        update_window.destroy()
                        new_window.destroy()  # Refresh list by destroying and reopening
                        view_all_items()


                tk.Button(update_window, text="Save", command=update_item_details).pack()
                tk.Button(update_window, text="Delete", command=delete_item_details).pack()

            # Button for each item to open the update window
            def on_item_selected(event):
                selected_item = tree.focus()
                item_values = tree.item(selected_item, 'values')
                open_update_window(item_values)

            tree.bind('<Double-1>', on_item_selected)
        else:
            messagebox.showinfo("Info", "No items in the inventory")
    else:
        messagebox.showerror("Error", "No database connection")



# GUI Layout
root = tk.Tk()
root.title('Inventory Management System')
root.geometry('500x300') 
label_font = ('Arial', 14)

name_var = tk.StringVar()
quantity_var = tk.StringVar()
price_var = tk.StringVar()

tk.Label(root, text='Item Name', font=label_font).grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root, textvariable=name_var, font=label_font)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text='Quantity', font=label_font).grid(row=1, column=0, padx=10, pady=10)
quantity_entry = tk.Entry(root, textvariable=quantity_var, font=label_font)
quantity_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text='Price', font=label_font).grid(row=2, column=0, padx=10, pady=10)
price_entry = tk.Entry(root, textvariable=price_var, font=label_font)
price_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text='Add Item', command=add_item, font=label_font).grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text='View All Items', command=view_all_items, font=label_font).grid(row=4, column=1, padx=10, pady=10)

# Run the GUI
root.mainloop()
