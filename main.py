import pandas as pd
from validate_email_address import validate_email
import asyncio
from concurrent.futures import ThreadPoolExecutor
import tqdm

def validate_email_address(email):
    try:
        return validate_email(email, verify=True) is not None
    
    except Exception as e:
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
    
    loop = asyncio.new_event_loop()
    loop.run_until_complete(validate_emails(df, output_csv_path))

input_csv_path = 'input_emails.csv'
output_csv_path = 'verified_emails.csv'
validate_emails_in_csv(input_csv_path, output_csv_path)
