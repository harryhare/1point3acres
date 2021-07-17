#!/usr/bin/env bash
sudo apt-get update
# 如果找不到 tesseract-ocr，请按照下面链接的说明增加 ppa
# https://launchpad.net/~alex-p/+archive/ubuntu/tesseract-ocr-devel
# https://notesalexp.org/tesseract-ocr/
sudo apt-get -y install python3 python3-pip tesseract-ocr=4.1.1-2build2
#brew install  tesseract
#apt-cache policy  tesseract-ocr
pip3 install -r requirements.txt
