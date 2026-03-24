import pytest
import pandas as pd
from utils.extract import jalankan_ekstraksi, ambil_elemen_teks
from bs4 import BeautifulSoup
import requests

def test_ambil_elemen_teks():
    html = '<div class="test"><p class="price">$10</p></div>'
    soup = BeautifulSoup(html, 'html.parser')
    # Tes elemen ditemukan
    assert ambil_elemen_teks(soup, 'p', 'price') == '$10'
    # Tes elemen tidak ditemukan
    assert ambil_elemen_teks(soup, 'h3') is None

def test_jalankan_ekstraksi_sukses(mocker):
    mock_html = """
    <div class="collection-card">
        <div class="product-details">
            <h3 class="product-title">T-shirt A</h3>
            <p class="price">$10.00</p>
            <p>Rating: ⭐ 4.5 / 5</p>
            <p>3 Colors</p><p>Size: M</p><p>Gender: Men</p>
        </div>
    </div>
    """
    mock_response = mocker.Mock()
    mock_response.content = mock_html
    
    # Patch requests.Session.get agar tidak menembak internet asli
    mocker.patch('requests.Session.get', return_value=mock_response)
    # Batasi halaman tes jadi 1 saja agar tidak loop 50 kali saat testing
    mocker.patch('utils.extract.TOTAL_HALAMAN', 1)
    
    df = jalankan_ekstraksi()
    assert not df.empty
    assert len(df) == 1
    assert df['Title'][0] == 'T-shirt A'

def test_jalankan_ekstraksi_error(mocker, caplog):
    mocker.patch('requests.Session.get', side_effect=requests.exceptions.RequestException("Koneksi Putus"))
    mocker.patch('utils.extract.TOTAL_HALAMAN', 1)
    
    df = jalankan_ekstraksi()
    assert df.empty
    assert "Koneksi Putus" in caplog.text