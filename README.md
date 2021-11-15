# 샘플 프로젝트 정보
이미 설치된 프로그램들
* conda version : 4.10.3
* Python 3.7.10 | packaged by conda-forge | (default, Feb 19 2021, 16:07:37)
* Flask 2.0.1
* Flask-Bootstrap 3.3.7.1
* Jinja2 3.0.1
* gunicorn 20.1.0
* mysql-connector-python 8.0.22

## PyCharm 에서 Flask 프로젝트 생성
### 개발서버 디렉토리 생성
* sample-test env 사용
```bash
$ mkdir /home/yelloweb/anaconda3/envs/sample-test/project/flask_sample_test
```

### PyCharm에서 생성한 디릭토리와 연동하여 Flask 프로젝트 생성
* PyCharm 과 연동하는 부분의 설명은 생략
* Run/Debug Configuration에서 Flask Server 로 실행하는 경우 Additional options에 아래의 내용을 추가
```text
--host=0.0.0.0 --port=5000
```

### PyCharm에서 생성된 프로젝트에서 Flask 개발모드 실행
* 실행결과
```bash
... 생략 ...

 * Serving Flask app 'app.py' (lazy loading)
 * Environment: development
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://10.0.2.15:5000/ (Press CTRL+C to quit)
```

## 개발모드에서 사용되는 5000 포트 개발서버 방화벽 설정
```bash
$ sudo firewall-cmd --permanent --add-port=5000/tcp
$ sudo firewall-cmd --reload
$ sudo systemctl restart firewalld
```

## logrotate 설정
* LOG BASE : /home/yelloweb/logs/flask_sample_test
```bash
$ sudo vi /etc/logrotate.d/flask_sample_test
```

* 내용
```bash
/home/yelloweb/logs/flask_sample_test/*.log {
    copytruncate
    daily
    rotate 15
    maxage 7
    missingok
    notifempty
    compress
    dateext
    dateformat -%Y%m%d_%s
    postrotate
        /bin/chown yelloweb:yello /home/yelloweb/logs/flask_sample_test/*.log*
    endscript
    su root yello
}
```

## 추가 모듈 설치
### MySQL Connector 설치
* 필요한 경우 설치
```bash
# MySQL Client 설치
$ sudo yum install mysql -y
```
