#  Simple Telnet Connection with Show Command using input and output files (yaml)

import telnetlib
import getpass
import yaml

def opentelnetconn(host, user, password):
    try:
        tn = telnetlib.Telnet(host, 23, 5)
        tn.read_until(b"Username: ", 5)
        tn.write(user.encode('ascii') + b"\n")
        tn.read_until(b"Password: ", 5)
        tn.write(password.encode('ascii') + b"\n")
        test = tn.read_until(b'#', 5)
        test = str(test).find('#')
        if test != -1:
            tn.write(b"terminal length 0\n")
            tn.read_until(b'#', 5)
            status = True
            cause = ''
            return tn, status, cause
        else:
            status = False
            cause = 'Failed to Authenticate'
            tn.close()
            return tn, status, cause
    except Exception:
        tn = 0
        status = False
        cause = 'Failed to Connect'
        return tn, status, cause

with open(r'C:\Users\Tony Fermendzin\Desktop\Network Automation\Python\Python_Learning\aaa_Python Programming for Network Engineers (David Bombal)\hosts.yml') as f:
    hosts = yaml.load(f, Loader=yaml.FullLoader)

user = input('Enter your telnet username:')
password = getpass.getpass()

output = []
for host in hosts:
    print('~'*97)
    print('Connecting to {}'.format(host['hostname']))
    tn,status,cause = opentelnetconn(host['ip_address'], user, password)
    if status:
        print('Connected to {}'.format(host['ip_address']))
        tn.write(b'show run | i user\n')
        credentials = tn.read_until(b'#', 5)
        credentials = credentials.decode('utf-8').splitlines()
        for n in range (1, len(credentials)-1):
            credential = credentials[n].split(' ')
            outputn = {'hostname': host['hostname'], 'ip_address': host['ip_address'], 'username': credential[1], 'privalige level': credential[3], 'password': credential[6]}
            output.append(outputn)
        tn.write(b'exit\n')
        tn.close()
    else:
        print(cause)
        outputn = {'hostname': host['hostname'], 'ip_address': host['ip_address'], 'failure':cause}
        output.append(outputn)
with open(r'C:\Users\Tony Fermendzin\Desktop\Network Automation\Python\Python_Learning\aaa_Python Programming for Network Engineers (David Bombal)\output.yml', 'w') as outfile:
    yaml.dump(output, outfile, default_flow_style=False)