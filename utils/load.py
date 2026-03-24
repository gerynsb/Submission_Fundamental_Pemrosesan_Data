import pandas as pd
from sqlalchemy import create_engine
from google.oauth2 import service_account
from googleapiclient.discovery import build

def load_to_csv(df, filename='products.csv'):
    try:
        df.to_csv(filename, index=False)
        print(f"Sukses menyimpan ke {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def load_to_mysql(df, db_user, db_pass, db_host, db_name, table_name='products'):
    try:
        # Ganti kredensial sesuai database MySQL lokal Anda
        engine = create_engine(f"mysql+pymysql://root:dean@localhost:3306/dicoding_etl")
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print(f"Sukses menyimpan ke tabel MySQL '{table_name}'")
    except Exception as e:
        print(f"Error saving to MySQL: {e}")

def load_to_gsheets(df, spreadsheet_id, credentials_file='google-sheets-api.json'):
    try:
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        
        # Konversi DataFrame ke format list of lists untuk API
        values = [df.columns.values.tolist()] + df.astype(str).values.tolist()
        body = {'values': values}
        
        range_name = 'Sheet1!A1'
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='RAW', body=body
        ).execute()
        
        print(f"Sukses menyimpan ke Google Sheets: {result.get('updatedCells')} cells updated.")
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")