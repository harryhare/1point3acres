import json
import http.cookies

def get_basic_cookie():
	# gbk 编码要用 tb 打开
	# https://stackoverflow.com/questions/28165639/unicodedecodeerror-gbk-codec-cant-decode-byte-0x80-in-position-0-illegal-mult
	f = open("../flaresolverr.json", "rb")
	data = json.load(f)
	f.close()
	cookies = data['solution']['cookies']
	cookie_lines=[]
	for c in cookies:
		k=c["name"]
		v=c["value"]
		cookie_lines.append(f'{k}={v}')
	raw_cookie_line = "; ".join(cookie_lines)
	#raw_cookie_line="cf_clearance=60850fb6ffd4f2d1e0f81d54dbe93024eefca053-1626071331-0-150"
	simple_cookie = http.cookies.SimpleCookie(raw_cookie_line)
	print(simple_cookie)
	return simple_cookie

if __name__ == "__main__":
	print(get_basic_cookie())