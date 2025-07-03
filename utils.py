import os
def simpan_hasil_scraping(nama_profil_tiktok: str, daftar_link_baru: list):
    """
    Menyimpan daftar link hasil scraping ke dalam file, menangani duplikasi.

    Args:
        nama_profil_tiktok (str): Nama profil TikTok untuk nama file.
        daftar_link_baru (list): Daftar link baru yang akan ditambahkan.
    """
    result_dir = "result"
    try:
        # 1. Periksa dan buat folder 'result' jika belum ada
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
            print(f"Folder '{result_dir}' berhasil dibuat.")

        # 2. Tentukan path file target
        file_path = os.path.join(result_dir, f"{nama_profil_tiktok}.txt")

        # 3. Baca link yang sudah ada dari file (jika ada)
        link_yang_ada = set()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                link_yang_ada.update(line.strip() for line in f)

        # 4. Gabungkan dan hilangkan duplikat secara efisien menggunakan set
        semua_link_unik = link_yang_ada.union(set(daftar_link_baru))

        # 5. Tulis kembali semua link unik ke file
        with open(file_path, 'w', encoding='utf-8') as f:
            for link in sorted(list(semua_link_unik)):
                f.write(f"{link}\n")
        
        print(f"Berhasil menyimpan {len(semua_link_unik)} link unik ke {file_path}")

    except IOError as e:
        print(f"Error saat menulis ke file: {e}")
    except Exception as e:
        print(f"Terjadi error tak terduga: {e}")