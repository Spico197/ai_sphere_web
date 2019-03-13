
## Methods to build
### Collectstatic
```bash
python manage.py collectstatic # 需要设置STATIC_ROOT，为admin后台的静态文件提供支持
python manage.py makemigrations user
python manage.py migrate user
python manage.py makemigrations
python manage.py migrate
```
### Nginx settings
save nginx file to `/etc/nginx/sites-enabled` or create a link file.
```nginx
server {
	listen 2678;
	server_name ai_sphere;
	charset utf-8;
	client_max_body_size 75M;
	location /static {
		alias /home/spico/ai_sphere/server_edition/static;
	}
	location /upload {
		alias /home/spico/ai_sphere/server_edition/upload;
	}
	location /media {
		alias /home/spico/ai_sphere/server_edition/media;
	}
	location / {
		uwsgi_pass 127.0.0.1:8899;
		include /etc/nginx/uwsgi_params;
	}
}
```

### Uwsgi settings
save to `uwsgi.ini` file
```ini
[uwsgi]
chdir = /home/spico/ai_sphere/server_edition    # website dir
home = /home/spico/.local/share/virtualenvs/ai_sphere-e14AwAak/ # virtualenv home
module = ai_sphere.wsgi:application # uwsgi application

master = True
processes = 4
harakiri = 60
max-requests = 5000

socket = 127.0.0.1:8899
#socket = 0.0.0.0:6666
pidfile = /home/spico/ai_sphere/server_edition/ai_sphere.pid
vacuum = True
```

### Settings check & Service start
```bash
nginx -t # check nginx setting files
sudo service nginx restart
uwsgi --ini uwsgi.ini
```

## Apps

- user: main user app

## Presentation

[AI圈码赛客](http://39.108.7.66:2678/user/panel/)