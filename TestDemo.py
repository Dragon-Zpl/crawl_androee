import hashlib



while True:
    a = input("path:")
    print(hashlib.md5((a).encode('utf-8')).hexdigest())