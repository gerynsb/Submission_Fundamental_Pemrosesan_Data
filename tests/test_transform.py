import pandas as pd
from utils.transform import transform_data

def test_transform_data_success():
    dirty_data = [
        {"Title": "T-shirt 1", "Price": "$10.00", "Rating": "Rating: ⭐️ 4.5 / 5", "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Men"},
        {"Title": "Unknown Product", "Price": "Price Unavailable", "Rating": "Not Rated", "Colors": "0 Colors", "Size": "Size: M", "Gender": "Gender: Men"}, # Harus terfilter
    ]
    
    result_df = transform_data(dirty_data)
    
    assert len(result_df) == 1
    assert result_df['Title'].iloc[0] == "T-shirt 1"
    assert result_df['Price'].iloc[0] == 160000.0  # 10 * 16000
    assert result_df['Rating'].iloc[0] == 4.5
    assert result_df['Colors'].iloc[0] == 3
    assert result_df['Size'].iloc[0] == "M"
    assert result_df['Gender'].iloc[0] == "Men"
    assert "Timestamp" in result_df.columns

def test_transform_data_exception():
    # Melempar data yang bukan format list dict untuk memicu blok except
    result_df = transform_data(None)
    assert result_df.empty