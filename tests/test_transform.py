import pytest
import pandas as pd
from utils.transform import bersihkan_data

def test_bersihkan_data_sukses():
    data_kotor = pd.DataFrame({
        'Title': ['Baju Bagus', 'Unknown Product'],
        'Price': ['$10.00', 'Price Unavailable'],
        'Rating': ['Rating: ⭐ 4.0 / 5', 'Invalid Rating'],
        'Colors': ['2 Colors', '0 Colors'],
        'Size': ['Size: L', 'Size: S'],
        'Gender': ['Gender: Unisex', 'Gender: Men']
    })
    
    df_bersih = bersihkan_data(data_kotor)
    
    # Baris kedua harus hilang karena Unknown Product
    assert len(df_bersih) == 1
    assert df_bersih['Title'].iloc[0] == 'Baju Bagus'
    assert df_bersih['Price'].iloc[0] == 160000.0
    assert df_bersih['Rating'].iloc[0] == 4.0
    assert df_bersih['Colors'].iloc[0] == 2
    assert df_bersih['Size'].iloc[0] == 'L'
    assert df_bersih['Gender'].iloc[0] == 'Unisex'
    assert 'timestamp' in df_bersih.columns

def test_bersihkan_data_kosong():
    df_kosong = pd.DataFrame()
    hasil = bersihkan_data(df_kosong)
    assert hasil.empty