import hashlib

if __name__=="__main__":
	m=hashlib.md5()
	m.update(b"xxxxxx")
	print(m.hexdigest())