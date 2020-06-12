#!/bin/bash
source $HOME/.bash_profile
cd /home/pi/Desktop/AQI/aqi
sudo scrapy crawl manual -o data.json -t json
sudo python sendEmail.py