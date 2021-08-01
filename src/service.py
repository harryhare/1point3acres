import time
import json
import hashlib
from raw_requests import *
import sys
from twocaptcha import TwoCaptcha


# 签到流程
# 获得formhash:
# https://www.1point3acres.com/bbs/dsu_paulsign-sign.html
# 获得验证码：
# get https://www.1point3acres.com/bbs/misc.php?mod=seccode&action=update&idhash=S00&inajax=1&ajaxtarget=seccode_S00
# get https://www.1point3acres.com/bbs/misc.php?mod=seccode&update=38135&idhash=S00
# 检查验证码正确性:
# get https://www.1point3acres.com/bbs/misc.php?mod=seccode&action=check&inajax=1&&idhash=S00&secverify=et39
# 提交状态：
# post https://www.1point3acres.com/bbs/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=0&inajax=0

# 答题流程
# 获得题目和formhash：
# get https://www.1point3acres.com/bbs/plugin.php?id=ahome_dayquestion:pop&infloat=yes&handlekey=pop&inajax=1&ajaxtarget=fwin_content_pop
# 查答案
# 获得验证码：
# get https://www.1point3acres.com/bbs/misc.php?mod=seccode&action=update&idhash=SA00&inajax=1&ajaxtarget=seccode_SA00
# get https://www.1point3acres.com/bbs/misc.php?mod=seccode&update=38135&idhash=SA00
# 检查验证码正确性:
# get https://www.1point3acres.com/bbs/misc.php?mod=seccode&action=check&inajax=1&&idhash=SA00&secverify=et39
# 提交状态：
# post https://www.1point3acres.com/bbs/plugin.php?id=ahome_dayquestion:pop

solver = None

def get_verify_code(id_hash) -> str:
	verify_code = ""
	for i in range(20):
		print(f"try to get verify code {i + 1}th time...")
		time.sleep(2)
		code = get_verify_code_(id_hash)
		if len(code) != 4:
			print("verify code len error, retry")
			continue
		if check_verify_code_(id_hash, code):
			verify_code = code
			break
		print("verify code verify error, retry")
	return verify_code


def get_g_token(api_key, url) -> dict:
	global solver
	solver = TwoCaptcha(api_key)
	try:
		result = solver.recaptcha(sitekey='6LeCeskbAAAAAE-5ns6vBXkLrcly-kgyq6uAriBR', url=url)

	except Exception as e:
		print(e)
		exit(-1)
		return ""
	else:
		print('solved: ' + str(result))
		return result


# 如果 login 失败, 后面的操作没必要再做，直接 exit
def daily_login(username: str, password_hashed: str):
	print("do login...")
	form_hash, login_hash = get_login_info_()
	time.sleep(2)
	if form_hash == "" or login_hash == "":
		print("wrong login info")
		exit(-1)
	return login(username, password_hashed, form_hash, login_hash)


def daily_checkin(api_key: str) -> bool:
	print("do daily checkin...")
	form_hash, sec_hash = get_checkin_info_()
	time.sleep(2)
	if form_hash == "":
		return False
	code = get_g_token(api_key, get_checkin_url)
	if code == "":
		return False
	result = do_daily_checkin_(g_token=code["code"], form_hash=form_hash, sec_hash=sec_hash)
	solver.report(code["captchaId"], result)
	return result


def daily_question(api_key: str) -> bool:
	print("do daily question...")
	answer, form_hash, sec_hash, = get_daily_task_answer()
	time.sleep(2)
	if form_hash == "" or answer == "":
		return False
	code = get_g_token(api_key, get_checkin_url)
	if code == "":
		return False
	result = do_daily_question_(answer=answer, g_token=code["code"], form_hash=form_hash, sec_hash=sec_hash)
	solver.report(code["captchaId"], result)
	return result


def do_all(username: str, password: str, api_key: str):
	print(f"for user: {username[:3]}...{username[-2:]}")
	daily_login(username, password)
	daily_checkin(api_key)
	daily_question(api_key)
	return


def main(from_file: bool = False):
	users = []
	api_key = ""
	if from_file or len(sys.argv) == 1:
		fp = open("../configure/data.json")
		data = json.load(fp)
		users = data["users"]
		api_key = data["api_key"]
	else:
		api_key = sys.argv[1]
		users = json.loads(sys.argv[2].replace("'", '"'))
	for user in users:
		m = hashlib.md5()
		m.update(user["password"].encode("ascii"))
		do_all(user["username"], m.hexdigest(), api_key)


if __name__ == "__main__":
	main()
