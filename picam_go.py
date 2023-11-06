import subprocess

# Run picam_downloader.py
subprocess.run(["python3", "picam_downloader.py"])

# Run picam_lux_remover.py
subprocess.run(["python3", "picam_lux_remover.py"])

# Run picam_movie_maker.py
subprocess.run(["python3", "picam_movie_maker.py"])