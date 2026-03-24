import pandas as pd
from utils.load import load_to_csv, load_to_mysql, load_to_gsheets

def test_load_to_csv(mocker):
    df = pd.DataFrame({"col1": [1, 2]})
    mock_to_csv = mocker.patch.object(pd.DataFrame, 'to_csv')
    load_to_csv(df, 'test.csv')
    mock_to_csv.assert_called_once_with('test.csv', index=False)

def test_load_to_mysql(mocker):
    df = pd.DataFrame({"col1": [1, 2]})
    mock_create_engine = mocker.patch('utils.load.create_engine')
    mock_to_sql = mocker.patch.object(pd.DataFrame, 'to_sql')
    
    load_to_mysql(df, 'user', 'pass', 'host', 'db', 'table')
    mock_create_engine.assert_called_once()
    mock_to_sql.assert_called_once()