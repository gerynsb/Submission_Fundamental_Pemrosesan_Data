from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_mysql, load_to_gsheets

def main():
    print("Mulai proses Ekstraksi...")
    # Batasi page kecil dulu saat testing lokal, ganti ke 50 saat submission final
    raw_data = extract_data(total_pages=50) 
    
    if raw_data:
        print(f"Ekstraksi selesai. Memulai Transformasi untuk {len(raw_data)} baris data kotor...")
        clean_df = transform_data(raw_data)
        
        if not clean_df.empty:
            print(f"Transformasi selesai. Memuat {len(clean_df)} baris data bersih...")
            
            # 1. Load to CSV
            load_to_csv(clean_df, 'products.csv')
            
            # 2. Load to MySQL (Sesuaikan user, password, host, dan nama DB)
            load_to_mysql(clean_df, db_user='root', db_pass='', db_host='localhost', db_name='dicoding_etl')
            
            # 3. Load to Google Sheets (Masukkan SPREADSHEET_ID dari URL Spreadsheet Anda)
            # URL Sheets: https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
            SPREADSHEET_ID = '1cBs2aDrhI5N5iuzBLFYfqvCiFitV2_VkUX_rO_UKF_c'
            load_to_gsheets(clean_df, SPREADSHEET_ID)
            
            print("ETL Pipeline Selesai!")
        else:
            print("Gagal: Dataframe hasil transformasi kosong.")
    else:
        print("Gagal: Tidak ada data yang berhasil diekstrak.")

if __name__ == "__main__":
    main()