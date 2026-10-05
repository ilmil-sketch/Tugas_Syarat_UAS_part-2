import streamlit as st
import random
import time

# Set konfigurasi halaman web
st.set_page_config(page_title="Analisis Algoritma", layout="wide")

# ==========================================
# 1. FUNGSI SORTING (Bubble Sort & Merge Sort)
# ==========================================
def bubble_sort_produk(arr, kunci_sorting):
    n = len(arr)
    b_arr = arr.copy()
    for i in range(n):
        for j in range(0, n-i-1):
            if b_arr[j][kunci_sorting] > b_arr[j+1][kunci_sorting]:
                b_arr[j], b_arr[j+1] = b_arr[j+1], b_arr[j]
    return b_arr

def merge_sort_produk(arr, kunci_sorting):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    kiri = merge_sort_produk(arr[:mid], kunci_sorting)
    kanan = merge_sort_produk(arr[mid:], kunci_sorting)
    return isi_gudang_merge(kiri, kanan, kunci_sorting)

def isi_gudang_merge(kiri, kanan, kunci_sorting):
    hasil = []
    i = j = 0
    while i < len(kiri) and j < len(kanan):
        if kiri[i][kunci_sorting] <= kanan[j][kunci_sorting]:
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil

# ============================================
# 2. FUNGSI SEARCHING (Multi-Result Cluster)
# ============================================
def binary_search_produk_banyak(arr, target, kunci_pencarian):
    steps = 0
    low = 0
    high = len(arr) - 1
    hasil_indeks = []
    
    if isinstance(target, str):
        target = target.lower()

    indeks_ketemu = -1
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        nilai_tengah = arr[mid][kunci_pencarian]
        
        if isinstance(nilai_tengah, str):
            nilai_tengah = nilai_tengah.lower()
            
        if nilai_tengah == target:
            indeks_ketemu = mid
            break
        elif nilai_tengah < target:
            low = mid + 1
        else:
            high = mid - 1
            
    if indeks_ketemu != -1:
        kiri = indeks_ketemu
        while kiri >= 0:
            nilai_kiri = arr[kiri][kunci_pencarian]
            if isinstance(nilai_kiri, str): nilai_kiri = nilai_kiri.lower()
            if nilai_kiri == target:
                if kiri not in hasil_indeks: hasil_indeks.append(kiri)
                kiri -= 1
                steps += 1
            else: break
                
        kanan = indeks_ketemu + 1
        while kanan < len(arr):
            nilai_kanan = arr[kanan][kunci_pencarian]
            if isinstance(nilai_kanan, str): nilai_kanan = nilai_kanan.lower()
            if nilai_kanan == target:
                if kanan not in hasil_indeks: hasil_indeks.append(kanan)
                kanan += 1
                steps += 1
            else: break
        hasil_indeks.sort()
        
    return hasil_indeks, steps

def linear_search_produk_banyak(arr, target, kunci_pencarian):
    steps = 0
    hasil_indeks = []
    if isinstance(target, str):
        target = target.lower()
        
    for i in range(len(arr)):
        steps += 1
        nilai_sekarang = arr[i][kunci_pencarian]
        if isinstance(nilai_sekarang, str):
            nilai_sekarang = nilai_sekarang.lower()
            
        if isinstance(target, str) and isinstance(nilai_sekarang, str):
            if target in nilai_sekarang:
                hasil_indeks.append(i)
        elif nilai_sekarang == target:
            hasil_indeks.append(i)
            
    return hasil_indeks, steps

# ==========================================
# 3. GENERATOR DATABASE PRODUK UNIK
# ==========================================
nama_mentah = [
    "Pita Satin 2cm Grid", "Pita Organza Aesthetic", "Pita Rami Vintage", "Buket Pita",
    "Replika Pedang Kawat Bulu", "Mahkota Kawat Bulu", "Topi Toga Kawat Bulu", "Gantungan Kawat Bulu",
    "Pop-Up Book Cerita Rakyat", "Kartu Ucapan Pop-Up 3D", "Diorama Kertas Mini", "Stiker Washi Tape Jurnal",
    "Kertas Vintage Scrapbook", "Buku Jurnal Kulit Kustom", "Stampel Kayu Estetik", "Lilin Aromaterapi Ukir"
]

category_mapping = {
    "Pita Satin 2cm Grid": "Aneka Pita", "Pita Organza Aesthetic": "Aneka Pita", "Pita Rami Vintage": "Aneka Pita", "Buket Pita": "Aneka Pita",
    "Replika Pedang Kawat Bulu": "Kawat Bulu Craft", "Mahkota Kawat Bulu": "Kawat Bulu Craft", "Topi Toga Kawat Bulu": "Kawat Bulu Craft", "Gantungan Kawat Bulu": "Kawat Bulu Craft",
    "Pop-Up Book Cerita Rakyat": "Pop-Up Paper Craft", "Kartu Ucapan Pop-Up 3D": "Pop-Up Paper Craft", "Diorama Kertas Mini": "Pop-Up Paper Craft",
    "Stiker Washi Tape Jurnal": "Scrapbook", "Kertas Vintage Scrapbook": "Scrapbook", "Buku Jurnal Kulit Kustom": "Scrapbook", "Stampel Kayu Estetik": "Scrapbook", "Lilin Aromaterapi Ukir": "Scrapbook"
}

def generate_database():
    random.seed(42)
    gudang_temp = []
    for i in range(200):
        id_barang = i + 101
        pilihan_nama = random.choice(nama_mentah)
        nama_barang_unik = f"{pilihan_nama} V.{id_barang}" 
        harga_barang = random.randint(2, 60) * 5000 
        kategori_barang = category_mapping.get(pilihan_nama, "Scrapbook")
        stok_barang = random.randint(10, 150)
        status_laris = "🔥 Paling Laris" if stok_barang < 40 else "🟢 Standar"
        
        gudang_temp.append({
            "ID": id_barang,
            "Nama Produk": nama_barang_unik,
            "Kategori": kategori_barang,
            "Harga": harga_barang,
            "Stok": stok_barang,
            "Penjualan": status_laris
        })
    return gudang_temp

if 'database_gudang' not in st.session_state:
    st.session_state.database_gudang = generate_database()

def reset_pencarian():
    if 'last_search' in st.session_state:
        del st.session_state['last_search']

# ==========================================
# 4. STRUKTUR INTERFACE KIRI (SIDEBAR CONTROL)
# ==========================================
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    jumlah_produk = st.slider(
        "Jumlah produk di gudang:", 
        min_value=10, max_value=200, value=200, step=10,
        on_change=reset_pencarian
    )
    
    db_aktif = st.session_state.database_gudang[:jumlah_produk]
    
    st.write("---")
    st.header("Filter Kategori")
    kategori_terpilih = st.radio(
        "Tampilkan kategori produk:",
        ("Semua Kategori", "Aneka Pita", "Kawat Bulu", "Pop-Up Paper Craft", "Scrapbook"),
        on_change=reset_pencarian
    )
    
    if kategori_terpilih == "Aneka Pita":
        db_aktif = [x for x in db_aktif if x["Kategori"] == "Aneka Pita"]
    elif kategori_terpilih == "Kawat Bulu":
        db_aktif = [x for x in db_aktif if x["Kategori"] == "Kawat Bulu Craft"]
    elif kategori_terpilih == "Pop-Up Paper Craft":
        db_aktif = [x for x in db_aktif if x["Kategori"] == "Pop-Up Paper Craft"]
    elif kategori_terpilih == "Scrapbook":
        db_aktif = [x for x in db_aktif if x["Kategori"] == "Scrapbook"]

    st.write("---")
    st.header("Kategori Kunci Data")
    kunci_data = st.selectbox(
        "Pilih Kunci Data Operasi:",
        ("Nama Produk", "Harga", "Kategori"),
        on_change=reset_pencarian
    )

    st.header("Pilih Algoritma Pencarian")
    algo_pencarian = st.radio(
        "Pilih algoritma yang ingin digunakan:",
        ("Linear Search", "Binary Search"),
        on_change=reset_pencarian
    )
    
    st.write("---")
    st.header("Kondisi Data Gudang")
    kondisi_gudang = st.radio(
        "Bagaimana kondisi data saat ini?",
        ("Data Acak (Unsorted)", "Data Terurut (Sorted)"),
        on_change=reset_pencarian
    )
    
    st.write("---")
    if st.button("🔄 Reset / Ulangi Semua Data", use_container_width=True):
        st.session_state.database_gudang = generate_database()
        reset_pencarian()
        st.rerun()

# ==========================================
# 5. STRUKTUR PANEL UTAMA (KANAN)
# ==========================================
st.title("Analisis Algoritma SEARCHING dan SORTING Berbasis Web")
st.write("Sistem Manajemen Inventaris Toko Bahan Seni & Kerajinan | Tugas Akhir Struktur Data")

inf_kol1, inf_kol2 = st.columns(2)
with inf_kol1:
    if kondisi_gudang == "Data Acak (Unsorted)":
        st.info(f"**Kondisi Data:** Data dalam keadaan ACAK (tidak terurut)")
    else:
        st.info(f"**Kondisi Data:** Data telah TERURUT berdasarkan `{kunci_data}`")
with inf_kol2:
    st.success(f"**Total Produk Aktif Sesuai Filter:** {len(db_aktif)} Items")

waktu_bubble = 0.0
waktu_merge = 0.0

if kondisi_gudang == "Data Terurut (Sorted)":
    t_start_b = time.time()
    data_bubble_test = bubble_sort_produk(db_aktif, kunci_data)
    t_end_b = time.time()
    waktu_bubble = (t_end_b - t_start_b) * 1000
    
    t_start_m = time.time()
    db_aktif = merge_sort_produk(db_aktif, kunci_data)
    t_end_m = time.time()
    waktu_merge = (t_end_m - t_start_m) * 1000

# Area Form Cari Produk
st.header("Cari Produk")

opsi_nama_produk = sorted(list(set([x["Nama Produk"] for x in db_aktif])))

with st.form(key="search_form", clear_on_submit=False):
    st.write(f"Sistem Pencarian Massal berdasarkan `{kunci_data}`")
    
    if kunci_data == "Nama Produk":
        input_user = st.multiselect(
            "Pilih/Ketik Nama Produk yang dicari (Bisa pilih lebih dari 1):",
            options=opsi_nama_produk,
            placeholder="Klik atau ketik kata kunci nama barang..."
        )
        input_user_str = ", ".join(input_user)
    else:
        placeholder_text = "Contoh jika harga: (15000, 50000)" if kunci_data == "Harga" else "Ketik: Aneka Pita / Kawat Bulu Craft / Pop-Up Paper Craft / Scrapbook"
        input_user_str = st.text_input(
            f"Masukkan {kunci_data} (Pisahkan dengan tanda koma jika mencari lebih dari 1):", 
            placeholder=placeholder_text
        )
    
    submit_button = st.form_submit_button(label="Cari Sekarang (ENTER)", use_container_width=True)

if submit_button and input_user_str:
    st.session_state['last_search'] = input_user_str

# TAMPILKAN HASIL PENCARIAN
if 'last_search' in st.session_state and st.session_state['last_search']:
    st.write("---")
    st.subheader("Laporan Hasil Analisis Pencarian Massal")
    
    target_input = st.session_state['last_search']
    daftar_target = [x.strip() for x in target_input.split(",") if x.strip() != ""]
    
    for target_mentah in daftar_target:
        if kunci_data == "Harga":
            if target_mentah.isdigit(): 
                target = int(target_mentah)
            else:
                st.error(f"Karakter `{target_mentah}` bukan angka murni! Gagal mencari kategori harga.")
                continue
        else:
            target = target_mentah

        if algo_pencarian == "Linear Search":
            t_start_s = time.time()
            daftar_idx, langkah = linear_search_produk_banyak(db_aktif, target, kunci_data)
            t_end_s = time.time()
        else:
            t_start_s = time.time()
            daftar_idx, langkah = binary_search_produk_banyak(db_aktif, target, kunci_data)
            t_end_s = time.time()
            
        waktu_search = (t_end_s - t_start_s) * 1000
        
        with st.container():
            if len(daftar_idx) > 0:
                st.success(f"🎉 **TARGET: `{target_mentah}` DITEMUKAN!** Total ada `{len(daftar_idx)}` item terdeteksi.")
                
                c1, c2 = st.columns(2)
                with c1: st.write(f"**Iterasi Langkah Cek:** `{langkah} kali`")
                with c2: st.write(f"**Kecepatan Mesin (Running Time):** `{waktu_search:.4f} ms`")
                
                for idx_hasil in daftar_idx:
                    detail = db_aktif[idx_hasil]
                    if "🔥" in detail['Penjualan']:
                        st.warning(f"📍 **Baris {idx_hasil + 1}** | ID: {detail['ID']} | **{detail['Nama Produk']}** | Kategori: *{detail['Kategori']}* | Rp {detail['Harga']} | Stok: {detail['Stok']} pcs | Status: **{detail['Penjualan']}**")
                    else:
                        st.info(f"📍 **Baris {idx_hasil + 1}** | ID: {detail['ID']} | **{detail['Nama Produk']}** | Kategori: *{detail['Kategori']}* | Rp {detail['Harga']} | Stok: {detail['Stok']} pcs | Status: {detail['Penjualan']}")
            else:
                st.error(f"❌ **TARGET: `{target_mentah}` TIDAK DITEMUKAN PADA POSISI YANG TEPAT!**")
                if kondisi_gudang == "Data Acak (Unsorted)" and algo_pencarian == "Binary Search":
                    st.warning("*Analisis Kegagalan: Binary Search gagal mendeteksi target karena Anda mencari di data yang belum diurutkan.*")
            st.write("") 

if kondisi_gudang == "Data Terurut (Sorted)":
    st.write("---")
    st.write("**Tabel Perbandingan Kecepatan Algoritma Pengurutan (Sorting):**")
    kol_t1, kol_t2 = st.columns(2)
    with kol_t1: st.metric(label="Bubble Sort Running Time", value=f"{waktu_bubble:.2f} ms")
    with kol_t2: st.metric(label="Merge Sort Running Time (Rekomendasi Dosen)", value=f"{waktu_merge:.2f} ms")

# Panel Collapse Tampilan Tabel Database Produk
st.write("---")
with st.expander("Lihat Semua Data Produk", expanded=True):
    tabel_nambah = [
        {
            "No.": idx + 1,  
            "ID": item["ID"],
            "Nama Produk": item["Nama Produk"],
            "Kategori": item["Kategori"],
            "Harga": item["Harga"],
            "Stok": item["Stok"],
            "Status Penjualan": item["Penjualan"]
        }
        for idx, item in enumerate(db_aktif)
    ]
    st.dataframe(tabel_nambah, use_container_width=True, hide_index=True)

# ==========================================
# 6. PANEL EVALUASI DINAMIS (BERUBAH SESUAI ALGORITMA)
# ==========================================
st.write("---")
with st.container():
    st.subheader(f"Catatan Evaluasi Dinamis ({algo_pencarian} Active)")
    col_eval1, col_eval2 = st.columns(2)
    
    # KONDISI 1: JIKA ALGORITMA YANG DIPILIH LINEAR SEARCH
    if algo_pencarian == "Linear Search":
        with col_eval1:
            st.markdown("""
            **🟢 Kelebihan Linear Search:**
            * **Fleksibel & Anti-Gagal:** Bisa mencari data dalam kondisi apa pun (baik data acak maupun terurut).
            * **Support Partial Match:** Lebih fleksibel dalam mendeteksi potongan kata kunci.
            * **Tanpa Syarat Pre-sorting:** Tidak membutuhkan proses pengurutan data di awal.
            """)
        with col_eval2:
            st.markdown("""
            **🔴 Kekurangan Linear Search:**
            * **Iterasi Lambat:** Menyeleksi data satu per satu dari awal sampai akhir ($O(N)$).
            * **Boros Waktu di Data Besar:** Jika posisi data ada di urutan paling akhir atau data sampai ribuan, *running time* membengkak.
            """)
            
    # KONDISI 2: JIKA ALGORITMA YANG DIPILIH BINARY SEARCH
    else:
        with col_eval1:
            st.markdown("""
            **🟢 Kelebihan Binary Search:**
            * **Super Cepat ($O(\\log N)$):** Memangkas separuh pencarian di setiap langkahnya.
            * **Sangat Efisien di Skala Besar:** Makin banyak data, waktu pencariannya tetap sangat instan.
            * **Cluster Support:** Berhasil dimodifikasi menyisir kanan-kiri untuk kategori massal.
            """)
        with col_eval2:
            st.markdown("""
            **🔴 Kekurangan Binary Search:**
            * **Wajib Data Terurut:** Gagal total jika dijalankan pada kondisi *Data Acak (Unsorted)*.
            * **Strict Target:** Kurang fleksibel jika pencarian dilakukan dengan kata kunci yang sangat acak/sepotong.
            """)
