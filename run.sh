#!/bin/bash

#DRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz"
DRIVER_URL="https://repo.huaweicloud.com/geckodriver/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz"

if [ ! -x "geckodriver" ];
then
  rm -f geckodriver*
  curl -s -o geckodriver.tar.gz $DRIVER_URL
  tar -zxf geckodriver.tar.gz
  rm -f *.tar.gz
fi

pip install --user -r requirements.txt
python main.py
