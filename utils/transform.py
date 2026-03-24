import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def bersihkan_data(df_kotor):
    """Membersihkan dan memformat DataFrame menggunakan vektorisasi Pandas."""
    if df_kotor.empty:
        logging.warning("DataFrame input kosong.")
        return pd.DataFrame()

    logging.info("Memulai tahap transformasi data...")
    df = df_kotor.copy()

    try:
        # 1. Hapus baris dengan nilai invalid utama terlebih dahulu
        df = df[df['Title'] != 'Unknown Product']
        df = df[df['Price'] != 'Price Unavailable']
        df = df[~df['Rating'].str.contains('Invalid Rating|Not Rated', na=False)]

        # 2. Vektorisasi Transformasi (Jauh lebih cepat dari iterasi/apply)
        # Regex: ambil angka dan buang tanda '$' atau ',' lalu kali 16000
        df['Price'] = df['Price'].str.replace(r'[\$\,]', '', regex=True).astype(float) * 16000.0
        
        # Regex: ekstrak hanya angka desimal untuk rating
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        
        # Regex: ekstrak hanya angka bulat untuk warna
        df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(float).astype('Int64') # Int64 Pandas mentoleransi NaN sementara

        # String replace untuk Size dan Gender
        df['Size'] = df['Size'].str.replace('Size: ', '', regex=False).str.strip()
        df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False).str.strip()

        # 3. Tambahkan timestamp
        df['timestamp'] = datetime.now().isoformat()

        # 4. Hapus duplikat dan baris yang masih mengandung NaN (missing values)
        baris_awal = len(df)
        df = df.dropna().drop_duplicates()
        logging.info(f"Menghapus {baris_awal - len(df)} baris duplikat atau bernilai kosong.")

        # 5. Konfirmasi tipe data final
        df['Price'] = df['Price'].astype('float64')
        df['Rating'] = df['Rating'].astype('float64')
        df['Colors'] = df['Colors'].astype('int64')

        logging.info("Transformasi sukses.")
        return df.reset_index(drop=True)

    except Exception as e:
        logging.error(f"Gagal saat mentransformasi data: {e}", exc_info=True)
        return pd.DataFrame()