import pandas as pd
import logging
from sqlalchemy import create_engine
from google.oauth2 import service_account
from googleapiclient.discovery import build

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def simpan_ke_csv(df, nama_file="produk.csv"):
    try:
        df.to_csv(nama_file, index=False)
        logging.info(f"Sukses menyimpan file CSV: {nama_file}")
        return True
    except Exception as e:
        logging.error(f"Gagal menyimpan CSV: {e}")
        return False

def simpan_ke_mysql(df, db_uri, nama_tabel="kompetitor_fashion"):
    try:
        mesin_db = create_engine(db_uri)
        df.to_sql(name=nama_tabel, con=mesin_db, if_exists='replace', index=False)
        logging.info(f"Sukses memuat data ke tabel MySQL: {nama_tabel}")
        return True
    except Exception as e:
        logging.error(f"Gagal memuat ke MySQL: {e}")
        return False

def simpan_ke_gsheets(df, spreadsheet_id, file_kredensial='google-sheets-api.json'):
    try:
        cakupan = ['https://www.googleapis.com/auth/spreadsheets']
        kredensial = service_account.Credentials.from_service_account_file(file_kredensial, scopes=cakupan)
        layanan = build('sheets', 'v4', credentials=kredensial)
        
        # Konversi ke format matrix (list of lists)
        nilai_sel = [df.columns.values.tolist()] + df.astype(str).values.tolist()
        body = {'values': nilai_sel}
        
        hasil = layanan.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range='Sheet1!A1',
            valueInputOption='RAW', body=body
        ).execute()
        
        logging.info(f"Sukses sinkronisasi ke Google Sheets. {hasil.get('updatedCells')} sel diperbarui.")
        return True
    except Exception as e:
        logging.error(f"Gagal memuat ke Google Sheets: {e}")
        return False