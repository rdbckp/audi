import os
import subprocess

# 1. Cari file di folder uploads
upload_dir = 'uploads'
output_dir = 'output'
audio_files = [f for f in os.listdir(upload_dir) if f.endswith(('.mp3', '.wav', '.flac'))]

if not audio_files:
    print("Gak ada file di folder uploads!")
    exit()

input_file = os.path.join(upload_dir, audio_files[0])
filename_no_ext = os.path.splitext(audio_files[0])[0]

# 2. Jalankan Demucs [cite: 3]
print(f"Lagi proses pisahin audio: {input_file}")
subprocess.run(["demucs", "-n", "htdemucs", input_file])

# 3. Path file bass hasil demucs
bass_wav = f"separated/htdemucs/{filename_no_ext}/bass.wav"

# 4. Convert ke MP3 pakai FFmpeg 
if os.path.exists(bass_wav):
    target_mp3 = os.path.join(output_dir, f"{filename_no_ext}_BASS_ONLY.mp3")
    print(f"Converting ke MP3: {target_mp3}")
    
    # Perintah FFmpeg: -q:a 2 itu kualitas VBR yang bagus (sekitar 190kbps)
    subprocess.run([
        "ffmpeg", "-i", bass_wav, 
        "-codec:a", "libmp3lame", 
        "-q:a", "2", 
        target_mp3
    ])
    print("Selesai, Bro!")
else:
    print("File bass.wav gak ketemu!")
