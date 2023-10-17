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
