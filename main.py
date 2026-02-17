import subprocess
import sys
import os
from pathlib import Path

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ambil file audio pertama di folder uploads
files = list(Path(UPLOAD_DIR).glob("*.*"))
if not files:
    print("❌ Upload file audio dulu di folder 'uploads/'")
    sys.exit(1)

audio_file = str(files[0])
print(f"✅ Found upload: {audio_file}")

def run(cmd):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

# Run Demucs separation
print("🎧 Running Demucs AI separation...")
run(f"demucs {audio_file}")

# Path folder hasil demucs (biasanya htdemucs)
base = f"separated/htdemucs/{Path(audio_file).stem}"

# Merge tracks tanpa bass + Naikin Volume ke 150%
print("🎚 Removing bass, merging others, and boosting volume to 150%...")
nobass_wav = f"{OUTPUT_DIR}/nobass.wav"

# Penjelasan: volume=1.5 artinya 150%. 1.0 itu normal (100%).
run(f'ffmpeg -i "{base}/drums.wav" -i "{base}/vocals.wav" -i "{base}/other.wav" '
    f'-filter_complex "amix=inputs=3:dropout_transition=0,volume=1.5" {nobass_wav}')

# Convert ke mp3
output_mp3 = f"{OUTPUT_DIR}/nobass.mp3"
print("🔊 Converting to mp3...")
run(f"ffmpeg -i {nobass_wav} {output_mp3}")

print(f"✅ DONE! Hasil (Volume 150%) ada di {output_mp3}")
