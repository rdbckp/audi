import os
import shutil
import subprocess

# 1. Cari file audio di folder uploads
upload_dir = 'uploads'
output_dir = 'output'
audio_files = [f for f in os.listdir(upload_dir) if f.endswith(('.mp3', '.wav', '.flac'))]

if not audio_files:
    print("Gak ada file di folder uploads, Bro!")
    exit()

input_file = os.path.join(upload_dir, audio_files[0])
filename_no_ext = os.path.splitext(audio_files[0])[0]

# 2. Jalankan Demucs buat misahin stem
# Kita pakai htdemucs (default 4 stems: drums, bass, other, vocals)
print(f"Lagi proses: {input_file}")
subprocess.run(["demucs", "-n", "htdemucs", input_file])

# 3. Lokasi hasil demucs biasanya di: separated/htdemucs/nama_file/bass.wav
bass_source = f"separated/htdemucs/{filename_no_ext}/bass.wav"

# 4. Pindahin file bass.wav ke folder output
if os.path.exists(bass_source):
    # Kasih nama baru biar jelas
    target_path = os.path.join(output_dir, f"{filename_no_ext}_BASS_ONLY.wav")
    shutil.copy(bass_source, target_path)
    print(f"Berhasil! File bass ada di: {target_path}")
else:
    print("Waduh, file bass gak ketemu!")
