.phony: push build bash run

build:
	docker build  -t 1point3acres -f docker/dockerfile .

bash:
	docker run --rm -it --entrypoint=bash 1point3acres

run:
	docker run --rm -it --entrypoint=python3 1point3acres _1point3acres.py

push:
	docker tag 1point3acres:latest 655445328103.dkr.ecr.us-east-1.amazonaws.com/1point3acres:latest
	docker push 655445328103.dkr.ecr.us-east-1.amazonaws.com/1point3acres:latest
