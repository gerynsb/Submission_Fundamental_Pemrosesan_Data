import pandas as pd
from datetime import datetime

def transform_data(raw_data):
    """Membersihkan dan memanipulasi data mentah menjadi format yang sesuai."""
    try:
        if not raw_data:
            return pd.DataFrame()

        df = pd.DataFrame(raw_data)

        # 1. Hapus data kosong dan duplikat
        df = df.dropna()
        df = df.drop_duplicates()

        # 2. Filter invalid data
        df = df[df['Title'] != 'Unknown Product']
        df = df[df['Price'] != 'Price Unavailable']
        df = df[~df['Rating'].str.contains('Invalid Rating|Not Rated', na=False)]

        # 3. Transformasi Kolom Price (Hapus $ -> float -> * 16000)
        df['Price'] = df['Price'].str.replace('$', '', regex=False) \
                                 .str.replace(',', '', regex=False) \
                                 .astype(float) * 16000.0

        # 4. Transformasi Kolom Rating (Ambil angka float)
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)').astype(float)

        # 5. Transformasi Kolom Colors (Ambil angka int)
        df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(int)

        # 6. Transformasi Kolom Size & Gender (Hapus prefix)
        df['Size'] = df['Size'].str.replace('Size: ', '', regex=False).str.strip()
        df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False).str.strip()

        # 7. Tambahkan Timestamp
        df['Timestamp'] = datetime.now().isoformat()

        # Bersihkan sisa NaN akibat regex extract yang mungkin gagal di data aneh
        df = df.dropna()
        
        # Pastikan tipe data sesuai ekspektasi
        df['Price'] = df['Price'].astype('float64')
        df['Rating'] = df['Rating'].astype('float64')
        df['Colors'] = df['Colors'].astype('int64')

        return df.reset_index(drop=True)
    except Exception as e:
        print(f"Error during transformation: {e}")
        return pd.DataFrame()