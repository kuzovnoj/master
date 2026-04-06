#!/bin/sh
while true; do
  certbot renew --webroot --webroot-path=/var/www/certbot --non-interactive --quiet
  sleep 43200  # 12 часов
done