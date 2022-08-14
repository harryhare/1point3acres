import random

import requests
import urllib.parse
import re
import xml.dom.minidom as xml
import lxml.html as html
import questions
from sys import exit
import os
import http.cookies

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
accept = "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
accept_language = "en-US,en;q=0.5"
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

referer = "https://www.1point3acres.com/bbs/"

get_login_url_v2 = "https://auth.1point3acres.com/"
login_url_v2 = "https://auth.1point3acres.com/login"
login_site_key_v2 = "6LewCc8ZAAAAAOu08V7c-IYrzICepKEQFFX401py"
default_site_key = "6LeCeskbAAAAAE-5ns6vBXkLrcly-kgyq6uAriBR"

get_login_url = "https://www.1point3acres.com/bbs/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login"
# login_url = "https://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
# login_url = "https://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
login_url = "https://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=%s&inajax=1"

get_verify_code_url = "https://www.1point3acres.com/bbs/misc.php?mod=seccode&action=update&idhash=%s&inajax=1&ajaxtarget=seccode_%s"
check_verify_code_url = "https://www.1point3acres.com/bbs/misc.php?mod=seccode&action=check&inajax=1&&idhash=%s&secverify=%s"

get_checkin_url = "https://www.1point3acres.com/bbs/dsu_paulsign-sign.html"
post_checkin_url = "https://www.1point3acres.com/bbs/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=0&inajax=0"

get_question_url = "https://www.1point3acres.com/bbs/plugin.php?id=ahome_dayquestion:pop&infloat=yes&handlekey=pop&inajax=1&ajaxtarget=fwin_content_pop"
post_answer_url = "https://www.1point3acres.com/bbs/plugin.php?id=ahome_dayquestion:pop"

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


def login_settings(login_settings: str) -> bool:
    global session, user_agent, accept, accept_language
    session = requests.session()
    session.cookies.update(http.cookies.SimpleCookie(login_settings["cookie"]))
    for e in ["user_agent", "accept", "accept_language"]:
        if e in login_settings and login_settings[e] != f"replace_with_your_{e}":
            globals()[e] = login_settings[e]
    return True


def get_login_info_() -> (str, str):
    global session
    header = {
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept_Language": accept_language,
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
        "Accept": accept,
        "Accept_Language": accept_language,
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
        "Accept": accept,
        "Accept_Language": accept_language,
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
        "Accept": accept,
        "Accept_Language": accept_language,
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


def get_checkin_info_() -> (str, str):
    form_hash = ""
    sec_hash = ""
    header = {
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept_Language": accept_language,
        "Referer": referer
    }
    response = session.get(get_checkin_url, headers=header)
    check_status_code(response, "get checkin info")
    if "您今天已经签到过了或者签到时间还未开始" in response.text:
        print("已签到")
        return "", ""
    if "您需要先登录才能继续本操作" in response.text:
        print("cookie无效 或者用户名密码错误")
        exit(-1)
    pattern = re.compile("formhash=([0-9a-z]+)")
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
        sec_hash = "S00"
    return form_hash, sec_hash


def do_daily_checkin_(solver, form_hash: str, sec_hash: str = "S00") -> bool:
    header = {
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept_Language": accept_language,
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.1point3acres.com/bbs/dsu_paulsign-sign.html"
    }
    captcha = solver.recaptcha(
        sitekey="6LeCeskbAAAAAE-5ns6vBXkLrcly-kgyq6uAriBR",
        url=get_checkin_url,
    )

    emoji_list = ['kx', 'ng', 'ym', 'wl', 'nu', 'ch', 'fd', 'yl', 'shuai']
    body = {
        "formhash": form_hash,
        "qdxq": random.choice(emoji_list),
        "qdmod": 2,
        "todaysay": None,
        "fastreply": 14,
        "sechash": sec_hash,
        "seccodehash": sec_hash,
        "seccodeverify": sec_hash,
        "g-recaptcha-response": captcha['code'],
    }

    response = session.post(post_checkin_url, headers=header, data=body)
    check_status_code(response, "daily checkin")
    if "验证码填写错误" in response.text:
        print("验证码错误")
        solver.report(captcha["captchaId"], False)
        return False
    else:
        solver.report(captcha["captchaId"], True)

    if "您需要先登录才能继续本操作" in response.text:  # cookie 出错
        print("login error，cookie missing")
        return False
    elif "您今日已经签到，请明天再来" in response.text:
        print("已签到")
        return True
    elif "做微信验证（网站右上角）后参与每日答题" in response.text:
        print("没绑微信")
        return True
    elif "恭喜你签到成功!获得随机奖励" in response.text:
        print("签到成功")
        return True
    else:
        save_error(response, "check in")
        return False


# 需要登录
def get_daily_task_answer() -> (str, str, str):
    print("get question...")
    header = {
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept_Language": accept_language,
        "Referer": referer
    }
    response = session.get(get_question_url, headers=header)
    check_status_code(response, "get daily question")
    if "您今天已经参加过答题，明天再来吧！" in response.text:
        print("已答题")
        return "", "", ""
    dom = xml.parseString(response.text)
    data = dom.childNodes[0].childNodes[0].data
    nodes = html.fragments_fromstring(data)
    form_hash_node = nodes[1].cssselect('form input[name="formhash"]')[0]
    form_hash = form_hash_node.get("value")
    sec_hash_node = nodes[1].cssselect("form input[name='sechash']")[0]
    sec_hash = sec_hash_node.get("value")
    print(f"form hash: {form_hash}")
    question_node = nodes[1].cssselect("form div span font")[0]
    question = question_node.text_content()
    question = question[5:]  # 去掉开始的 "【问题】 "
    question = question.strip()  # 去掉结尾空格
    print(f"question: {question}")
    answer_nodes = nodes[1].cssselect("form div.qs_option input")
    answers = {}
    for node in answer_nodes:
        id = node.get("value")
        text = node.getparent().text_content()
        answers[id] = text[2:].strip()  # 去掉前后的空格 fix https://github.com/harryhare/1point3acres/issues/3
    print(f"answers: {answers}")
    answer = ""
    answer_id = ""
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
    return answer_id, form_hash, sec_hash


def do_daily_question_(answer: str, solver, form_hash: str, sec_hash: str = "SA00") -> bool:
    header = {
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept_Language": accept_language,
        "Referer": referer,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    captcha = solver.recaptcha(
        sitekey=default_site_key,
        url=get_checkin_url,
    )

    body = {
        "formhash": form_hash,
        "answer": answer,
        "sechash": sec_hash,
        "seccodehash": sec_hash,
        "seccodeverify": sec_hash,
        "g-recaptcha-response": captcha['code'],
        "submit": "true"
    }
    # 网站的原版请求是 multipart/form-data ，但是我发现用 application/x-www-form-urlencoded 也是可以的
    # response = scraper.post(post_answer_url, files=body, headers=header, cookies=cookie_jar)
    # response = requests.post(post_answer_url, data=body, headers=header, cookies=cookie_jar)
    response = session.post(post_answer_url, data=body, headers=header)
    check_status_code(response, "post answer")

    if "抱歉，验证码填写错误" in response.text:
        print("验证码错误")
        solver.report(captcha["captchaId"], False)
        return False
    else:
        solver.report(captcha["captchaId"], True)

    if "抱歉，您的请求来路不正确或表单验证串不符，无法提交" in response.text:
        print("抱歉，您的请求来路不正确或表单验证串不符，无法提交")
        return False
    elif "登录后方可进入应用" in response.text:
        print("cookie 错误")
        return False
    elif "恭喜你，回答正确" in response.text:
        print("答题成功")
        return True
    elif "抱歉，回答错误！扣除1大米" in response.text:
        print("答案错了，请报 issue: https://github.com/harryhare/1point3acres/issues/new")
        return True
    else:
        save_error(response, "post answer")
        return False
