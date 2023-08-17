import json
import random

import requests
import urllib.parse
import re
import questions
from sys import exit
import os
import http.cookies

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

referer = "https://www.1point3acres.com/"

get_login_url_v2 = "https://auth.1point3acres.com/"
login_url_v2 = "https://auth.1point3acres.com/login"
login_site_key_v2 = "6LewCc8ZAAAAAOu08V7c-IYrzICepKEQFFX401py"
default_site_key = "6LeCeskbAAAAAE-5ns6vBXkLrcly-kgyq6uAriBR"

get_login_url = "https://www.1point3acres.com/bbs/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login"
# login_url = "https://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
# login_url = "https://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
login_url = "https://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=%s&inajax=1"

cf_capcha_site_key = "0x4AAAAAAAA6iSaNNPWafmlz"

checkin_page = "https://www.1point3acres.com/next/daily-checkin"
post_checkin_url = "https://api.1point3acres.com/api/users/checkin"
# request body example:
# {
# 	"qdxq": "kx",
# 	"todaysay": "你好啊",
# 	"captcha_response": "0.378rshk_QlVixQwLiLJ_mTYYgNN5kk1n8KdgAMlWmqschH3Hry4NvVfmlq6xpVU7gNrmPRpK6dG_sH13E3yx5UKm9YUYnqe_8wqGEOgPU5ojo5B6GHJ08zuxLjch1GfduICYMWOZK_r69Cx5_W2NpfPYC7hekZtnx1UHf1hNjpglRfuAzg8hVBjGNJkKWZnwul7v5qPKUrJG8Vt4X_dqfNJSfBh120BWZxNogtRt3wC0yO-WonkBZFxTziaw9GNzUU0qKTXGd8TdFLGwzAW8M_C8yObCWxZke1YNu6xDIjJqr0MQF7Us-aPZhWt2NpJ_acPrz9TBFNCDd9m1XXlTzAHgnTp40syzr2dqJ-85EGYTCqFwi7fEP--iOxpBEdOibVyRPKFP5Lm1vrpKjlzrzagoqZeX_o4RPjkovzFLYO2tYd3EYG-ivzgZOmTztEyS.2mJfdz2J7SJyzhK79hp07w.2a799721779509dbb3cfc02860e74fa7b818edf2e61501a9b82652475523fbab",
# 	"hashkey": "",
# 	"version": 2
# }


question_page = "https://www.1point3acres.com/next/daily-question"
post_answer_url = "https://api.1point3acres.com/api/daily_questions"
# request body example:
# {
# 	"qid": 9,
# 	"answer": 4,
# 	"captcha_response": "0.sPVf24zxppaPTsCFVL0cY2H3JVV3bXsV16lrUg49rZk46219-yTqpMveg5-dK4o-PW-7pZZ7gvNiULTHdooVLlyF8BWzfCA57dp0QYTau1bwKryZQ9VYjdPv0QsoRUMDpVKlH2ujnvlZLBKZZ2mOMBld2K7eqkc69p2HC8v6eiuDHcNy8LMtKJq93zxwCxihgJLZeQuNHh3dZkyx-TaNI_MhDzWiIOo3HhfgjP0yiUE34Z8Ubm_SJIjURV4HuZ0uhGcTUkSeY7YKZp2Umk1vq_zJtNzX9JbR8tST2kyc-Pji_f0XaYrAV60haeECO2F2gQGP9hTsPYnZKFUMf6bzNlli0wsqzjAFHMFGc7cD6OYN-kxjH25J9NgZj1Bax49_fuDI-c6mxx_GUceJ7ULmiL1bxuuDxGYHLgU2_utRxLGwmC48ZdqHUkmhBZxl1i2m.SVpKadpQzkqDDJCxy7t5sw.65267473216ce644205fb205b9864820234ba07362209fdf07f3d57a887dd469",
# 	"hashkey": "",
# 	"version": 2
# }

session = requests.Session()


def save_error(response: requests.Response, error_desc: str = ""):
	print(f"{error_desc} 未知错误，查看tmp.html，了解详情")
	tmpfilename = "tmp.html"
	if os.name == "posix":
		tmpfilename = "/tmp/" + tmpfilename
	# content 是字节
	# text 是字符串
	# f = open("tmp.html", "w", encoding="utf-8")
	# f.write(response.text)
	f = open("tmp.html", "wb")
	f.write(response.content)
	f.close()


def check_status_code(response: requests.Response, error_desc: str = ""):
	if response.status_code != 200:
		print(f"{error_desc} error: status code is {response.status_code}")
		exit(-1)


def login_cookie(cookie: str) -> bool:
	global session
	session = requests.session()
	session.cookies.update(http.cookies.SimpleCookie(cookie))
	return True


def get_login_info_() -> (str, str):
	global session
	header = {
		"User-Agent": user_agent,
		"Referer": referer,
	}
	session = requests.session()
	response = session.get("https://www.1point3acres.com/bbs/", headers=header)
	if (response.status_code == 503):
		print("stop by cloudflare", response.status_code)
		exit(-1)
	if (response.status_code != 200):
		print("wrong status code: ", response.status_code)
		exit(-1)

	login_hash = ""
	form_hash = ""
	sec_hash = "SA0"
	response = session.get(get_login_url, headers=header)
	check_status_code(response, "get login info")
	pattern = re.compile("loginhash=([0-9a-zA-Z]+)")
	login_hashes = pattern.findall(response.text)
	if len(login_hashes) >= 1:
		login_hash = login_hashes[0]
	else:
		save_error(response, "login hash not found")
		exit(-1)
	pattern = re.compile('input type="hidden" name="formhash" value="([0-9a-zA-Z]+)"')
	form_hashes = pattern.findall(response.text)
	if len(form_hashes) >= 1:
		form_hash = form_hashes[0]
	else:
		save_error(response, "formhash not found")
		exit(-1)
	pattern = re.compile('input name="sechash" type="hidden" value="([0-9a-zA-Z]+)"')
	sec_hashes = pattern.findall(response.text)
	if len(sec_hashes) >= 1:
		sec_hash = sec_hashes[0]
	else:
		save_error(response, "sec hash not found")
		exit(-1)
	return form_hash, login_hash, sec_hash


def get_login_info_v2() -> str:
	global session
	# global proxy
	header = {
		"User-Agent": user_agent,
		"Referer": referer,
	}
	session = requests.session()
	response = session.get("https://www.1point3acres.com/bbs/", headers=header)

	if (response.status_code == 503):
		print("stop by cloudflare", response.status_code)
		exit(-1)
	if (response.status_code != 200):
		print("wrong status code: ", response.status_code)
		exit(-1)

	response = session.get(get_login_url_v2, headers=header)
	check_status_code(response, "get login info")
	pattern = re.compile('input id="csrf_token" name="csrf_token" type="hidden" value="([^"]+)"')
	csrf_tokens = pattern.findall(response.text)
	csrf_token = ""
	if len(csrf_tokens) >= 1:
		csrf_token = csrf_tokens[0]
	else:
		save_error(response, "csrf_token not found")
		exit(-1)
	return csrf_token


# sec_hash 默认 "SA0"
def login(username: str, password_hashed: str, form_hash: str, login_hash: str, sec_hash: str, solver) -> bool:
	print("try login...")
	header = {
		"User-Agent": user_agent,
		'Content-Type': 'application/x-www-form-urlencoded',
	}
	# body = {
	# 	"username": username,
	# 	"password": password_hashed,
	# 	"cookietime": "2592000",  # 30 days
	# 	"quickforward": "yes",
	# 	"handlekey": "ls",
	# }

	captcha = solver.recaptcha(
		sitekey=default_site_key,
		url=get_login_url,
	)

	body = {
		"formhash": form_hash,
		"referer": "https://www.1point3acres.com/bbs/",
		"username": username,
		"password": password_hashed,
		"questionid": 0,
		"answer": "",
		"sechash": sec_hash,
		"seccodehash": sec_hash,
		"seccodeverify": sec_hash,
		"g-recaptcha-response": captcha['code'],
		"cookietime": 2592000
	}
	url = login_url % login_hash
	response = session.post(url, headers=header, data=urllib.parse.urlencode(body))

	check_status_code(response, "log in")
	if "验证码填写错误" in response.text:
		print("验证码填写错误")
		solver.report(captcha["captchaId"], False)
		exit(-1)
	else:
		solver.report(captcha["captchaId"], True)
	if "登录失败" in response.text:
		print("用户名密码错误")
		exit(-1)
	if "您的账号存在被盗风险" in response.text:
		print("账号被强制微信登录")
		exit(-1)
	return True


def login_v2(username: str, password_hashed: str, csrf_token: str, solver) -> bool:
	print("try login...")
	header = {
		"User-Agent": user_agent,
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referer': 'https://auth.1point3acres.com/login',
		'Origin': 'https://auth.1point3acres.com',

	}
	captcha = solver.recaptcha(
		sitekey=login_site_key_v2,
		url="https://auth.1point3acres.com/",
	)
	body = {
		"redirect_url": "https://www.1point3acres.com/bbs/",
		"csrf_token": csrf_token,
		"username": username,
		"password": password_hashed,
		"question_id": 0,
		"answer": "",
		"g-recaptcha-response": captcha['code'],
		"submit": "\u767B\u5F55",
		# "submit": "登录",
		# "submit": "%E7%99%BB%E5%BD%95"
	}
	response = session.post(login_url_v2, headers=header, data=urllib.parse.urlencode(body))
	print(response.status_code)
	if response.status_code == 400:
		print("login error")
		save_error(response, "login_v2 err")
		exit(-1)
	if response.status_code != 302 and response.status_code != 200:
		print("login error")
		exit(-1)
	# todo：这句没试，不确定验证码错误的返回内容是什么
	if "验证码填写错误" in response.text:
		print("验证码填写错误")
		solver.report(captcha["captchaId"], False)
		exit(-1)
	else:
		solver.report(captcha["captchaId"], True)
	if "登录" not in response.text:
		print("登录成功")
	if "您的账号存在被盗风险" in response.text:
		print("账号被强制微信登录")
		exit(-1)
	if "用户名或密码错误" in response.text:
		print("用户名或密码错误")
		exit(-1)
	return True


def get_checkin_info_() -> (bool):
	header = {
		"User-Agent": user_agent,
	}
	response = session.get(checkin_page, headers=header)
	check_status_code(response, "get checkin info")
	if "今日已签到" in response.text:
		print("已签到")
		return False
	if "请登录后进行签到" in response.text:
		print("cookie无效 或者用户名密码错误")
		exit(-1)
		return True
	return True


def do_daily_checkin2_(solver) -> bool:
	header = {
		"User-Agent": user_agent,
		"Content-Type": "application/json",
		"Referer": referer
	}
	result = solver.turnstile(sitekey=cf_capcha_site_key, url=checkin_page, useragent=user_agent)
	#print(result)
	code = result["code"]
	id = result["captchaId"]

	emoji_list = ['kx', 'ng', 'ym', 'wl', 'nu', 'ch', 'fd', 'yl', 'shuai']
	body = {
		"qdxq": random.choice(emoji_list),
		"todaysay": "你好啊",
		"captcha_response": code,
		"hashkey": "",
		"version": 2
	}

	response = session.post(post_checkin_url, headers=header, data=json.dumps(body))
	#print(response.status_code)
	#print(response.text)
	check_status_code(response, "daily checkin")
	if "人机验证出错，请重试" in response.text:
		print("验证码错误")
		solver.report(id, False)
		return False
	else:
		solver.report(id, True)

	result = json.load(response.text)
	print(result["msg"])
	if (result["errno"] == 0):  # 成功
		return True
	elif (result["msg"] == "您今天已经签到过了"):
		return True
	else:
		print(result)
		return False


# 需要登录
def get_daily_task_answer() -> (int, int):
	# print("get question page")
	# header = {
	# 	"User-Agent": user_agent
	# }
	# response = session.get(question_page, headers=header)
	# check_status_code(response, "get daily question")
	# if "今日已答题" in response.text:
	# 	print("已答题")
	# 	return None

	print("get question...")
	header = {
		"User-Agent": user_agent,
		"Referer": referer,
	}
	response = session.get(post_answer_url, headers=header)
	check_status_code(response, "get daily question")
	resp_json = json.loads(response.text)
	if resp_json["errno"] != 0 or resp_json["msg"] != "OK":
		print(response.text)
		return None

	# {
	# 	"errno": 0,
	# 	"msg": "OK",
	# 	"question": {
	# 		"a1": "直接告诉对方自己目前薪酬，让对方看着良心办",
	# 		"a2": "拿地里抖包袱版的工资数字要对方match",
	# 		"a3": "开一个天价，谈不拢就散伙",
	# 		"a4": "精读工资谈判宝典：https://www.1point3acres.com/bbs/thread-286214-1-1.html 知己知彼，百战不殆",
	# 		"id": 9,
	# 		"qc": "谈判工资时，哪种做法有利于得到更大的包裹？"
	# 	}
	# }
	question_id = resp_json["question"]["id"]
	question = resp_json["question"]["qc"]
	question = question.strip()
	print(f"question: {question}")
	answers = {}
	answers[1] = resp_json["question"]["a1"]
	answers[2] = resp_json["question"]["a2"]
	answers[3] = resp_json["question"]["a3"]
	answers[4] = resp_json["question"]["a4"]
	print(f"answers: {answers}")
	answer = ""
	answer_id = 0
	if question in questions.questions.keys():
		answer = questions.questions[question]

		if type(answer) == list:
			for k in answers:
				if answers[k] in answer:
					print(f"find answer: {answers[k]} option value: {k} ")
					answer_id = k
		else:
			for k in answers:
				if answers[k] == answer:
					print(f"find answer: {answers[k]} option value: {k} ")
					answer_id = k
		if answer_id == "":
			print(f"answer not found: {answer}")
	else:
		print("question not found")
		return None
	return (question_id, answer_id)


def do_daily_question_(question: int, answer: int, solver) -> bool:
	header = {
		"User-Agent": user_agent,
		"Referer": referer,
		"Content-Type": "application/json",
	}

	result = solver.turnstile(sitekey=cf_capcha_site_key, url=question_page, useragent=user_agent)
	#print(result)
	code = result["code"]
	captcha_id = result["captchaId"]

	body = {
		"qid": question,
		"answer": answer,
		"captcha_response": code,
		"hashkey": "",
		"version": 2
	}

	response = session.post(post_answer_url, headers=header, data=json.dumps(body))
	#print(response.status_code)
	#print(response.text)

	check_status_code(response, "post answer")
	if "人机验证出错，请重试" in response.text:
		print("验证码错误")
		solver.report(captcha_id, False)
		return False
	else:
		solver.report(captcha_id, True)

	result = json.loads(response.text)
	print(result["msg"])
	if (result["errno"] == 0):  # 成功
		return True
	elif (result["msg"] == "您今天已经答过题了"):
		return True
	else:
		print(response.text)
		return False
