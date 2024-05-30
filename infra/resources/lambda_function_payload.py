import traceback, subprocess, os, json, requests

def lambda_handler(event, context):
    cmd = "echo Hello World"
    if "cmd" in event:
        cmd = event['cmd']

    try:
        result = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).stdout
        out = result.read()
        out = out.decode("utf8")
        
        request = requests.get('https://api.github.com/')
    

    except Exception as e:
        out = str(e)

    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": out,
        "urlRequestResponse": {"statusCode": request.status_code,}
    }
    return response