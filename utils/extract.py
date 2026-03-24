import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL_TARGET = "https://fashion-studio.dicoding.dev"
TOTAL_HALAMAN = 50

def ambil_elemen_teks(elemen, selektor, nama_class=None):
    """Fungsi bantu untuk menghindari error AttributeError saat elemen None"""
    try:
        if nama_class:
            ditemukan = elemen.find(selektor, class_=nama_class)
        else:
            ditemukan = elemen.find(selektor)
        return ditemukan.text.strip() if ditemukan else None
    except Exception:
        return None

def jalankan_ekstraksi():
    """Mengekstrak seluruh halaman website menjadi DataFrame."""
    logging.info("Memulai proses ekstraksi web...")
    semua_produk = []
    
    # Menggunakan Session agar koneksi lebih efisien untuk banyak halaman
    sesi = requests.Session()
    
    for halaman in range(1, TOTAL_HALAMAN + 1):
        # Penanganan URL untuk pagination
        url = f"{URL_TARGET}/page{halaman}" if halaman > 1 else URL_TARGET
        
        try:
            respons = sesi.get(url, timeout=15)
            respons.raise_for_status()  # Memastikan status 200 OK
            
            sup = BeautifulSoup(respons.content, 'html.parser')
            daftar_kartu = sup.find_all('div', class_='collection-card')
            
            if not daftar_kartu:
                logging.warning(f"Tidak ada kartu produk di halaman {halaman}")
                continue

            for kartu in daftar_kartu:
                detail = kartu.find('div', class_='product-details')
                if not detail: continue

                # Mencari harga (bisa di dalam span.price atau langsung di p.price)
                wadah_harga = detail.find('div', class_='price-container')
                harga_teks = ambil_elemen_teks(wadah_harga, 'span', 'price') if wadah_harga else ambil_elemen_teks(detail, 'p', 'price')

                # Mengambil elemen <p> untuk rating, warna, ukuran, gender
                kumpulan_p = detail.find_all('p')
                teks_paragraf = [p.text.strip() for p in kumpulan_p]

                produk = {
                    'Title': ambil_elemen_teks(detail, 'h3', 'product-title'),
                    'Price': harga_teks,
                    'Rating': next((t for t in teks_paragraf if 'Rating:' in t), None),
                    'Colors': next((t for t in teks_paragraf if 'Color' in t), None),
                    'Size': next((t for t in teks_paragraf if 'Size:' in t), None),
                    'Gender': next((t for t in teks_paragraf if 'Gender:' in t), None)
                }
                semua_produk.append(produk)
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Gagal mengambil data di halaman {halaman}: {e}")
        except Exception as e:
            logging.error(f"Terjadi kesalahan tak terduga pada halaman {halaman}: {e}")

    logging.info(f"Ekstraksi selesai. Total data kotor: {len(semua_produk)} baris.")
    return pd.DataFrame(semua_produk)