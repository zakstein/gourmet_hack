#!/bin/bash

#unzip
/bin/echo $PATH > test.tmp
tar xvzf nginx-1.0.5.tar.gz && cd nginx-1.0.5;

#config
./configure --prefix=/usr \
    --sbin-path=/usr/sbin/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --pid-path=/var/run/nginx/nginx.pid  \
    --lock-path=/var/lock/nginx.lock \
    --user=nginx \
    --group=nginx \
    --with-http_ssl_module \
    --with-http_flv_module \
    --with-http_gzip_static_module \
    --http-log-path=/var/log/nginx/access.log \
    --http-client-body-temp-path=/var/tmp/nginx/client/ \
    --http-proxy-temp-path=/var/tmp/nginx/proxy/ \
    --http-fastcgi-temp-path=/var/tmp/nginx/fcgi/ 

#make
make && make install

#clean up
cd ..
rm -r nginx-1.0.5
