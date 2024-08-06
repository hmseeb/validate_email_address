# Email Validation Tool

This Python script validates email addresses from a CSV file and outputs the results to a new CSV file. It uses the `validate_email_address` library to verify each email and `asyncio` for asynchronous processing.

## Features

- Reads email addresses from an input CSV file.
- Validates each email address.
- Writes the validation results to an output CSV file.
- Asynchronous processing for faster validation.

## Requirements

- pandas
- validate_email_address
- asyncio
- tqdm

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/hmseeb/validate_email_address.git
    cd validate_email_address
    ```

2. Install the required Python packages:
    ```bash
    pip install pandas validate_email_address tqdm
    ```

## Usage

1. Prepare your input CSV file (`input_emails.csv`) with an `email` column containing the email addresses you want to validate.

2. Run the script:
    ```bash
    python validate_emails.py
    ```

3. The validation results will be saved to `verified_emails.csv` in the same directory.

## Script Details

### Functions

- `validate_email_address(email)`: Validates a single email address.
- `process_email(row, executor, output_csv_path)`: Processes a single row from the DataFrame, validating the email address and writing the result to the output CSV.
- `validate_emails(df, output_csv_path)`: Validates all email addresses in the DataFrame asynchronously.
- `validate_emails_in_csv(input_csv_path, output_csv_path)`: Main function to read the input CSV, validate the emails, and write the results to the output CSV.

### Example

Ensure you have an `input_emails.csv` file with the following structure:

```csv
email
example1@example.com
example2@example.com
```

Run the script:

```bash
python validate_emails.py
```

The output will be written to `verified_emails.csv` with an additional `verified` column indicating whether each email address is valid.

## Contributing

Contributions are welcome. Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License.

---

Feel free to modify the script or the README file according to your needs. If you encounter any issues or have any questions, please open an issue on GitHub.