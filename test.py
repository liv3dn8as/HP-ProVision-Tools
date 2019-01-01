import paramiko
import time

def disable_paging(remote_conn):
    '''Disable paging on a HP router'''

    remote_conn.send("terminal length 1000\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output
	
if __name__ == '__main__':

# VARIABLES THAT NEED CHANGED
	ip = '10.1.1.1'
	uname = 'admin'
	pw = 'he770@d187.org'

remote_conn_pre=paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

remote_conn_pre.connect(ip, username=uname, password=pw, look_for_keys=False, allow_agent=False)
print ("SSH Connection established to %s" % ip)

# Use invoke_shell to establish an 'interactive session'
remote_conn=remote_conn_pre.invoke_shell()

#strip initial prompt
output=remote_conn.recv(1000)
print(output)

#turn off paging
disable_paging(remote_conn)

remote_conn.send("\n")
remote_conn.send("show run")

time.sleep(3)

output=remote_conn.recv(65535)
print(output)