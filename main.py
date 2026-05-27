import subprocess
import sys
import os
from pathlib import Path

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

files = list(Path(UPLOAD_DIR).glob("*.*"))
if not files:
    print("❌ Upload file audio dulu di folder 'uploads/'")
    sys.exit(1)

def run(cmd):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

for audio_path in files:
    audio_file = str(audio_path)
    file_stem = audio_path.stem
    original_name = audio_path.name  # misal: lagu1.mp3

    print(f"\n🎵 Processing: {original_name}")

    # 1. Demucs separation
    print("🎧 Running Demucs AI separation...")
    run(f'demucs "{audio_file}"')

    # 2. Path folder hasil demucs
    base = os.path.join("separated", "htdemucs", file_stem)

    # 3. Merge tracks tanpa bass + volume 1.95x (1.5 * 1.3 = boost 30% dari original)
    print("🎚 Removing bass, merging, and boosting volume...")
    nobass_wav = os.path.join(OUTPUT_DIR, f"{file_stem}_nobass.wav")

    ffmpeg_cmd = (
        f'ffmpeg -y -i "{base}/drums.wav" -i "{base}/vocals.wav" -i "{base}/other.wav" '
        f'-filter_complex "amix=inputs=3:dropout_transition=0,volume=1.95" "{nobass_wav}"'
    )
    run(ffmpeg_cmd)

    # 4. Convert ke mp3 dengan nama sama kayak file asli
    output_mp3 = os.path.join(OUTPUT_DIR, original_name)
    print(f"🔊 Converting to mp3: {output_mp3}")
    run(f'ffmpeg -y -i "{nobass_wav}" "{output_mp3}"')

    # 5. Bersihin wav temp
    os.remove(nobass_wav)

    # 6. Bersihin folder separated biar ga numpuk
    run(f'rm -rf "separated/htdemucs/{file_stem}"')

    print(f"✅ Done: {output_mp3}")

print("\n🎉 Semua file selesai diproses!")
