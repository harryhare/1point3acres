![每日签到答题](https://github.com/harryhare/1point3acres/actions/workflows/get_credit_ubuntu_flaresolverr.yml/badge.svg)


## Notice

**为登录增加验证码**

由于 昨天(2021.08.25) 网站为登录页面（弹窗）增加了验证码，所以代码也需要做相应的修改。

修改后，每天每用户需要调用 **3次** 验证码 API(登录一次，签到一次，答题一次)，

2captcha.com 充值 **3刀** 的可用天数缩减到 **300天**

2021.08.26

<br>

**更新验证模块**

使用 [网站 2captcha.com](https://2captcha.com?from=12332166) 提供的api。

但是该API 收费，一亩三分地的验证码是 [reCAPTCHA v2 hard](https://2captcha.com/demo) ，对应的[收费](https://2captcha.com/2captcha-api)是 $2.99 / 1000 次请求

如果想使用需要注册账号+充值只少3刀（单个账号可以用 500 天左右）+ 复制 apikey 替换 configure/data.json 文件中的字段

2021.08.01

<br>

**程序失效**

论坛增加了google Google reCAPTCHA 验证码，导致程序失效

部分账号被封号

2021.07.30

<br>

**Github Action 模式下** `get credit with flaresolverr` **这个workflow 有一定概率成功**

目前我试了三次只有一次是成功的。如果想尝试可以拉下最新代码

2021.07.13

<br>

**尝试了很多方法都行不通，宣布失败**

但由于 cloudflare 是根据 IP 来阻挡的，所以这个程序依然可以在本地运行 

2021.07.13

<br>

**目前遇到 被 cloudflare 阻挡的问题，还在修复中，修复后会更新**

2021.07.11

---

# 1point3acres

[一亩三分地](https://www.1point3acres.com/bbs/) 自动签到、答题

快速设置，无 aws 依赖，验证码自动识别，一次性设置后再无需手动操作

* 程序会自动识别验证码

* 程序会在指定的时间每天运行一次，一次配置，永远执行，设好后就再不用管

* 配置简单，~~使用 github action 模式，不依赖 github 以外的东西，只要 fork 本repo后设置 repo secret 即可~~

* 支持多用户签到，批量用户签到，把用户名密码加到`USERS`数组中即可

## how to use

下面几种执行模式任选一种即可。

### 本地 crontab 模式

* 注册[2captcha.com](https://2captcha.com?from=12332166) 得到 apikey 并充值(可以用支付宝)
    <details>
    <summary>具体操作展开查看</summary>
    
    ![](screenshots/2captcha.png)
    </details>
* 修改 configure/data.json，用你的用户名,密码,apikey替换文件中的相应字段

* 安装依赖
以 ubuntu 为例，其他系统请用相应的方式安装依赖
    ```bash
    sudo /bin/bash prepare.sh
    ```
    
* crontab
    ```
    crontab -e
    ```
    ```text
    15 8 * * * cd /replace_with_path_to_repo/src && python3 service.py 2>&1 1>/tmp/1point3acres.log
    ```


### ~~github action 模式（现已失效）~~

* fork 这个repo

* 增加一个 repo secret: `USERS`, 格式如下，需代入你的用户名密码，
    ```text
    [{'username':'replace_with_your_username','password':'replace_with_your_password'}]
    ```
    用户名一般是邮箱，就是你登录的时候填的那个东东
    <details>
    <summary>具体操作展开查看</summary>
    
    ![](screenshots/repo_secret_1.png)
    ---
    ![](screenshots/repo_secret_2.png)
    </details>
* enable github action
    <details>
    <summary>具体操作展开查看</summary>
    
    ![](screenshots/repo_action_1.png)
    ---
    ![](screenshots/repo_action_2.png)
    </details>

* 做完上面的步骤，就完成了所有操作，github 会在每天的 北京时间9:00.am（UTC 1:00am.） 左右自动执行签到和答题程序。

  如果你想验证下用户名密码是否设置正确，可以到 git action 页面手动执行， 查看log中是否有"签到成功"
  
  如果已经答题或者已经签到，会显示"已答题" 或者 "已签到"，同样表示设置已成功。
  
  github 每天自动执行的log 也可以在这里看到。
  
    <details>
    <summary>具体操作展开查看</summary>
  
    ![](screenshots/repo_action_3.png)
    ---
    ![](screenshots/repo_action_4.png)
    </details>

* 好用请给个星
  ![](screenshots/star.png)

### ~~github action with docker 模式（已失效）~~

* 随便选（建）一个github repo

* 创建 一个 repo secret ： `USERS`, 格式如下，需代入你的用户名密码

    ```text
    [{'username':'replace_with_your_username','password':'replace_with_your_password'}]
    ```
    
* 创建 workflow

	```yaml
    name: 1point3acre get credits with docker
    on:
      workflow_dispatch:
      schedule:
        - cron: '30 0 * * *'
    jobs:
      _1point3acres:
        runs-on: ubuntu-latest
        name: get credits
        steps:
        - name: run docker
          id: checkin
          uses: harryhare/1point3acres@main
          with:
            users: ${{ secrets.USERS }}
        - name: get the result
          run: echo "${{ steps.checkin.outputs.result }}"
	```


### ~~AWS-lambda 模式 （已失效）~~

* 修改 configure/data.json，用你的用户名密码替换文件中的相应字段
* aws 创建 docker registry, 修改 makefile 的 image 地址
* 根据 aws 提示，docker login，然后 make build && make push
* aws 创建 lambda，选择第一步创建的 image，设置trigger



## 其他

* 题目数据来自： https://github.com/eagleoflqj/p1a3_script