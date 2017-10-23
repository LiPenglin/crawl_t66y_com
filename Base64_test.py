import time
from urllib import parse

tm = time.time()

print(str(tm))

tm = str(tm)[0:10]

print(tm)

import base64

print(base64.b64encode(tm.encode()).decode())

b64 = base64.b64encode(tm.encode()).decode()

print(parse.quote(b64)) # encodeURIComponent

'''
MTUwMjQyODkwMw==
MTUwMjQyNTE1Mw==
'''