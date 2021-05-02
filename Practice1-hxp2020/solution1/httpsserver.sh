#!/bin/sh
python3 tls.py server -k  ~/tls/privkey.pem -c ~/tls/fullchain.pem 0.0.0.0:11211
