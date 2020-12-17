# aselva
  
# Raspberry Pi OS with desktop
version: Raspbian GNU/Linux 10 (buster)
  
# Install Python
$ sudo apt-get update  
$ sudo apt-get upgrade  
$ sudo apt-get install build-essential  
$ sudo apt-get install libncurses5-dev libncursesw5-dev libreadline6-dev libffi-dev  
$ sudo apt-get install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libsqlite3-dev libgdbm-dev tk8.5-dev libssl-dev openssl  
$ sudo apt-get install libboost-python-dev  
$ sudo apt-get install libpulse-dev  
$ sudo apt-get install python-dev  
$ sudo apt-get install vim  
$ cd ~  
$ mkdir python-source  
$ cd python-source/  
# check python current version at https://www.python.org/
$ wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz  
$ tar -xf Python-3.9.0.tar.xz  
$ cd Python-3.9.0/  
$ ./configure --prefix=/usr/local/opt/python-3.9.0  
$ make  
$ sudo make install  
# check installation, the response should be 3.9.0
$ /usr/local/opt/python-3.9.0/bin/python3.9 --version  
  
# Configure Virtual Environment in the project folder
$ cd ~  
$ sudo su  
$ cd /var  
$ mkdir www  
$ cd www/  
$ mkdir aselva  
$ cd aselva/  
$ /usr/local/opt/python-3.9.0/bin/python3.9 -m venv .  
$ . bin/activate  
  
# Install NGINX and Flask
$ apt-get update  
$ apt-get upgrade  
$ apt-get install nginx  
$ /var/www/aselva/bin/python3.9 -m pip install --upgrade pip  
$ pip install flask  
$ pip install flask-socketio  
$ vim hello.py  
# In hello.py, copy and save this text:
from flask import Flask  
app = Flask(__name__)  
@app.route("/")  
def hello():  
  return "Hello World!"  
  
if __name__ == "__main__":  
  app.run(host='0.0.0.0', port=8080)  
# save and quit typing :wq
$ python hello.py  
# Use the browser to confirm it is working:
http://192.168.43.118/:8080/  
  
# Install uWSGI
$ pip install uwsgi  
$ mkdir /var/log/uwsgi  
  
# Install Git
$ sudo apt-get install git-core  
$ git config --global user.email raulgroig@gmail.com  
$ git config --global user.name "Raul"  
  
# Sync git repo
$ git init .  
$ git remote add origin https://github.com/raulgroig/aselva  

# Enable ssh login with root user
$ cd ~
$ nano /etc/ssh/sshd_config
  PermitRootLogin yes
$ /etc/init.d/ssh restart
