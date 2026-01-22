"""
Python Script for Reading and Writing Sheets
Supports both Google Sheets and Excel files
"""

import pandas as pd
import os

# ============================================================================
# Excel File Operations (using pandas)
# ============================================================================

def read_excel_file(file_path, sheet_name=0):
    """
    Read an Excel file using pandas.
    
    Args:
        file_path: Path to the Excel file (.xlsx or .xls)
        sheet_name: Name or index of the sheet to read (default: first sheet)
    
    Returns:
        DataFrame containing the sheet data
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Successfully read Excel file: {file_path}")
        print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None


def write_excel_file(df, file_path, sheet_name='Sheet1', index=False):
    """
    Write a DataFrame to an Excel file.
    
    Args:
        df: DataFrame to write
        file_path: Path where the Excel file will be saved
        sheet_name: Name of the sheet (default: 'Sheet1')
        index: Whether to include the index column (default: False)
    """
    try:
        df.to_excel(file_path, sheet_name=sheet_name, index=index)
        print(f"Successfully wrote Excel file: {file_path}")
    except Exception as e:
        print(f"Error writing Excel file: {e}")


def read_all_excel_sheets(file_path):
    """
    Read all sheets from an Excel file.
    
    Args:
        file_path: Path to the Excel file
    
    Returns:
        Dictionary of sheet names and DataFrames
    """
    try:
        excel_file = pd.ExcelFile(file_path)
        sheets_dict = {}
        for sheet_name in excel_file.sheet_names:
            sheets_dict[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Successfully read {len(sheets_dict)} sheets from: {file_path}")
        return sheets_dict
    except Exception as e:
        print(f"Error reading Excel sheets: {e}")
        return {}


# ============================================================================
# Google Sheets Operations (requires gspread library)
# ============================================================================

def read_google_sheet(sheet_id, worksheet_name=None, credentials_path=None):
    """
    Read data from a Google Sheet.
    
    Requires: pip install gspread google-auth
    
    Args:
        sheet_id: Google Sheet ID (from the URL)
        worksheet_name: Name of the worksheet (default: first worksheet)
        credentials_path: Path to Google service account credentials JSON file
    
    Returns:
        DataFrame containing the sheet data
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        if credentials_path is None:
            print("Error: credentials_path is required for Google Sheets access")
            return None
        
        # Authenticate
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(worksheet_name) if worksheet_name else sheet.sheet1
        
        # Get all values
        data = worksheet.get_all_values()
        
        # Convert to DataFrame
        if data:
            df = pd.DataFrame(data[1:], columns=data[0])
            print(f"Successfully read Google Sheet: {worksheet_name or 'Sheet1'}")
            print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        else:
            print("Sheet is empty")
            return pd.DataFrame()
            
    except ImportError:
        print("Error: gspread and google-auth libraries are required.")
        print("Install with: pip install gspread google-auth")
        return None
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return None


def write_google_sheet(df, sheet_id, worksheet_name, credentials_path, 
                       clear_existing=True):
    """
    Write a DataFrame to a Google Sheet.
    
    Requires: pip install gspread google-auth
    
    Args:
        df: DataFrame to write
        sheet_id: Google Sheet ID (from the URL)
        worksheet_name: Name of the worksheet
        credentials_path: Path to Google service account credentials JSON file
        clear_existing: Whether to clear existing data (default: True)
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        # Authenticate
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=worksheet_name, rows=1000, cols=26)
        
        # Clear existing data if requested
        if clear_existing:
            worksheet.clear()
        
        # Write headers
        worksheet.append_row(df.columns.tolist())
        
        # Write data
        for _, row in df.iterrows():
            worksheet.append_row(row.tolist())
        
        print(f"Successfully wrote to Google Sheet: {worksheet_name}")
        
    except ImportError:
        print("Error: gspread and google-auth libraries are required.")
        print("Install with: pip install gspread google-auth")
    except Exception as e:
        print(f"Error writing to Google Sheet: {e}")


# ============================================================================
# Example Usage
# ============================================================================

def example_excel_operations():
    """Example of reading and writing Excel files."""
    print("\n=== Excel File Operations Example ===\n")
    
    # Example: Create a sample DataFrame
    sample_data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Age': [25, 30, 35, 28],
        'City': ['New York', 'London', 'Tokyo', 'Paris']
    }
    df = pd.DataFrame(sample_data)
    
    # Write to Excel
    excel_file = 'example_output.xlsx'
    write_excel_file(df, excel_file)
    
    # Read from Excel
    df_read = read_excel_file(excel_file)
    if df_read is not None:
        print("\nRead data:")
        print(df_read)
    
    # Clean up (optional)
    # os.remove(excel_file)


def example_google_sheets_operations():
    """Example of reading and writing Google Sheets."""
    print("\n=== Google Sheets Operations Example ===\n")
    print("Note: This requires Google Sheets API credentials.")
    print("See: https://gspread.readthedocs.io/en/latest/oauth2.html")
    
    # Example usage (commented out - requires credentials):
    # sheet_id = "your-google-sheet-id"
    # credentials_path = "path/to/credentials.json"
    # 
    # # Read from Google Sheet
    # df = read_google_sheet(sheet_id, worksheet_name="Sheet1", 
    #                        credentials_path=credentials_path)
    # 
    # # Write to Google Sheet
    # write_google_sheet(df, sheet_id, "Sheet2", credentials_path)


if __name__ == "__main__":
    # Run Excel examples
    example_excel_operations()
    
    # Run Google Sheets examples (commented out - requires setup)
    # example_google_sheets_operations()
