#!/usr/bin/env bash
sudo apt-get update
sudo apt-get -y install tesseract-ocr=4.1.1-2build2
#apt-cache policy  tesseract-ocr
pip3 install -r requirements.txt
