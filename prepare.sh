#!/usr/bin/env bash
sudo apt-get update
sudo apt-get -y install python3 python3-pip tesseract-ocr=4.1.1-2build2
#brew install  tesseract
#apt-cache policy  tesseract-ocr
pip3 install -r requirements.txt
