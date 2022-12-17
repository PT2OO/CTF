#!/usr/bin/python3
# exit()
import requests
import base64
import json
import os
from datetime import datetime
from termcolor import colored
import urllib3
import os
import subprocess
from pathlib import Path
import collections
import jsondiff
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# from Log.Log import Log

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) #added


def list_programs(data="", proxy=None):
	# try:
	username = "h1_ana1yst_f3rgustran" # H1 username

	api_token = "lQ42BqZjuewyHwTuXJvt18KnxXy1A6u16yV7L2lCq7I=" # H1 api token
	access_token = base64.b64encode((username+":"+api_token).encode()).decode()


	url = "https://api.hackerone.com"
	# retries = Retry(total=10, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])

	if proxy is None:
		HTTP_CONFIG = {}
	else:
		HTTP_CONFIG = {
		"http":"http://127.0.0.1:8080",
		"https":"http://127.0.0.1:8080"}

	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0",
		"Authorization": "Basic " + access_token,
		"Accept-Encoding": "gzip, deflate",
		"Connection": "close"
	}
	api = "/v1/hackers/programs/"
	flag = True
	while flag:
		try:
			flag = False
			r = requests.get(url+api+data, headers=headers, proxies=None, verify=False, timeout=60)
			print("--> {}".format(url+api+data))
		except:
			print(colored("[ERROR] - Request To H1 Failed, Trying Again...", "red"))
			flag = True
	return r

	
def monitorScopes():
	main_path = os.path.dirname(os.path.abspath(__file__))
	monitor_scopes = {}
	programs = []
	noti_data = []
	link = True

	print(colored("[INFO] - Scope Monitor Running...", "green"))
	r = None
	while(link):
		if link==True:
			while r == None:
				r = list_programs(data="")
		else:
			while r == None:
				r = list_programs(data=link)
		try:
			json_response = json.loads(r.text)
			list_program = json_response["data"]
			if "next" in json_response["links"].keys():
				link = json_response["links"]["next"].split("programs")[1]
			else:
				link = False
			for data in list_program:
				programs.append(data["attributes"]["handle"])
		except:
			continue
		r = None

	monitor_scopes = filter_programs(programs, state=None, asset_type=None, eligible_for_bounty=False)

	
	pathFile = "{}/latest_scopes.json".format(main_path)
	with open(pathFile, "w") as outfile:
		json_object = json.dumps(monitor_scopes, indent = 4)
		outfile.write(json_object)
	outfile.close()
	print(colored("[DONE] - Scopes Monitoring Process", "green"))


def filter_programs(programs, state=None, asset_type=None, eligible_for_bounty=False):
	monitor_scopes = {}
	list_asset_type = ["URL", "OTHER", "CIDR", "GOOGLE_PLAY_APP_ID", "APPLE_STORE_APP_ID", "HARDWARE", "OTHER_APK", "DOWNLOADABLE_EXECUTABLES", "SOURCE_CODE"]
	list_states = ["soft_launched", "public_mode"]

	#Filter program state
	choosen_programs = []
	for program in programs:
		r_json = None
		while r_json is None:
			try:
				r = list_programs(data=program)
				r_json = r.json()
			except:
				r_json = None
				continue
		if state is None:
			if r_json["attributes"]["submission_state"] == "open": 
				choosen_programs.append(r_json)
		else:
			if state not in list_states:
				print("[E] Invalid program state!")
				exit()
			else:
				if r_json["attributes"]["state"] == state and r_json["attributes"]["submission_state"] == "open":
					choosen_programs.append(r_json)

	if len(choosen_programs) < 1:
		print("")
	else:
		for program in choosen_programs:
			choosen_scopes = []
			list_scopes = program["relationships"]["structured_scopes"]["data"]
			if len(list_scopes) > 1:
				for scope in list_scopes:
					if asset_type is None:
						if scope["attributes"]["eligible_for_bounty"] == eligible_for_bounty and scope["attributes"]["max_severity"] != "none":
							choosen_scopes.append(scope)
					else:
						if scope["attributes"]["eligible_for_bounty"] == eligible_for_bounty and scope["attributes"]["asset_type"] == asset_type and scope["attributes"]["max_severity"] != "none":
							choosen_scopes.append(scope)
			if len(choosen_scopes) > 0:
				program_name = program["attributes"]["handle"]
				monitor_scopes[program_name] = {"state" : program["attributes"]["state"]}
				monitor_scopes[program_name]["scopes"] = []
				for choosen in choosen_scopes:
					monitor_scopes[program_name]["scopes"].append({
										choosen["attributes"]["asset_identifier"]: 
										{
											"asset_type": choosen["attributes"]["asset_type"],
											"updated_at": choosen["attributes"]["updated_at"],
											"eligible_for_bounty": choosen["attributes"]["eligible_for_bounty"]
										}
									}
								)
	return monitor_scopes


def export_url_scopes():
	url_scopes_full = []
	url_scopes_short = []	

	main_path = os.path.dirname(os.path.abspath(__file__))
	pathFile = "{}/latest_scopes.json".format(main_path)
	with open(pathFile, "r") as outfile:
		list_programs = json.load(outfile)
	for program in list_programs:
		# print(list_programs[program])
		for scope in list_programs[program]["scopes"]:
			for item in scope:
				if scope[item]["asset_type"] == "URL":
					full = "[{}] - {} - {} - Bounty: {}".format(program, scope[item], scope[item]["asset_type"], scope[item]["eligible_for_bounty"])
					short = item
					url_scopes_full.append(full)
					url_scopes_short.append(short)

	# print(url_scopes_full)
	with open('{}/url_scopes_full.txt'.format(main_path), 'w') as f1:
			for url in url_scopes_full:
				f1.writelines(url + "\n")

	with open('{}/url_scopes_short.txt'.format(main_path), 'w') as f2:
			for url in url_scopes_short:
				f2.writelines(url + "\n")

    	




monitorScopes()
	
export_url_scopes()	