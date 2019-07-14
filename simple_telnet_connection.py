#  Simple Telnet Connection with Show Command

import telnetlib
import getpass

def opentelnetconn(host, user, password):
    try:
        tn = telnetlib.Telnet(host, 23, 2)
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



hosts = ['1.1.1.1', '2.2.2.2', '3.3.3.3', '4.4.4.4', '5.5.5.5', '6.6.6.6']
user = input('Enter your telnet username:')
password = getpass.getpass()

for host in hosts:
    print('~'*97)
    print('Connecting to {}'.format(host))
    tn,status,cause = opentelnetconn(host, user, password)
    if status:
        print('Connected to {}'.format(host))
        tn.write(b"show ip interface brief\n")
        print(tn.read_until(b'#', 5).decode('ascii'))
        # print(tn.read_all().decode('ascii'))
        tn.write(b'exit\n')
        print('Closing connection to {}'.format(host))
        tn.close()
    else:
        print(cause)