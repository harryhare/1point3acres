# for public github action
# debian
# size: 729MB
from debian:latest
#copy docker/debian.aliyun.sources.list /etc/apt/sources.list
#copy docker/pip.conf /root/.pip/pip.conf
run apt-get update
run apt-get -y install python3 python3-pip tesseract-ocr
run pip3 install requests lxml pytesseract cssselect
copy src /app/src/
copy configure /app/configure
env PYTHONIOENCODING=utf8
ENTRYPOINT ["python3","/app/src/service.py"]

