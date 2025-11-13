from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

# Konfigurasi dasar Flask
app = Flask(__name__)
app.secret_key = 'devsecret'

# Folder untuk upload file musik
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ekstensi file yang diizinkan
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

# Database sementara (pakai list dulu, nanti bisa diganti SQLAlchemy)
tracks = []

# Fungsi untuk validasi ekstensi file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --------------------------
# ROUTES
# --------------------------

@app.route('/')
def index():
    return redirect(url_for('artist_dashboard'))


@app.route('/artist/dashboard')
def artist_dashboard():
    """
    Halaman dashboard artis:
    - Menampilkan daftar lagu yang telah diupload
    - Tombol untuk upload lagu baru
    """
    return render_template('artist_dashboard.html', tracks=tracks)


@app.route('/artist/upload', methods=['GET', 'POST'])
def upload_track():
    """
    Halaman upload lagu:
    - Form upload file, judul lagu, harga
    - File disimpan di folder uploads/
    """
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        file = request.files.get('file')

        # Validasi form
        if not title or not file:
            flash("Judul dan file wajib diisi!")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Format file tidak didukung. Gunakan mp3/wav/ogg.")
            return redirect(request.url)

        # Simpan file
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # Simpan data ke list (sementara)
        track = {'title': title, 'price': price, 'filename': filename}
        tracks.append(track)

        flash("Lagu berhasil diupload!")
        return redirect(url_for('artist_dashboard'))

    return render_template('upload_track.html')


if __name__ == '__main__':
    app.run(debug=True)

import os
print("Current working directory:", os.getcwd())
