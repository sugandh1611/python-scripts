from sys import argv
import subprocess
import json
import ast

key_values = []

def removeNesting(l):
    for i in l:
        if type(i) == list:
            removeNesting(i)
        else:
            key_values.append(i)

script, service_env = argv
service_env_string = ""
service_env_string = service_env_string.join(service_env)

key_values_json = subprocess.check_output('aws ssm get-parameters --names '+service_env_string+' --query "Parameters[*].Value" --with-decryption --region ap-south-1', shell=True, stderr=subprocess.STDOUT)
key_values_string = (key_values_json.decode())
key_values_list = ast.literal_eval(key_values_string)
removeNesting(key_values_list)

for key_value in key_values:
    parameters = key_value
    print(parameters)
