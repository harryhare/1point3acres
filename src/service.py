import time
import json
import hashlib
from raw_requests import *
import sys
from twocaptcha import TwoCaptcha


# 签到流程
# 查看是否已签到
# https://www.1point3acres.com/next/daily-checkin
# 执行签到（post）
# https://api.1point3acres.com/api/users/checkin

# 答题流程
# 获得题目（get）
# https://api.1point3acres.com/api/daily_questions
# 提交答案（post）
# https://api.1point3acres.com/api/daily_questions


def daily_login_cookie(cookie: str):
	return login_cookie(cookie)


def daily_login_v2(solver, username: str, password: str):
	print("do login...")
	csrf_token = get_login_info_v2()
	if csrf_token == "":
		print("wrong csrf_token")
		exit(-1)
	time.sleep(2)
	# token = get_g_token(api_key, "https://auth.1point3acres.com/", login_site_key_v2)
	# if token == "":
	#     return False
	# print(csrf_token)
	# print(token)
	return login_v2(username, password, csrf_token, solver)


# 如果 login 失败, 后面的操作没必要再做，直接 exit
def daily_login(solver, username: str, password_hashed: str):
	print("do login...")
	form_hash, login_hash, sec_hash = get_login_info_()
	time.sleep(2)
	if form_hash == "" or login_hash == "" or sec_hash == "":
		print("wrong login info")
		exit(-1)
	url = login_url % login_hash
	# token = get_g_token(api_key, "https://www.1point3acres.com/bbs/")
	# code = get_g_token(api_key, get_login_url)
	# code = get_g_token(api_key, url)
	# if token == "":
	#     return False
	return login(username, password_hashed, form_hash, login_hash, sec_hash, solver)


def daily_question(solver) -> bool:
	print("do daily question...")
	r = get_daily_task_answer()
	if r == None:
		return False
	time.sleep(2)
	return do_daily_question_(question=r[0], answer=r[1], solver=solver)


def do_all_cookie(solver, cookie: str):
	daily_login_cookie(cookie)
	if get_checkin_info_() == True:
		do_daily_checkin2_(solver)
	daily_question(solver)
	return


def do_all_password(solver, username: str, password: str):
	print(f"for user: {username[:3]}...{username[-2:]}")
	daily_login_v2(solver, username, password)
	# daily_question(solver)
	return


def main(from_file: bool = False):
	users = []
	api_key = ""
	cookie_file = "../configure/cookie.json"
	password_file = "../configure/data.json"
	if (len(sys.argv) > 1):
		cookie_file = sys.argv[1]
	if os.path.exists(cookie_file):
		fp = open(cookie_file)
		data = json.load(fp)
		users = data["users"]
		api_key = data["api_key"]
		solver = TwoCaptcha(api_key)
		if api_key != "replace_with_your_api_key":
			for user in users:
				do_all_cookie(solver, user["cookie"])
			return

	fp = open(password_file)
	data = json.load(fp)
	users = data["users"]
	api_key = data["api_key"]
	solver = TwoCaptcha(api_key)
	for user in users:
		do_all_password(solver, user["username"], user["password"])
		time.sleep(5)


if __name__ == "__main__":
	main()
