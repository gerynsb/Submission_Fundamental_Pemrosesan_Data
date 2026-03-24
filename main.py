import logging
from utils.extract import jalankan_ekstraksi
from utils.transform import bersihkan_data
from utils.load import simpan_ke_csv, simpan_ke_mysql, simpan_ke_gsheets

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Kredensial Pribadi Anda
DB_URI = "mysql+pymysql://root:dean@localhost:3306/dicoding_etl"
SPREADSHEET_ID = "1cBs2aDrhI5N5iuzBLFYfqvCiFitV2_VkUX_rO_UKF_c"

def orkestrator_etl():
    logging.info("=== MEMULAI PIPELINE ETL ===")
    
    # 1. Extract
    df_mentah = jalankan_ekstraksi()
    if df_mentah.empty:
        logging.error("Pipeline dihentikan: Data mentah kosong.")
        return

    # 2. Transform
    df_bersih = bersihkan_data(df_mentah)
    if df_bersih.empty:
        logging.error("Pipeline dihentikan: Data bersih kosong setelah transformasi.")
        return
        
    logging.info(f"Data siap dimuat: {len(df_bersih)} baris.")

    # 3. Load
    simpan_ke_csv(df_bersih)
    simpan_ke_mysql(df_bersih, DB_URI)
    simpan_ke_gsheets(df_bersih, SPREADSHEET_ID)
    
    logging.info("=== PIPELINE ETL SELESAI DENGAN SUKSES ===")

if __name__ == "__main__":
    orkestrator_etl()