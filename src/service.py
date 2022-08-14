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


# def get_g_token(api_key: str, url: str, site_key: str = '6LeCeskbAAAAAE-5ns6vBXkLrcly-kgyq6uAriBR') -> dict:
#     solver = TwoCaptcha(api_key)
#     try:
#         result = solver.recaptcha(
#             sitekey=site_key,
#             url=url
#         )
#
#     except Exception as e:
#         print(e)
#         exit(-1)
#     else:
#         print('solved: ' + str(result))
#         return result


def daily_login_settings(settings: dict):
    return login_settings(settings)


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


def daily_checkin(solver) -> bool:
    print("do daily checkin...")
    form_hash, sec_hash = get_checkin_info_()
    time.sleep(2)
    if form_hash == "":
        return False
    # token = get_g_token(api_key, get_checkin_url, other_site_key)
    # if token == "":
    #     return False
    return do_daily_checkin_(solver, form_hash=form_hash, sec_hash=sec_hash)


def daily_question(solver) -> bool:
    print("do daily question...")
    answer, form_hash, sec_hash, = get_daily_task_answer()
    time.sleep(2)
    if form_hash == "" or answer == "":
        return False
    # token = get_g_token(api_key, get_checkin_url)
    # if token == "":
    #     return False
    return do_daily_question_(answer=answer, solver=solver, form_hash=form_hash, sec_hash=sec_hash)


def do_all_settings(solver, settings: dict):
    daily_login_settings(settings)
    daily_checkin(solver)
    daily_question(solver)
    return


def do_all_password(solver, username: str, password: str):
    print(f"for user: {username[:3]}...{username[-2:]}")
    daily_login_v2(solver, username, password)
    daily_checkin(solver)
    daily_question(solver)
    return


def main(from_file: bool = False):
    users = []
    api_key = ""
    settings_file = "../configure/settings.json"
    password_file = "../configure/data.json"
    if (len(sys.argv) > 1):
        settings_file = sys.argv[1]
    if os.path.exists(settings_file):
        fp = open(settings_file)
        data = json.load(fp)
        users = data["users"]
        api_key = data["api_key"]
        solver = TwoCaptcha(api_key)
        if api_key != "replace_with_your_api_key":
            for user in users:
                do_all_settings(solver, user)
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
