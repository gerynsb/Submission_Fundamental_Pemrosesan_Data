import pytest
import pandas as pd
from utils.load import simpan_ke_csv, simpan_ke_mysql, simpan_ke_gsheets

@pytest.fixture
def df_dummy():
    return pd.DataFrame({'Title': ['A'], 'Price': [1000]})

def test_simpan_ke_csv(mocker, df_dummy):
    mock_to_csv = mocker.patch.object(pd.DataFrame, 'to_csv')
    hasil = simpan_ke_csv(df_dummy, 'test.csv')
    assert hasil is True
    mock_to_csv.assert_called_once()

def test_simpan_ke_mysql(mocker, df_dummy):
    mock_engine = mocker.patch('utils.load.create_engine')
    mock_to_sql = mocker.patch.object(pd.DataFrame, 'to_sql')
    hasil = simpan_ke_mysql(df_dummy, 'sqlite:///:memory:') # Dummy URI
    assert hasil is True
    mock_engine.assert_called_once()
    mock_to_sql.assert_called_once()

def test_simpan_ke_gsheets(mocker, df_dummy):
    mocker.patch('utils.load.service_account.Credentials.from_service_account_file')
    mock_build = mocker.patch('utils.load.build')
    
    # Simulasi rantai API Google
    mock_sheet = mocker.Mock()
    mock_build.return_value.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = {'updatedCells': 2}
    
    hasil = simpan_ke_gsheets(df_dummy, 'dummy_id', 'dummy.json')
    assert hasil is True