import hashlib
import hmac
import base64
import requests
import time
import json
# unix timestamp 설정
timestamp = int(time.time() * 1000)
timestamp = str(timestamp)
# Ncloud API Key 설정

#입력 필요
ncloud_accesskey = ""
ncloud_secretkey = ""

ncloud_secretkey = bytes(ncloud_secretkey, 'UTF-8')
def make_signature():
    # 암호화 문자열 생성을 위한 기본값 설정
    apicall_method = "POST"
    space = " "
    new_line = "\n"
    # API 서버 정보
    #api_server = "https://cw.apigw.gov-ntruss.com"
    api_server = "https://cw.apigw.ntruss.com"
# API URL 서버 목록 조회
    #api_uri = "/cw_server/real/api/plugin/process/add"
    api_uri = "cw_fea/real/cw/api/planned-maintenances"
# hmac으로 암호화할 문자열 생성
    message = apicall_method + space + api_uri + new_line + timestamp + new_line + ncloud_accesskey
    message = bytes(message, 'UTF-8')
# hmac_sha256 암호화
    signingKey = base64.b64encode(hmac.new(ncloud_secretkey, message, digestmod=hashlib.sha256).digest())
    return signingKey
#위 코드까지는 Ncloud에서 제공해 주는 Signatuer Key 생성 부분과 동일
# 텍스트 파일에서 instanceNo 값을 읽어와 리스트에 저장
instanceNo_list = []
# 아래줄 텍스트 변경 필요
with open('D:\개발공부\Test-insight-DB.txt', 'r') as file:
    for line in file:
        instanceNo_list.append(line.strip())
# http 호출 헤더값 설정
http_header = {
    'Host': 'cw.apigw.ntruss.com',
    #'Host': 'cw.apigw.gov-ntruss.com',
    'Content-Type': 'application/json',
    'x-ncp-apigw-timestamp': timestamp,
    'x-ncp-iam-access-key': ncloud_accesskey,
    'x-ncp-apigw-signature-v2': make_signature(),
    'x-ncp-dmn_cd': 'PUB',
    #'x-ncp-dmn_cd': 'GOV',
    'x-ncp-region_code': "KR"
}
    # instanceNo 값을 하나씩 처리
    # Process
#for instanceNo_value in instanceNo_list:
# 요청 바디 (페이로드)
#    payload = {
#        "configList": [
#            "process_name001",
#            "*tomcat*"
#        ],
#        "instanceNo": instanceNo_value,
#        "type": "VPCServer"
#    }

for instanceNo_value in instanceNo_list:
# 요청 바디 (페이로드) - 
    payload = {
        "desc": "",
        "dimensions": {
                "460438474722512896": [
                 {
                    "instanceNo": instanceNo_value,
                    "mnt_nm": "/",
                    "type": "fs"
                 }
                ]
    }
    }

    # Process Add
    # url = "https://cw.apigw.gov-ntruss.com/cw_server/real/api/plugin/process/add"
    # File Add
    # url = "https://cw.apigw.gov-ntruss.com/cw_server/real/api/plugin/file/add"

    # File Add
    url = "https://cw.apigw.ntruss.com/cw_fea/real/cw/api/planned-maintenances"

    # File Add
    #url = "https://cw.apigw.ntruss.com/cw_server/real/api/plugin/file/add"

    # api 호출
    #GET 요청 보내기
    #response = requests.get(api_server + api_uri, headers=http_header)
    # POST 요청 보내기
    response = requests.post(url, headers=http_header, json=payload)
    # 응답 확인
    if response.status_code == 200:
        print(f"요청 성공 - instanceNo: {instanceNo_value}")
        #print(response.json())  # 응답 바디 출력
    else:
        print(f"요청 실패 - instanceNo: {instanceNo_value}, status_code: {response.status_code}, response_text: {response.text}")