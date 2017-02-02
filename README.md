# hshltsbch
Installation: <br>

apt-get install python-setuptools python-pip virtualenv sqlite3<br>
virtualenv venv<br>
source venv/bin/activate<br>
pip install flask<br>

#developing <br>
pip install pyoo <br>

#deploying with uwsgi
apt-get install build-essential python-dev nginx
pip install uwsgi

#uwsgi.ini
[uwsgi]
socket = 127.0.0.1:3031
chdir = /home/money/hshltsbch/
processes = 1
threads = 1
stats = 127.0.0.1:9191
callable = app
wsgi-file = hshltsbch.py
uid = money
guid = money


#/etc/systemd/system/hshltsbch.service 
[Unit]
Description=Haushaltsbuch 
After=syslog.target

[Service]
ExecStart=/usr/local/bin/uwsgi --ini /home/money/hshltsbch/uwsgi.ini

RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target


systemctl daemon-reload
systemctl start hshltsbch

#cat /etc/nginx/sites-enabled/hshltsbch 
server 
{
    listen          80;
    server_name     localhost;
    charset         utf-8;

    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:3031;
    }
}

