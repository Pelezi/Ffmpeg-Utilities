import os
import subprocess

# Define source and destination folders
source_folder = r"C:\Users\Path\To\Your\MP4s"
destination_folder = r"C:\Users\Path\To\Your\MP3s"

# Gather all .mp4 files
mp4_files = []
for root, _, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith('.mp4'):
            mp4_files.append(os.path.join(root, file))

total = len(mp4_files)
for idx, mp4_file in enumerate(mp4_files, start=1):
    # Compute destination path
    relative_path    = os.path.relpath(mp4_file, source_folder)
    destination_file = os.path.join(
        destination_folder,
        relative_path.replace('.mp4', '.mp3')
    )
    os.makedirs(os.path.dirname(destination_file), exist_ok=True)

    # Progress indicator
    print(f"Converting [{idx}/{total}]: {os.path.basename(mp4_file)}")

    # FFmpeg command:
    #  -hide_banner: no header
    #  -loglevel fatal: silence warnings/errors below fatal
    #  -stats: show progress stats
    cmd = [
        'ffmpeg',
        '-hide_banner',
        '-loglevel', 'fatal',
        '-stats',
        '-i', mp4_file,
        '-q:a', '0',
        '-map', 'a',
        destination_file
    ]

    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"⚠️ Error converting {os.path.basename(mp4_file)} (exit code {result.returncode})")

print("✅ All files converted!")
