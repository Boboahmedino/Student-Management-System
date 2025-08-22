"""I used this to test the 2 gmail ports i used, trust me it was very funny"""

import socket, ssl, sys

HOST = "smtp.gmail.com"
for port in (587, 465):
    try:
        print(f"[*] Testing tcp connect to {HOST}:{port} ...")
        s = socket.create_connection((HOST, port), timeout=40)
        s.close()
        print(f"[OK] TCP connect to {HOST}:{port} succeeded")
    except Exception as e:
        print(f"[FAIL] TCP connect to {HOST}:{port} failed: {e}")
