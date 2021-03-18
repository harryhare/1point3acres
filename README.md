# 1point3acres

[一亩三分地](https://www.1point3acres.com/bbs/) 自动签到、答题 


## how to use

下面几种执行模式任选一种即可。


### github action 模式（推荐）

* fork 这个repo
* 增加一个 repo secret ： `USERS`, 格式如下，需代入你的用户名密码
    ```text
    [{'username':'replace_with_your_username','password':'replace_with_your_password'}]
    ```
* 测试：git action 页面手动执行， 查看log中是否有签到成功

### github action with docker

* 随便选（建）一个github repo
* 创建 一个 repo secret ： `USERS`, 格式如下，需代入你的用户名密码
    ```text
    [{'username':'replace_with_your_username','password':'replace_with_your_password'}]
    ```
* 创建 workflow
	```yaml
    name:  1point3acre get credits with docker
    on: 
      workflow_dispatch:
      schedule:
        - cron: '30 6 * * *'
    	
    jobs:
      _1point3acres:
        runs-on: ubuntu-latest
        name: get credits
        steps:
        - name: Hello world action step
          id: checkin
          uses: harryhare/1point3acres@main
          with:
            users: ${{ secrets.USERS }}
        - name: Get the log
          run: echo "${{ steps.checkin.outputs.log }}"
	```


### AWS-lambda 模式
* aws 创建 docker registry, 修改 makefile 的 image 地址
* 根据 aws 提示，docker login，然后 make build && make push
* aws 创建 lambda，选择第一步创建的 image，设置trigger


### crontab 模式
* 修改 configure/data/json，用你的用户名密码替换文件中的相应字段
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
    15 6 * * * python3 /replace_with_path_to_repo/service.py 2>&1 1>/dev/null
    ```

