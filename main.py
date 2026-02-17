import subprocess
import sys
import os
from pathlib import Path

# Folder setup
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ambil file audio pertama di folder uploads
files = list(Path(UPLOAD_DIR).glob("*.*"))
if not list(files):
    print("❌ Upload file audio dulu di folder 'uploads/'")
    sys.exit(1)

# Ambil path lengkap file pertama
audio_file = str(files[0])
# Ambil nama file tanpa extension (untuk path hasil demucs)
file_stem = files[0].stem

print(f"✅ Found upload: {audio_file}")

def run(cmd):
    print(f"> {cmd}")
    # shell=True butuh quotes ekstra buat jaga-jaga spasi
    subprocess.run(cmd, shell=True, check=True)

# 1. Run Demucs separation (pake kutip di {audio_file})
print("🎧 Running Demucs AI separation...")
run(f'demucs "{audio_file}"')

# 2. Path folder hasil demucs (pake file_stem yang udah fix)
# Demucs biasanya bikin folder sesuai nama file di 'separated/htdemucs/'
base = os.path.join("separated", "htdemucs", file_stem)

# 3. Merge tracks tanpa bass + Naikin Volume ke 150%
print("🎚 Removing bass, merging others, and boosting volume to 150%...")
nobass_wav = os.path.join(OUTPUT_DIR, "nobass.wav")

# Kita bungkus setiap input path dengan kutip dua (")
ffmpeg_cmd = (
    f'ffmpeg -y -i "{base}/drums.wav" -i "{base}/vocals.wav" -i "{base}/other.wav" '
    f'-filter_complex "amix=inputs=3:dropout_transition=0,volume=1.5" "{nobass_wav}"'
)
run(ffmpeg_cmd)

# 4. Convert ke mp3
output_mp3 = os.path.join(OUTPUT_DIR, "nobass.mp3")
print("🔊 Converting to mp3...")
run(f'ffmpeg -y -i "{nobass_wav}" "{output_mp3}"')

print(f"✅ DONE! Hasil ada di: {output_mp3}")
