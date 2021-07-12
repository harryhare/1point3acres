import json
import http.cookies

def get_basic_cookie():
	f = open("../flaresolverr.json", "rb")  # gbk 编码要用 tb 打开
	data = json.load(f)
	f.close()
	cookies = data['solution']['cookies']
	cookie_lines=[]
	for c in cookies:
		k=c["name"]
		v=c["value"]
		cookie_lines.append(f'{k}={v}')
	raw_cookie_line = "; ".join(cookie_lines)
	simple_cookie = http.cookies.SimpleCookie(raw_cookie_line)
	return simple_cookie

if __name__ == "__main__":
	print(get_basic_cookie())