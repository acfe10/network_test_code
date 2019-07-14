#####################################################################
# Simple Telnet Connection with Show Command
# Uses input and output files (csv)
#####################################################################


import telnetlib
import getpass

#####################################################################
# Establish telnet connection to 'host'
# Prompts for Username = 'user' & Password = 'password'
# Returns telnet connection = 'tn',
#   connection status = 'status' & failure cause = 'cause'
#####################################################################

def openTelnetConn(host, user, password):
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

def importHostFile(hostFileName):
    with open(hostFileName, 'r') as host_file:
        hosts = host_file.read().splitlines()
    for n in range(0, len(hosts)):
        hosts[n] = hosts[n].split(',')
    for n in range(0, len(hosts)):
        for x in range(0, 2):
            hosts[n][x] = hosts[n][x].strip()
    return hosts

def exportCredentials(outputFileName, hosts, user, password):
    with open(outputFileName, 'w') as write_file:
        for host in hosts:
            print('~'*97)
            print('Connecting to {}'.format(host[0]))
            write_file.write(host[0])
            tn,status,cause = openTelnetConn(host[1], user, password)
            if status:
                print('Connected to {}'.format(host[1]))
                write_file.write(',Connected')
                tn.write(b'show run | i user\n')
                credentials = tn.read_until(b'#', 10)
                credentials = credentials.decode('utf-8').splitlines()
                for n in range (1, len(credentials)-1):
                    credential = credentials[n].split(' ')
                    write_file.write(  ',' + credential[1]
                                     + ',' + credential[3]
                                     + ',' + credential[6]  )
                write_file.write('\n')
                tn.write(b'exit\n')
                tn.close()
            else:
                write_file.write(',' + cause + '\n')
                print(cause)

def main():
    user = input('Enter your telnet username:')
    password = getpass.getpass()

    hostFileName = r'C:\Users\Tony Fermendzin\Desktop\Network Automation\Python\Python_Learning\aaa_Python Programming for Network Engineers (David Bombal)\hosts.csv'
    outputFileName = r'C:\Users\Tony Fermendzin\Desktop\Network Automation\Python\Python_Learning\aaa_Python Programming for Network Engineers (David Bombal)\output.csv'

    hosts = importHostFile(hostFileName)
    exportCredentials(outputFileName, hosts, user, password)

if __name__ == '__main__':
    main()