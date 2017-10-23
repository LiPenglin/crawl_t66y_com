import hashlib
import time

m = hashlib.md5()

m.update(str(time.time()).encode())

md5value=m.hexdigest()

print(md5value)