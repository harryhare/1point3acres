# aws lambda entry
import service
import json
import os


def handler(event, context):
	print(os.system("id"))
	service.main(True)
	return {
		'statusCode': 200,
		'body': json.dumps('Hello from Lambda!')
	}
