# 1point3acres

一亩三分地自动签到 答题 https://www.1point3acres.com/bbs/


## how to

下面几种执行模式任选一种即可。


### github action 模式（推荐）

* fork 这个repo
* 增加一个 repo secret `USERS`, 格式如下，需代入你的用户名密码
```text
[{'username':'replace_with_your_username','password':'replace_with_your_password'}]
```

### github action with docker

* 随便选（建）一个github repo
* 创建 一个 repo secret USER
* 创建 workflow
```yaml
name: run docker
on: 
  schedule:
    - cron: '10 10 * * *'

jobs:
  1point3acres:
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


### 本机 crontab 模式
```bash
sudo /bin/bash prepare.sh
```

