#!/usr/bin/python
from passlib.hash import sha512_crypt
hash = sha512_crypt.encrypt("Leanwork109A")
print hash
