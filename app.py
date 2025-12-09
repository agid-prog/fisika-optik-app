import os
from flask import Flask, render_template, request
import math

# Inisialisasi Aplikasi Flask
# Nama variabel aplikasi HARUS "app" agar Gunicorn bisa menemukannya
app = Flask(__name__)

# Database sederhana material (digunakan oleh route /material)
material_data = [
    {"nama": "Udara", "n": 1.0003},
    {"nama": "Air", "n": 1.33},
    {"nama": "Kaca", "n": 1.5},
    {"nama": "Akrilik", "n": 1.49},
    {"nama": "Intan", "n": 2.42}
]

# Route untuk Beranda (index.html)
@app.route("/")
def index():
    return render_template("index.html", title="Beranda")

# Route untuk Refleksi (refleksi.html)
@app.route("/refleksi")
def refleksi():
    return render_template("refleksi.html", title="Simulasi Refleksi")

# Route untuk Pembiasan (pembiasaan.html) dengan logika POST (Hukum Snellius)
@app.route("/pembiasaan", methods=["GET", "POST"])
def pembiasaan():
    hasil = None
    sudut_datang = n1 = n2 = None

    if request.method == "POST":
        try:
            sudut_datang = float(request.form["sudut_datang"])
            n1 = float(request.form["n1"])
            n2 = float(request.form["n2"])
            sudut_datang_rad = math.radians(sudut_datang)

            sin_sudut_bias = (n1 / n2) * math.sin(sudut_datang_rad)

            if abs(sin_sudut_bias) > 1:
                # Total Internal Reflection
                hasil = "Terjadi Total Internal Reflection (TIR). Tidak ada pembiasan."
            else:
                # Pembiasan Normal (Hukum Snellius)
                sudut_bias = math.degrees(math.asin(sin_sudut_bias))
                hasil = f"Sudut bias = {sudut_bias:.2f}°"

        except ValueError:
            hasil = "Input tidak valid. Pastikan angka sudah benar."
        except Exception:
            hasil = "Terjadi error tak terduga."

    # Mengirim data yang telah diinput kembali ke template untuk ditampilkan
    return render_template("pembiasaan.html", title="Simulasi Pembiasaan",
                            hasil=hasil, sudut_datang=sudut_datang, n1=n1, n2=n2,
                            material_data=material_data)

# Route untuk Polarisasi (polarisasi.html)
@app.route("/polarisasi")
def polarisasi():
    return render_template("polarisasi.html", title="Simulasi Polarisasi")

# Route untuk Database Material (material.html)
@app.route("/material")
def material():
    return render_template("material.html", title="Database Material", materials=material_data)

# Bagian ini hanya untuk testing LOKAL
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)