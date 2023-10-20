# rpi_timelapse
A timelapse camera app for RPI which also gets sunrises and sunsets

The local sunrise and sunset times can be obtained using get_sunrise_sunset.py. Change the gps location
The timelapser is installed and run at boot by cron. 

```
################################################
# Start timelasper camera script
#/home/icrucrob/picam
@reboot /usr/bin/python3 /home/icrucrob/picam/timelapser.py >> /home/icrucrob/picam/logfile.log 2>&1
################################################
```

## Make a video based on the images
This sorts the files in chronological order before making the file. 
Change framerate appropriately

```
cat $(ls -1 *.jpg | sort) | ffmpeg -f image2pipe -framerate 30 -i - -c:v libx264 -pix_fmt yuv420p -vf "scale=1920:1080" -y output/my_video.mp4
```

