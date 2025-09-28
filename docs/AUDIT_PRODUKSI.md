# AUDIT PRODUKSI / RELEASE ADDON BLENDER

Dokumen ini digunakan untuk audit kesiapan produksi sebelum merilis addon Blender.  
Setiap poin harus diperiksa dan dicentang ✅ sebelum addon dipublikasikan.

---

## 1. Kode & Struktur
- [ ] Folder addon memiliki struktur rapi (`addon_name/__init__.py`, `modules/`, `icons/`, `docs/`).
- [ ] Semua file `.py` memiliki **license header** (GPL atau lisensi lain yang sesuai).
- [ ] Tidak ada kode debug (`print`, `breakpoint()`, log sementara).
- [ ] Kode mengikuti **PEP8** (formatting, indentasi, line length ≤120).
- [ ] Hanya import yang diperlukan, tanpa library eksternal ilegal.
- [ ] File `__init__.py` memiliki `bl_info` lengkap (name, author, version, description, category, location, wiki).

---

## 2. Fungsionalitas
- [ ] Semua operator, panel, menu, dan handler berjalan tanpa error.
- [ ] Kompatibilitas dengan **Blender 3.6 LTS** dan versi terbaru.
- [ ] Tes di **Windows**, **macOS**, dan **Linux** (jika memungkinkan).
- [ ] Tidak ada error/traceback saat addon di-enable/disable.
- [ ] Tes edge case (file kosong, tanpa lampu, banyak kamera/scene).

---

## 3. UI & UX
- [ ] Semua tombol/operator memiliki label jelas, tidak ada placeholder.
- [ ] Tooltips tersedia (`description` atau `bl_description`).
- [ ] Ikon konsisten (gunakan bawaan Blender atau custom legal).
- [ ] Shortcut dan modal operator terdokumentasi, tidak bentrok dengan default Blender.
- [ ] UI layout rapi pada resolusi dan DPI berbeda.

---

## 4. Lisensi & Legal
- [ ] Header lisensi tersedia di setiap file `.py`.
- [ ] File `LICENSE` lengkap ada di root addon.
- [ ] Asset (ikon, gambar, shader) memiliki hak distribusi yang jelas.

---

## 5. Dokumentasi
- [ ] `README.md` berisi:
  - Nama addon + logo/icon
  - Deskripsi singkat
  - Cara instalasi
  - Cara penggunaan dasar
  - Screenshot/gif contoh
- [ ] `CHANGELOG.md` berisi riwayat versi.
- [ ] Dokumentasi online (Wiki/Website/GitHub Pages) tersedia.
- [ ] Panduan kontribusi (opsional).

---

## 6. Distribusi
- [ ] Instalasi `.zip` berhasil via Blender Preferences > Add-ons > Install.
- [ ] Addon bisa enable/disable tanpa restart Blender.
- [ ] Nama paket konsisten dengan versi (`addon_name_vX.Y.zip`).
- [ ] Tidak ada file sampah (`.git/`, `.vscode/`, `__pycache__/`, `.DS_Store`).

---

## 7. Marketing & Support (Opsional)
- [ ] Screenshot promo resolusi tinggi tersedia.
- [ ] Video demo singkat dibuat.
- [ ] Slogan/tagline jelas.
- [ ] FAQ untuk masalah umum tersedia.
- [ ] Kanal support aktif (Email, GitHub Issues, Discord).

---

✅ Jika semua poin sudah dicentang, addon siap untuk **release publik/produksi**.
