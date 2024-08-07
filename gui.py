import pandas as pd
from validate_email_address import validate_email
import asyncio
from concurrent.futures import ThreadPoolExecutor
import tqdm
import tkinter as tk
from tkinter import filedialog, messagebox

def validate_email_address(email):
    try:
        is_valid = validate_email(email, verify=True) is not None
        print(f"{email} is valid: {is_valid}")
        return is_valid
    except Exception as e:
        print(f"Error validating email {email}: {e}")
        return False

async def process_email(row, executor, output_csv_path):
    email = row['email']
    row['verified'] = await asyncio.get_event_loop().run_in_executor(executor, validate_email_address, email)
    row.to_frame().T.to_csv(output_csv_path, mode='a', header=False, index=False)
    return row

async def validate_emails(df, output_csv_path):
    with ThreadPoolExecutor() as executor:
        tasks = []
        for index, row in df.iterrows():
            tasks.append(process_email(row, executor, output_csv_path))
        for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            await f

def validate_emails_in_csv(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path)
    if 'email' not in df.columns:
        raise ValueError("The input CSV file must have an 'email' column.")
    df['verified'] = False
    df.head(0).to_csv(output_csv_path, index=False)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(validate_emails(df, output_csv_path))

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    input_path_var.set(file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    output_path_var.set(file_path)

def start_validation():
    input_path = input_path_var.get()
    output_path = output_path_var.get()
    if not input_path or not output_path:
        messagebox.showerror("Error", "Please select both input and output files.")
        return
    try:
        validate_emails_in_csv(input_path, output_path)
        messagebox.showinfo("Success", "Email validation completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main application window
app = tk.Tk()
app.title("Email Validator")
app.geometry("400x200")

# Create input file selection section
input_path_var = tk.StringVar()
tk.Label(app, text="Input CSV File:").pack(pady=5)
tk.Entry(app, textvariable=input_path_var, width=50).pack(pady=5)
tk.Button(app, text="Browse...", command=select_input_file).pack(pady=5)

# Create output file selection section
output_path_var = tk.StringVar()
tk.Label(app, text="Output CSV File:").pack(pady=5)
tk.Entry(app, textvariable=output_path_var, width=50).pack(pady=5)
tk.Button(app, text="Browse...", command=select_output_file).pack(pady=5)

# Create the start button
tk.Button(app, text="Start Validation", command=start_validation).pack(pady=20)

# Start the GUI event loop
app.mainloop()
